# Gold Price Risk Model

A Monte Carlo simulation framework for modelling gold price risk using Geometric Brownian Motion (GBM) with a simple regime-switching volatility model.

## Overview

The model simulates 10,000 gold price paths across three time horizons (30, 60, 90 trading days) and computes Value at Risk (VaR) and Conditional VaR (CVaR / Expected Shortfall) from the resulting return distribution.

A rolling-volatility regime detector selects between a low-vol and high-vol GBM parameter set, giving the simulation a basic awareness of current market conditions.

## Project Structure

```
gold-risk-model/
├── main.py                  # Entry point — orchestrates the full pipeline
├── requirements.txt
├── README.md
└── gold_risk/
    ├── __init__.py
    ├── config.py            # All model parameters and constants
    ├── regime.py            # Historical return generation and regime detection
    ├── simulation.py        # Vectorised GBM price-path simulation
    ├── risk.py              # VaR and CVaR computation
    ├── plotting.py          # Matplotlib chart generation
    └── reporting.py         # Console summary and interpretation
```

## Methodology

### Geometric Brownian Motion

Each price path follows:

```
S(t + dt) = S(t) * exp((mu - 0.5 * sigma^2) * dt + sigma * sqrt(dt) * Z)
```

where `Z ~ N(0, 1)` and `dt = 1 / 252`.

### Regime Switching

The model compares 21-day rolling annualised volatility against the long-run annualised volatility of a synthetic price history:

- **Low-vol regime** — sigma = 12% per annum
- **High-vol regime** — sigma = 22% per annum

### Risk Metrics

| Metric | Definition |
|--------|------------|
| VaR 95% | Maximum loss not exceeded in 95% of simulated scenarios |
| CVaR 95% | Average loss in the worst 5% of simulated scenarios |

## Getting Started

### Install dependencies

```bash
pip install -r requirements.txt
```

### Run the model

```bash
python3 main.py
```

### Output

- Printed VaR / CVaR table for 30, 60, and 90-day horizons
- `gold_risk_results.png` — 6-panel chart:
  - **Top row**: simulated price-path fans with percentile bands
  - **Bottom row**: terminal return distributions with VaR / CVaR markers

## Parameters

All parameters are centralised in `gold_risk/config.py`:

| Parameter | Default | Description |
|-----------|---------|-------------|
| `SPOT_PRICE` | 2350.0 | Starting gold price (USD/oz) |
| `MU` | 0.08 | Annualised drift (8%) |
| `SIGMA_LOW` | 0.12 | Annualised vol, low-vol regime (12%) |
| `SIGMA_HIGH` | 0.22 | Annualised vol, high-vol regime (22%) |
| `N_SIMS` | 10,000 | Number of Monte Carlo paths |
| `HORIZONS` | [30, 60, 90] | Forecast horizons in trading days |
| `VAR_CONFIDENCE` | 0.95 | VaR confidence level |
| `RANDOM_SEED` | 42 | Seed for reproducibility |

## Dependencies

- `numpy` — vectorised simulation and statistics
- `pandas` — data structures (available for extension)
- `matplotlib` — chart generation

