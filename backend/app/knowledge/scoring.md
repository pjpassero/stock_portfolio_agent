# Fin Scoring Methodology

## Overview

Fin is designed to use deterministic financial mathematical formulas to get statistics for the user's portfolio. The score represents multiple dimensions of the user's portfolio. The score is intended to provide an overall summary of the portfolio risk while preserving the original risk measurements used to produce the score.

## Primary Components
- Volatility Risk
- Concentration Risk
- Drawdown Risk

## Risk Weights


The default scoring weights are as follows: 

- Alpha (α): 0.40 — Volatility
- Beta (β): 0.30 — Concentration
- Gamma (γ): 0.30 — Drawdown

The weights MUST sum to 1.0. 

The weights represent the relative importance of each risk component in the final portfolio score. 

A higher alpha means that volatility has a greater influence on the score. 

A higher beta means that concentration has a greater influence on the score.

A higher gamma means that drawdown has a greater influence on the final score.

## Volatility Risk

Volatility measures the varaiability of the portfolio returns. Higher portfolio volatility results in greater volatilityrisk. 

Portfolio variance is calculated as:

σ_p² = wᵀΣw

Annualized portfolio volatility is calculated as:

σ_p = √(252 × wᵀΣw)

The volatility risk component is normalized using:

V = min(σ_p / V_MAX, 1)

where:

V_MAX = 0.40

## Concentration Risk

Concentration measures how dependent the portfolio is on a limited number of positions. Fin uses the Herfindahl-Hirschman Index (HHI) as part of its concentration analysis. Although Fin provides the HHI to the user, Fin goes deeper into the analysis of where exactly the concentration is and whether or not there may be overlap between things like holding a single stock and an ETF containing multiple stocks, which could point to more underlying concentration that is not initally seen. 

HHI is calculated as:

HHI = Σ(w_i²)

where:

w_i = the weight of asset i in the portfolio.

## Drawdown Risk

Drawdown measires losses from a portfolio peak to a subsequent trough.

Drawdown at time t is calculated as:

D_t = (V_t - Peak_t) / Peak_t

Maximum drawdown is calculated as:

D_max = |min(D_t)|

The drawdown risk component is normalized using:

D = min(D_max / D_MAX, 1)

where:

D_MAX = 0.50


## Final Score

The portfolio's risk components are combined using the user's configured
risk weights.

The final portfolio risk score is calculated as:

Risk Score = 100 × (αV + βC + γD)

where:

α = 0.40

β = 0.30

γ = 0.30

V = normalized volatility risk

C = normalized concentration risk

D = normalized drawdown risk

## Interpretation

Higher scores indicate greater modeled portfolio risk.

Lower scores indicate lower modeled portfolio risk.

## Limitations

The Fin portfolio score is a model-generated measurement based on the
risk factors defined above. It does not represent a guarantee of future
portfolio performance.