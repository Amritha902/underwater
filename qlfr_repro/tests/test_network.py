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
