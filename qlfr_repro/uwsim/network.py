"""Packet-level UASN simulation with four routing protocols.

Protocols
---------
dbr     Depth-Based Routing (Yan et al., NETWORKING 2008): receiver-based, depth-difference
        holding time, suppression on overhearing a shallower forwarder.
vbf     Vector-Based Forwarding (Xie et al., NETWORKING 2006): receiver-based, forwards only
        inside a routing pipe around the source-to-sink vector.
qlfr    Q-learning anypath routing built from the design elements documented in the QLFR
        abstract (Zhou, Cao, Xiang, IEEE IoTJ 2021): depth- and energy-related rewards,
        a ranked forwarding-candidate set, priority-based holding times and overhearing
        suppression. Single-estimator Q-learning.
dqevdr  Our protocol: the same anypath machinery with Double Q-learning (two independent
        estimators) and an explicit, learned void penalty.

Simplifications (documented, applied to all protocols equally): no MAC collisions,
idle energy ignored, sinks acknowledge receptions reliably over their surface radio.
"""
from collections import defaultdict
import math
import numpy as np

from .channel import SOUND_SPEED
from .config import Config
from .energy import Battery
from .engine import Engine
from .metrics import Metrics
from .phy import packet_success_prob
from .topology import deploy, build_neighbours


class Estimator:
    """Per-node learned estimates: link success P[j] and neighbour value V[j]."""

    def __init__(self):
        self.p = {}
        self.v = {}
        self.n = defaultdict(int)


class Network:
    def __init__(self, cfg: Config, n_sensors: int, protocol: str, seed: int):
        self.cfg, self.protocol = cfg, protocol
        self.rng = np.random.default_rng(seed)
        self.nodes = deploy(n_sensors, cfg.n_sinks, cfg.area_xyz, self.rng)
        build_neighbours(self.nodes, cfg.comm_range)
        self.pos = np.stack([n.pos for n in self.nodes])
        self.dist = np.linalg.norm(self.pos[:, None, :] - self.pos[None, :, :], axis=-1)
        self.ps = np.vectorize(lambda d: packet_success_prob(
            d, cfg.packet_bits, cfg.source_level_db, cfg.noise_level_db, cfg.f_khz))(self.dist)
        self.bat = [Battery(math.inf if n.is_sink else cfg.initial_energy_j, cfg.tx_power_w, cfg.rx_power_w)
                    for n in self.nodes]
        self.sinks = [n.nid for n in self.nodes if n.is_sink]
        self.eng, self.m = Engine(), Metrics()
        self.seen = [set() for _ in self.nodes]          # packets already handled by a node
        self.pending = {}                                # (node, pkt) -> active flag dict
        self.await_ack = {}                              # (node, pkt) -> state
        self.consumed = 0.0
        self.first_death = None
        n_est = 2 if protocol == "dqevdr" else 1
        self.est = [[Estimator() for _ in range(n_est)] for _ in self.nodes]
        self.void = [self._is_void(i) for i in range(len(self.nodes))]

    # ------------------------------------------------------------------ helpers
    def depth(self, i):
        return self.nodes[i].depth

    def alive(self, i):
        return self.bat[i].alive

    def _is_void(self, i):
        """A sensor with no shallower neighbour cannot make depth progress (local-minimum node)."""
        if self.nodes[i].is_sink:
            return False
        return not any(self.depth(j) < self.depth(i) for j in self.nodes[i].neighbours)

    def _spend(self, i, joules):
        if self.nodes[i].is_sink:
            return
        before = self.bat[i].residual_j
        self.bat[i]._draw(joules)
        self.consumed += before - self.bat[i].residual_j
        if not self.bat[i].alive and self.first_death is None:
            self.first_death = (self.eng.now, self.m.generated)

    def _energy_frac(self, i):
        return 1.0 if self.nodes[i].is_sink else self.bat[i].residual_j / self.cfg.initial_energy_j

    # ------------------------------------------------------------ Q-learning core
    def _init_value(self, j):
        return self.cfg.sink_value if self.nodes[j].is_sink else -self.depth(j) / self.cfg.comm_range

    def _reward(self, s, j):
        c = self.cfg
        r = -c.hop_cost + c.w_depth * (self.depth(s) - self.depth(j)) / c.comm_range \
            + c.w_energy * (self._energy_frac(j) - 1.0)
        if self.protocol == "dqevdr" and self.void[j]:
            r -= c.void_penalty
        return r

    def _q(self, s, j, e: Estimator, e_eval: Estimator = None):
        """Q_s(j) = r + gamma * [P V_j + (1-P)(V_s - fail_penalty)]  (QELAR-style expectation)."""
        c = self.cfg
        p = e.p.get(j, 0.9)
        vj = (e_eval or e).v.get(j, self._init_value(j))
        vs = e.v.get(s, self._init_value(s))
        return self._reward(s, j) + c.gamma * (p * vj + (1 - p) * (vs - c.fail_penalty))

    def _candidates(self, s):
        return [j for j in self.nodes[s].neighbours if self.alive(j) and self.depth(j) < self.depth(s)]

    def _rank(self, s):
        cands = self._candidates(s)
        if not cands:
            return [], self._value(s)
        ests = self.est[s]
        if len(ests) == 1:
            q = {j: self._q(s, j, ests[0]) for j in cands}
        else:
            q = {j: 0.5 * (self._q(s, j, ests[0]) + self._q(s, j, ests[1])) for j in cands}
        ranked = sorted(cands, key=lambda j: -q[j])[: self.cfg.n_candidates]
        return ranked, q[ranked[0]]

    def _value(self, s):
        """Value advertised by s.  Q-learning: max_j Q(s,j).  Double Q: Q^B(argmax_j Q^A)."""
        if self.nodes[s].is_sink:
            return self.cfg.sink_value
        cands = self._candidates(s)
        if not cands:
            return self._init_value(s) - self.cfg.fail_penalty
        ests = self.est[s]
        if len(ests) == 1:
            return max(self._q(s, j, ests[0]) for j in cands)
        a, b = ests
        ja = max(cands, key=lambda j: self._q(s, j, a))
        jb = max(cands, key=lambda j: self._q(s, j, b))
        return 0.5 * (self._q(s, ja, b, b) + self._q(s, jb, a, a))

    def _learn(self, s, outcomes, values):
        """outcomes: {j: 1 success / 0 failure}; values: {j: V_j heard in j's header}."""
        lr = self.cfg.alpha
        ests = self.est[s]
        for j, ok in outcomes.items():
            e = ests[self.rng.integers(len(ests))]     # Double Q: each sample updates one estimator
            e.n[j] += 1
            e.p[j] = e.p.get(j, 0.9) + lr * (ok - e.p.get(j, 0.9))
            if ok and j in values:
                e.v[j] = e.v.get(j, self._init_value(j)) + lr * (values[j] - e.v.get(j, self._init_value(j)))
        for e in ests:
            e.v[s] = self._value(s)

    # -------------------------------------------------------------- packet flow
    def generate(self):
        alive = [n.nid for n in self.nodes if not n.is_sink and self.alive(n.nid)]
        if not alive:
            return
        src = int(self.rng.choice(alive))
        pkt = self.m.generated
        self.m.on_generate()
        self.pkt_info[pkt] = (src, self.eng.now, self._nearest_sink(src))
        self.seen[src].add(pkt)
        self._send(src, pkt, attempt=0)

    def _nearest_sink(self, i):
        return min(self.sinks, key=lambda k: self.dist[i, k])

    def _send(self, s, pkt, attempt):
        if not self.alive(s):
            return
        c = self.cfg
        hdr = {"sender": s, "depth": self.depth(s)}
        if self.protocol in ("qlfr", "dqevdr"):
            ranked, _ = self._rank(s)
            if not ranked:
                return                                      # stuck: no shallower neighbour
            hdr["ranked"] = ranked
            hdr["value"] = self._value(s)
            self.await_ack[(s, pkt)] = {"ranked": ranked, "attempt": attempt, "done": False}
            self.eng.schedule(2 * c.comm_range / SOUND_SPEED + c.n_candidates * self._slot() + 2 * c.packet_time,
                              self._ack_timeout, s, pkt)
        self._spend(s, c.tx_power_w * c.packet_time)
        self.m.transmissions += 1
        for j in self.nodes[s].neighbours:
            if self.alive(j):
                self.eng.schedule(self.dist[s, j] / SOUND_SPEED + c.packet_time, self._receive, j, s, pkt, hdr)

    def _slot(self):
        return self.cfg.comm_range / SOUND_SPEED + self.cfg.packet_time

    def _receive(self, j, s, pkt, hdr):
        if not self.alive(j):
            return
        self._spend(j, self.cfg.rx_power_w * self.cfg.packet_time)
        if self.rng.random() > self.ps[s, j]:
            return                                          # reception failed
        # implicit acknowledgement / suppression from overhearing a forward of pkt
        st = self.await_ack.get((j, pkt))
        if st and not st["done"] and hdr["depth"] < self.depth(j):
            self._ack(j, pkt, forwarder=s, value=hdr.get("value"))
        tok = self.pending.get((j, pkt))
        if tok and tok["active"] and hdr["depth"] < self.depth(j):
            tok["active"] = False                           # a better node already forwarded
        if self.nodes[j].is_sink:
            src, t0, _ = self.pkt_info[pkt]
            self.m.on_deliver(pkt, self.eng.now - t0)
            st_s = self.await_ack.get((s, pkt))
            if st_s and not st_s["done"]:
                self._ack(s, pkt, forwarder=j, value=self.cfg.sink_value)
            return
        if pkt in self.seen[j]:
            return
        hold = self._holding_time(j, s, pkt, hdr)
        if hold is None:
            return
        self.seen[j].add(pkt)
        tok = {"active": True}
        self.pending[(j, pkt)] = tok
        self.eng.schedule(hold, self._forward, j, pkt, tok)

    def _holding_time(self, j, s, pkt, hdr):
        c = self.cfg
        R = c.comm_range
        if self.protocol == "dbr":
            dd = hdr["depth"] - self.depth(j)
            if dd <= c.dbr_depth_threshold:
                return None
            tau = R / SOUND_SPEED
            return 2 * tau / R * (R - dd)                  # DBR: (2*tau/delta)(R - d), delta = R
        if self.protocol == "vbf":
            src, _, sink = self.pkt_info[pkt]
            a, b, p = self.pos[src], self.pos[sink], self.pos[j]
            ab = b - a
            t = np.clip(np.dot(p - a, ab) / np.dot(ab, ab), 0, 1)
            proj = np.linalg.norm(p - (a + t * ab))
            if proj > c.vbf_pipe_radius or self.dist[j, sink] >= self.dist[s, sink]:
                return None
            d = self.dist[s, j]
            sv = b - self.pos[s]
            cos = np.dot(self.pos[j] - self.pos[s], sv) / (np.linalg.norm(sv) * d + 1e-9)
            alpha = proj / c.vbf_pipe_radius + (R - d * cos) / R
            return math.sqrt(max(alpha, 0)) * c.max_hold_s + (R - d) / SOUND_SPEED
        ranked = hdr.get("ranked", [])
        if j not in ranked:
            return None
        return ranked.index(j) * self._slot()               # priority-based holding time

    def _forward(self, j, pkt, tok):
        if tok["active"] and self.alive(j):
            self._send(j, pkt, attempt=0)

    def _ack(self, s, pkt, forwarder, value):
        st = self.await_ack[(s, pkt)]
        st["done"] = True
        ranked = st["ranked"]
        outcomes = {}
        for k in ranked:
            if k == forwarder:
                outcomes[k] = 1
                break
            outcomes[k] = 0                                 # higher-ranked candidates did not forward
        if forwarder not in outcomes:
            outcomes[forwarder] = 1
        self._learn(s, outcomes, {forwarder: value} if value is not None else {})

    def _ack_timeout(self, s, pkt):
        st = self.await_ack.get((s, pkt))
        if not st or st["done"]:
            return
        st["done"] = True
        self._learn(s, {k: 0 for k in st["ranked"]}, {})
        if st["attempt"] < self.cfg.retx_limit:
            self._send(s, pkt, st["attempt"] + 1)

    # ----------------------------------------------------------------- driver
    def run(self, n_packets: int, interval_s: float, stop_on_first_death: bool = False):
        self.pkt_info = {}
        for k in range(n_packets):
            self.eng.schedule(k * interval_s, self.generate)
        if stop_on_first_death:
            while self.eng._q and self.first_death is None:
                self.eng.run(until=self.eng._q[0][0])
        else:
            self.eng.run()
        return self.summary()

    def summary(self):
        sensors = [i for i, n in enumerate(self.nodes) if not n.is_sink]
        res = np.array([self.bat[i].residual_j for i in sensors])
        return {
            "pdr": self.m.pdr,
            "delay_s": self.m.avg_delay,
            "energy_per_pkt_j": self.consumed / max(len(self.m.delivered), 1),
            "transmissions_per_pkt": self.m.transmissions / max(self.m.generated, 1),
            "residual_std_j": float(res.std()),
            "generated": self.m.generated,
            "delivered": len(self.m.delivered),
            "first_death_pkt": None if self.first_death is None else self.first_death[1],
            "void_nodes": int(sum(self.void[i] for i in sensors)),
        }
