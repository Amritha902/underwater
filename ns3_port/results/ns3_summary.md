# ns-3 evaluation: QLFR vs LAQR (MAC: UanMacAloha)

Runs: 300 (10 seeds x 5 densities x 3 protocols x 2 scenarios). Mean +/- 95% CI over seeds.

## Scenario: desync

### Averaged over densities

| Protocol | PDR | Delay (s) | Lifetime (s) | Energy (J) | Tx/packet |
|---|---|---|---|---|---|
| QLFR (P_th = 0.90) | 0.800 ± 0.008 | 1.997 ± 0.036 | 46,045 ± 549 | 4,663 ± 39 | 37.5 ± 0.6 |
| QLFR (P_th = 0.97) | 0.801 ± 0.007 | 1.999 ± 0.034 | 45,935 ± 582 | 4,682 ± 42 | 37.8 ± 0.6 |
| LAQR | 0.572 ± 0.015 | 0.825 ± 0.011 | 83,316 ± 1,307 | 2,808 ± 17 | 8.3 ± 0.1 |

### Per density (mean PDR / delay / lifetime)

| Nodes | QLFR (P_th = 0.90) | QLFR (P_th = 0.97) | LAQR |
|---|---|---|---|
| 100 | 0.637 / 1.35 s / 68,859 s | 0.637 / 1.35 s / 68,859 s | 0.521 / 0.84 s / 103,641 s |
| 200 | 0.800 / 1.88 s / 45,448 s | 0.800 / 1.88 s / 45,448 s | 0.588 / 0.83 s / 89,874 s |
| 300 | 0.844 / 2.07 s / 39,930 s | 0.843 / 2.07 s / 40,118 s | 0.596 / 0.81 s / 77,071 s |
| 400 | 0.862 / 2.24 s / 38,674 s | 0.866 / 2.26 s / 38,190 s | 0.590 / 0.82 s / 73,538 s |
| 500 | 0.858 / 2.44 s / 37,315 s | 0.862 / 2.44 s / 37,060 s | 0.562 / 0.83 s / 72,457 s |

### Paired LAQR vs QLFR (same seed and density; averaged over densities per seed)

| Baseline | ΔPDR | ΔDelay (s) | Lifetime ratio | Energy ratio | Tx ratio |
|---|---|---|---|---|---|
| QLFR (P_th = 0.90) | -0.228 ± 0.014 | -1.172 ± 0.032 | 1.85 ± 0.02 | 0.62 ± 0.01 | 0.25 ± 0.01 |
| QLFR (P_th = 0.97) | -0.230 ± 0.015 | -1.174 ± 0.030 | 1.86 ± 0.02 | 0.61 ± 0.00 | 0.25 ± 0.00 |

## Scenario: sync

### Averaged over densities

| Protocol | PDR | Delay (s) | Lifetime (s) | Energy (J) | Tx/packet |
|---|---|---|---|---|---|
| QLFR (P_th = 0.90) | 0.703 ± 0.010 | 2.296 ± 0.057 | 53,760 ± 1,069 | 4,294 ± 42 | 33.2 ± 0.5 |
| QLFR (P_th = 0.97) | 0.703 ± 0.010 | 2.296 ± 0.057 | 53,760 ± 1,069 | 4,294 ± 42 | 33.2 ± 0.5 |
| LAQR | 0.250 ± 0.008 | 0.938 ± 0.011 | 101,465 ± 1,318 | 2,452 ± 14 | 4.9 ± 0.1 |

### Per density (mean PDR / delay / lifetime)

| Nodes | QLFR (P_th = 0.90) | QLFR (P_th = 0.97) | LAQR |
|---|---|---|---|
| 100 | 0.462 / 1.62 s / 84,760 s | 0.462 / 1.62 s / 84,760 s | 0.214 / 0.91 s / 128,042 s |
| 200 | 0.699 / 2.20 s / 53,627 s | 0.699 / 2.20 s / 53,627 s | 0.246 / 0.94 s / 110,834 s |
| 300 | 0.767 / 2.38 s / 45,543 s | 0.767 / 2.38 s / 45,543 s | 0.267 / 0.92 s / 94,136 s |
| 400 | 0.797 / 2.52 s / 43,051 s | 0.797 / 2.52 s / 43,051 s | 0.261 / 0.93 s / 88,955 s |
| 500 | 0.791 / 2.76 s / 41,822 s | 0.791 / 2.76 s / 41,822 s | 0.260 / 0.98 s / 85,360 s |

### Paired LAQR vs QLFR (same seed and density; averaged over densities per seed)

| Baseline | ΔPDR | ΔDelay (s) | Lifetime ratio | Energy ratio | Tx ratio |
|---|---|---|---|---|---|
| QLFR (P_th = 0.90) | -0.454 ± 0.009 | -1.358 ± 0.061 | 1.96 ± 0.04 | 0.58 ± 0.01 | 0.18 ± 0.00 |
| QLFR (P_th = 0.97) | -0.454 ± 0.009 | -1.358 ± 0.061 | 1.96 ± 0.04 | 0.58 ± 0.01 | 0.18 ± 0.00 |

