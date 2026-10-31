"""3-D deployment and neighbour tables."""
from dataclasses import dataclass, field
import numpy as np


@dataclass
class Node:
    nid: int
    pos: np.ndarray            # (x, y, z); z = depth in metres (0 = surface)
    is_sink: bool = False
    neighbours: list = field(default_factory=list)

    @property
    def depth(self) -> float:
        return float(self.pos[2])


def deploy(n_sensors: int, n_sinks: int, size_xyz, rng: np.random.Generator):
    """Uniform random sensors in the box; sinks uniformly on the surface (depth 0)."""
    sx, sy, sz = size_xyz
    nodes = []
    for i in range(n_sinks):
        nodes.append(Node(i, np.array([rng.uniform(0, sx), rng.uniform(0, sy), 0.0]), is_sink=True))
    for j in range(n_sensors):
        nodes.append(Node(n_sinks + j, np.array([rng.uniform(0, sx), rng.uniform(0, sy), rng.uniform(0, sz)])))
    return nodes


def build_neighbours(nodes, comm_range: float) -> None:
    pos = np.stack([n.pos for n in nodes])
    d = np.linalg.norm(pos[:, None, :] - pos[None, :, :], axis=-1)
    for i, n in enumerate(nodes):
        n.neighbours = [j for j in np.nonzero((d[i] <= comm_range) & (d[i] > 0))[0].tolist()]


def distance(a: Node, b: Node) -> float:
    return float(np.linalg.norm(a.pos - b.pos))
