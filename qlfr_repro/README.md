# QLFR re-implementation (Python)

Base paper: Y. Zhou, T. Cao, W. Xiang, "Anypath Routing Protocol Design via Q-Learning for Underwater Sensor Networks," IEEE Internet of Things Journal, vol. 8, no. 10, pp. 8173-8190, 2021. doi:10.1109/JIOT.2020.3042901 (preprint: arXiv:2002.09623).

## Status

- `uwsim/`: generic simulator core (Thorp channel, energy, 3-D topology, event engine, metrics), with tests.
- QLFR protocol, baselines, paper parameters and figure reproduction: **blocked on access to the paper's full text** (arxiv.org is not reachable from this environment).

## Run tests

```bash
python3 -m pytest -q tests
```
