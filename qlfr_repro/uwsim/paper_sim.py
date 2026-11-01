"""Faithful re-implementation of QLFR (Zhou, Cao, Xiang, IEEE IoTJ 2021; arXiv:2002.09623v1)
and the baselines it is compared against (DBR, EEDBR, DVOR, QELAR), plus our DQ-EVDR.

Equation numbers refer to arXiv:2002.09623v1.
Values the paper does not specify are listed in PaperConfig with "ASSUMED".
"""
from dataclasses import dataclass, field
import heapq
import itertools
import math

import numpy as np

V0 = 1500.0  # m/s, paper Sec. VI-C / Table II


@dataclass
class PaperConfig:
    # ---- Table II (given in the paper) ----
    n_sensors: int = 300
    n_sources: int = 5
    n_sinks: int = 5
    area: float = 500.0            # 500 x 500 x 500 m
    psi_t: float = 2.0             # W, transmission power
    psi_r: float = 0.5             # W, reception power
    R: float = 150.0               # m, maximal transmission range
    gamma: float = 0.8             # discount factor
    k: float = 0.05                # s, holding-time step (default used for Figs. 6-8, 13-15)
    speed: float = 3.0             # m/s, random-walk speed (default for Figs. 6-8, 10-12)
    # ---- ASSUMED (not given in the paper) ----
    alpha: float = 0.5             # ASSUMED learning rate
    M: int = 500                   # ASSUMED packet size (bits)
    mu: float = 10000.0            # ASSUMED data rate (bit/s) -> tx/rx energy per packet
    f_khz: float = 10.0            # ASSUMED carrier frequency
    kappa: float = 1.5             # ASSUMED spreading factor (paper: kappa in [1, 2])
    eb_n0_db: float = 63.0         # ASSUMED Eb/N0 (gives p ~ 0.9 at R with Rayleigh fading)
    e_ini: float = 1000.0          # ASSUMED initial energy (J); lifetime via Eq. (39)-(40), no node dies mid-run
    v_init: float = -5.0           # ASSUMED initial V of sensor nodes for QELAR (sink V = 0)
    rounds: int = 100              # ASSUMED: each round all 5 sources send one packet
    round_s: float = 10.0          # ASSUMED round length (s); nodes move speed*round_s per round
    list_len0: int = 3             # ASSUMED initial priority-list length (Sec. IV-D)
    list_len_max: int = 8          # ASSUMED cap on priority-list length
    pdr_th: float = 0.90           # ASSUMED P_th for the multipath suppression scheme (Fig. 4); calibrated
    # baselines (their own papers' constants are not in QLFR; ASSUMED)
    dbr_delta: float = 150.0       # DBR: holding time (2*tau/delta)(R - d)
    eedbr_tmax: float = 0.2        # EEDBR: energy-based holding window (s)
    dvor_k: float = 0.05           # DVOR: holding step per extra hop (s)
    qelar_g: float = 1.0           # QELAR reward constants
    qelar_a1: float = 0.5
    qelar_a2: float = 0.5
    qelar_retx: int = 3
    qelar_sweeps: int = 10         # ASSUMED value-update sweeps per round
    # DQ-EVDR (ours)
    w_link: float = 1.0
    void_cost: float = 1.0


def thorp_db_per_km(f):
    f2 = f * f
    return 2.75e-4 * f2 + 44 * f2 / (4100 + f2) + 0.11 * f2 / (1 + f2) + 1e-3     # Eq. (17)


def link_success(dist_m, cfg: PaperConfig):
    """Eq. (16)-(22): Urick attenuation, Rayleigh-averaged BPSK BER, p = (1 - pe)^M."""
    d = np.maximum(dist_m, 1.0)
    att_db = 10 * cfg.kappa * np.log10(d) + (d / 1000.0) * thorp_db_per_km(cfg.f_khz)
    snr = 10 ** ((cfg.eb_n0_db - att_db) / 10)                                       # Eq. (18)
    pe = 0.5 * (1 - np.sqrt(snr / (1 + snr)))                                         # Eq. (21)
    return (1 - pe) ** cfg.M                                                          # Eq. (22)


class Sim:
    def __init__(self, cfg: PaperConfig, protocol: str, seed: int):
        self.cfg, self.proto = cfg, protocol
        self.rng = np.random.default_rng(seed)
        c = cfg
        N = c.n_sensors
        self.N = N + c.n_sinks
        pos = self.rng.uniform(0, c.area, size=(self.N, 3))
        pos[N:, 2] = 0.0                                   # sinks on the surface (depth 0)
        self.src = list(range(c.n_sources))
        pos[self.src, 2] = c.area                          # sources at the bottom layer
        self.pos = pos
        self.is_sink = np.zeros(self.N, bool)
        self.is_sink[N:] = True
        self.energy = np.full(self.N, c.e_ini)
        self.used = np.zeros(self.N)                       # energy consumed per node
        self.Q = np.zeros((self.N, self.N))
        self.Q2 = np.zeros((self.N, self.N))               # second estimator (DQ-EVDR)
        self.V = np.zeros(self.N)
        if protocol == "qelar":
            self.V[:] = cfg.v_init
            self.V[N:] = 0.0
        self.list_len = c.list_len0
        self.gen = 0
        self.delivered = {}
        self.tx_count = 0
        self.t_pkt = c.M / c.mu
        self._refresh()

    # ------------------------------------------------------------------ topology
    def _refresh(self):
        c = self.cfg
        diff = self.pos[:, None, :] - self.pos[None, :, :]
        self.dist = np.linalg.norm(diff, axis=-1)
        self.adj = (self.dist <= c.R) & ~np.eye(self.N, dtype=bool)
        self.p = link_success(self.dist, c)
        self.depth = self.pos[:, 2].copy()
        if self.proto == "dvor":
            self._hop_counts()

    def _move(self):
        c = self.cfg
        step = c.speed * c.round_s
        d = self.rng.normal(size=(self.N, 3))
        d /= np.linalg.norm(d, axis=1, keepdims=True)
        new = self.pos + step * d
        new = np.abs(new)                                   # reflect at 0
        new = c.area - np.abs(c.area - new)                 # reflect at area
        new[self.is_sink, 2] = 0.0
        new[self.src, 2] = c.area
        sink_xy = self.pos[self.is_sink]                    # sinks are stationary
        new[self.is_sink] = sink_xy
        self.pos = new
        self._refresh()

    def _hop_counts(self):
        """DVOR: hop count to the nearest sink via a breadth-first query from all sinks."""
        hop = np.full(self.N, np.inf)
        frontier = list(np.nonzero(self.is_sink)[0])
        hop[frontier] = 0
        while frontier:
            nxt = []
            for u in frontier:
                for v in np.nonzero(self.adj[u])[0]:
                    if hop[v] == np.inf:
                        hop[v] = hop[u] + 1
                        nxt.append(v)
            frontier = nxt
        self.hop = hop

    # ------------------------------------------------------------- Q-learning
    def _ce(self, idx):
        e = np.where(self.is_sink[idx], self.cfg.e_ini, self.energy[idx])
        return 1 - e / self.cfg.e_ini                                                 # Eq. (6)

    def _qlfr_reward(self):
        c = self.cfg
        dd = self.depth[:, None] - self.depth[None, :]                                # d(s_i, s_j)
        cd = 0.5 * (1 - dd / c.R)                                                     # Eq. (7), |d|max = R
        ce = self._ce(np.arange(self.N))
        return -ce[:, None] - ce[None, :] - cd                                        # Eq. (5)

    def _update_q(self):
        """One iteration of Eq. (8) for every node over all its neighbours (once per round)."""
        c = self.cfg
        A = self.adj & ~self.is_sink[:, None]
        if self.proto in ("qlfr",):
            r = self._qlfr_reward()
            target = r + c.gamma * self.V[None, :]
            self.Q = np.where(A, c.alpha * target + (1 - c.alpha) * self.Q, self.Q)
            masked = np.where(A, self.Q, -np.inf)
            self.V = np.where(A.any(1), masked.max(1), self.V)
            self.V[self.is_sink] = 0.0
        elif self.proto == "dqevdr":
            r = self._qlfr_reward()
            # link quality from a noisy one-shot sample (hello reception), Bernoulli(p_ij)
            heard = self.rng.random(self.p.shape) < self.p
            r = r - c.w_link * (1 - heard)
            void = self._void_mask()
            r = r - c.void_cost * void[None, :]
            # Double Q-learning: update one table, evaluate argmax of it with the other
            upd_a = self.rng.random() < 0.5
            Qa, Qb = (self.Q, self.Q2) if upd_a else (self.Q2, self.Q)
            ma = np.where(A, Qa, -np.inf)
            mb = np.where(A, Qb, -np.inf)
            arg = np.argmax(ma, axis=1)
            v_eval = np.where(A.any(1), Qb[np.arange(self.N), arg], 0.0)
            v_eval[self.is_sink] = 0.0
            target = r + c.gamma * v_eval[None, :]
            Qa_new = np.where(A, c.alpha * target + (1 - c.alpha) * Qa, Qa)
            if upd_a:
                self.Q = Qa_new
            else:
                self.Q2 = Qa_new
            avg = 0.5 * (self.Q + self.Q2)
            self.V = np.where(A.any(1), np.where(A, avg, -np.inf).max(1), self.V)
            self.V[self.is_sink] = 0.0
        elif self.proto == "qelar":
            # QELAR (Hu & Fei 2010): r = -g - a1[c(s)+c(sj)] + a2[d(s)+d(sj)],
            # d(s) = (2/pi) arctan(E_res(s) - mean neighbour E_res); Q uses link success p.
            ce = self._ce(np.arange(self.N))
            e = np.where(self.is_sink, c.e_ini, self.energy)
            nb = np.maximum(self.adj.sum(1), 1)
            mean_nb = (self.adj * e[None, :]).sum(1) / nb
            dn = (2 / math.pi) * np.arctan(e - mean_nb)
            r = -c.qelar_g - c.qelar_a1 * (ce[:, None] + ce[None, :]) + c.qelar_a2 * (dn[:, None] + dn[None, :])
            for _ in range(c.qelar_sweeps):          # several learning updates per round
                target = r + c.gamma * (self.p * self.V[None, :] + (1 - self.p) * self.V[:, None])
                self.Q = np.where(A, target, self.Q)
                masked = np.where(A, self.Q, -np.inf)
                self.V = np.where(A.any(1), masked.max(1), self.V)
                self.V[self.is_sink] = 0.0

    def _void_mask(self):
        shallower = self.adj & (self.depth[None, :] < self.depth[:, None])
        return (~shallower.any(1)) & ~self.is_sink

    def _priority_list(self, s):
        nb = np.nonzero(self.adj[s] & (self.depth < self.depth[s]))[0]
        if nb.size == 0:
            return []
        q = self.Q[s, nb] if self.proto == "qlfr" else 0.5 * (self.Q[s, nb] + self.Q2[s, nb])
        order = nb[np.argsort(-q)]
        return list(order[: self.list_len])

    # ----------------------------------------------------------- event engine
    def _sched(self, t, fn, *a):
        heapq.heappush(self.q, (t, next(self.cnt), fn, a))

    def _transmit(self, t, s, pkt, info):
        """s broadcasts pkt at time t. Energy per Eq. (33)-(36)."""
        self._spend(s, self.cfg.psi_t * self.t_pkt)
        self.tx_count += 1
        for j in np.nonzero(self.adj[s])[0]:
            self._spend(j, self.cfg.psi_r * self.t_pkt)
            if self.rng.random() < self.p[s, j]:
                self._sched(t + self.dist[s, j] / V0, self._recv, j, s, pkt, info)

    def _spend(self, i, joules):
        if not self.is_sink[i]:
            self.energy[i] -= joules
            self.used[i] += joules

    def _recv(self, t, j, s, pkt, info):
        st = self.state.setdefault(pkt, {"forwarded": set(), "held": {}})
        if j in st["held"]:
            st["held"][j]["cancel"] = True                  # overheard during holding time
        if self.is_sink[j]:
            if pkt not in self.delivered:
                self.delivered[pkt] = t - self.t0[pkt]
            if self.proto == "qelar":
                st["acked"] = True
            return
        if j in st["forwarded"]:
            return
        hold = self._hold(j, s, pkt, info)
        if hold is None:
            return
        tok = {"cancel": False}
        st["held"][j] = tok
        self._sched(t + hold, self._fire, j, pkt, tok)

    def _hold(self, j, s, pkt, info):
        c = self.cfg
        if self.proto in ("qlfr", "dqevdr"):
            pl = info.get("plist", [])
            if j not in pl:
                return None                                  # Alg. 1 lines 4-5
            return c.k * pl.index(j)                         # Eq. (15): tau(n) = k (n - 1)
        if self.proto == "qelar":
            return 0.0 if info.get("next") == j else None
        dd = self.depth[s] - self.depth[j]
        if self.proto == "dbr":
            if dd <= 0:
                return None
            tau = c.R / V0
            return 2 * tau / c.dbr_delta * (c.R - dd)
        if self.proto == "eedbr":
            if dd <= 0:
                return None
            e = max(self.energy[j], 0) / c.e_ini
            return c.eedbr_tmax * (1 - e) + (c.R - dd) / V0
        if self.proto == "dvor":
            if not self.hop[j] < self.hop[s]:
                return None
            return c.dvor_k * (self.hop[j] - (self.hop[s] - 1)) + (c.R - self.dist[s, j]) / V0
        raise ValueError(self.proto)

    def _fire(self, t, j, pkt, tok):
        st = self.state[pkt]
        st["held"].pop(j, None)
        if tok["cancel"] or j in st["forwarded"]:
            return                                           # Alg. 1 lines 12-13
        st["forwarded"].add(j)
        self._send(t, j, pkt)

    def _send(self, t, s, pkt, attempt=0):
        info = {}
        if self.proto in ("qlfr", "dqevdr"):
            info["plist"] = self._priority_list(s)
            if not info["plist"]:
                return
        if self.proto == "qelar":
            nb = np.nonzero(self.adj[s])[0]
            if nb.size == 0:
                return
            info["next"] = int(nb[np.argmax(self.Q[s, nb])])
            self.state.setdefault(pkt, {"forwarded": set(), "held": {}})
            self._sched(t + 2 * self.cfg.R / V0 + 1e-3, self._qelar_check, s, pkt, attempt, info["next"])
        self._transmit(t, s, pkt, info)

    def _qelar_check(self, t, s, pkt, attempt, nxt):
        """QELAR retransmission: if the chosen next hop did not forward (and not delivered), retry."""
        st = self.state[pkt]
        if pkt in self.delivered or nxt in st["forwarded"] or st.get("acked"):
            return
        if attempt < self.cfg.qelar_retx:
            self._send(t, s, pkt, attempt + 1)

    # ------------------------------------------------------------------ driver
    def run(self):
        c = self.cfg
        self.q, self.cnt = [], itertools.count()
        self.state, self.t0 = {}, {}
        for rnd in range(c.rounds):
            t_start = rnd * c.round_s
            if rnd:
                self._move()
            self._update_q()
            for s in self.src:
                pkt = self.gen
                self.gen += 1
                self.t0[pkt] = t_start
                self.state[pkt] = {"forwarded": {s}, "held": {}}
                self._send(t_start, s, pkt)
            while self.q and self.q[0][0] < t_start + c.round_s:
                t, _, fn, a = heapq.heappop(self.q)
                fn(t, *a)
            self.q.clear()
            # multipath suppression scheme (Sec. IV-D, Fig. 4): adapt list length from sink PDR
            pdr = len(self.delivered) / self.gen
            if pdr > c.pdr_th:
                self.list_len = max(1, self.list_len - 1)
            else:
                self.list_len = min(c.list_len_max, self.list_len + 1)
        return self.result()

    def result(self):
        c = self.cfg
        T_run = c.rounds * c.round_s
        sensors = ~self.is_sink
        used = np.maximum(self.used[sensors], 1e-12)
        lifetime = float(np.min(c.e_ini * T_run / used))                              # Eq. (39)-(40)
        return {
            "pdr": len(self.delivered) / self.gen,
            "delay_s": float(np.mean(list(self.delivered.values()))) if self.delivered else float("nan"),
            "energy_j": float(self.used[sensors].sum()),
            "lifetime_s": lifetime,
            "tx_per_pkt": self.tx_count / self.gen,
        }
