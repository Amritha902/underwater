# QLFR re-implementation (Python)

Base paper: Y. Zhou, T. Cao, W. Xiang, "Anypath Routing Protocol Design via Q-Learning for Underwater Sensor Networks," IEEE Internet of Things Journal, vol. 8, no. 10, pp. 8173-8190, 2021. doi:10.1109/JIOT.2020.3042901 (preprint: arXiv:2002.09623).

## Status

- `uwsim/`: generic simulator core (Thorp channel, energy, 3-D topology, event engine, metrics), with tests.
- `uwsim/network.py`: DBR, VBF, QLFR (abstract-level re-implementation) and DQ-EVDR (ours).
- `experiments.py` and `plots.py`: write `results/*.csv`, `results/summary.md` and `figures/*.png`.
- Report: `../docs/01_base_paper_reimplementation.md`. Brainstorming: `../docs/02_brainstorming.md`.
- Matching the paper's exact equations and numbers still needs its full text (arxiv.org is blocked here).

## Run

```bash
python3 -m pytest -q tests
python3 experiments.py
python3 plots.py
```
