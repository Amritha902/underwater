from uwsim.config import Config
from uwsim.network import Network


def test_all_protocols_deliver_in_dense_network():
    for proto in ("dbr", "vbf", "qlfr", "dqevdr"):
        r = Network(Config(), 300, proto, seed=3).run(n_packets=60, interval_s=20)
        assert r["generated"] == 60
        assert r["pdr"] > 0.5, proto


def test_deterministic_given_seed():
    a = Network(Config(), 150, "dqevdr", seed=7).run(40, 20)
    b = Network(Config(), 150, "dqevdr", seed=7).run(40, 20)
    assert a == b


def test_paper_sim_runs_and_delay_matches_holding_time_model():
    from uwsim.paper_sim import Sim, PaperConfig, link_success
    import numpy as np
    c = PaperConfig(n_sensors=150, rounds=20)
    assert 0.85 < float(link_success(np.array(150.0), c)) < 0.92
    for proto in ("dbr", "eedbr", "dvor", "qlfr", "qelar", "dqevdr"):
        r = Sim(c, proto, seed=0).run()
        assert 0 < r["pdr"] <= 1, proto
        assert 0.3 < r["delay_s"] < 1.5, proto


def test_v2_variants_and_adaptive_list():
    import numpy as np
    from uwsim.paper_sim import Sim, PaperConfig, V2_VARIANTS
    c = PaperConfig(n_sensors=150, rounds=15)
    for proto in V2_VARIANTS:
        r = Sim(c, proto, seed=0).run()
        assert 0 < r["pdr"] <= 1 and not np.isnan(r["v_bias"]), proto
    sim = Sim(c, "dqevdr2", seed=0)
    s = next(i for i in range(sim.N) if not sim.is_sink[i] and (sim.adj[i] & (sim.depth < sim.depth[i])).sum() >= 3)
    sim.P[0][:] = 0.995
    sim.P[1][:] = 0.995
    assert len(sim._priority_list(s)) == 1          # one 0.995 link already meets rho = 0.99
    sim.P[0][:] = 0.5
    sim.P[1][:] = 0.5
    assert len(sim._priority_list(s)) >= 3          # weak links need more candidates


def test_final_laqr_config_runs():
    import json, os
    from uwsim.paper_sim import Sim, PaperConfig
    cfg = json.load(open(os.path.join(os.path.dirname(__file__), "..", "results", "final_config.json")))["final"]
    r = Sim(PaperConfig(n_sensors=150, rounds=15, lq_beta=cfg["beta"], rho=cfg["rho"]), cfg["protocol"], 0).run()
    assert 0 < r["pdr"] <= 1
