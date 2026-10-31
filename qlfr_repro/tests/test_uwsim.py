import math
import numpy as np
from uwsim.channel import thorp_absorption_db_per_km, path_loss_db, propagation_delay
from uwsim.energy import Battery
from uwsim.topology import deploy, build_neighbours
from uwsim.engine import Engine


def test_thorp_known_values():
    # Hand-computed from Thorp's formula: 10 kHz -> 1.187 dB/km, 25 kHz -> 6.105 dB/km
    assert abs(thorp_absorption_db_per_km(10) - 1.187) < 1e-3
    assert abs(thorp_absorption_db_per_km(25) - 6.105) < 1e-3


def test_path_loss_monotonic():
    assert path_loss_db(200, 10) < path_loss_db(400, 10)


def test_delay():
    assert math.isclose(propagation_delay(1500), 1.0)


def test_battery():
    b = Battery(initial_j=10, tx_power_w=2, rx_power_w=0.1)
    b.transmit(1.0); b.receive(10.0)
    assert math.isclose(b.residual_j, 7.0)
    b.transmit(10)
    assert b.residual_j == 0 and not b.alive


def test_topology_neighbours_symmetric():
    rng = np.random.default_rng(0)
    nodes = deploy(50, 3, (500, 500, 500), rng)
    build_neighbours(nodes, 250)
    for n in nodes:
        for j in n.neighbours:
            assert n.nid in nodes[j].neighbours
    assert all(n.depth == 0 for n in nodes if n.is_sink)


def test_engine_order():
    e, out = Engine(), []
    e.schedule(2, out.append, "b"); e.schedule(1, out.append, "a")
    e.run()
    assert out == ["a", "b"]
