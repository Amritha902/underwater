# QLFR re-implementation (Python)

Base paper: Y. Zhou, T. Cao, W. Xiang, "Anypath Routing Protocol Design via Q-Learning for Underwater Sensor Networks," IEEE Internet of Things Journal, vol. 8, no. 10, pp. 8173-8190, 2021. doi:10.1109/JIOT.2020.3042901 (preprint: arXiv:2002.09623).

## Paper-faithful reproduction (main result)

- `uwsim/paper_sim.py`: QLFR exactly as in arXiv:2002.09623v1 (Eq. 5–8, 15–22, 33–40; Table II), with DBR, EEDBR, DVOR, QELAR and DQ-EVDR.
- `paper_experiments.py`, `paper_plots.py`, `paper_sensitivity.py`: reproduce Figs. 6–15 and write `figures/paper_*.png`, `results/paper_comparison.md`.
- Report: `../docs/01_base_paper_reimplementation.md`.

## Earlier prototype (superseded)

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
