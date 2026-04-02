# Stock EDA

Exploratory data analysis of stock market data using Python. Two components: an interactive
analysis tool for any stocks, and a deep dive into five AI-related stocks over 2019–2024.

Built as a first real Python project after completing CS50P, using pandas, yfinance,
matplotlib, and seaborn.

---

## Project Structure
```
Stock_EDA/
├── one.py            # Part 1: interactive analysis tool
├── analysis.py       # Part 2: AI stocks deep dive
├── requirements.txt  # dependencies
├── data/
│   └── stocks.csv    # cached price data
└── images/           # generated charts
    ├── price_chart.png
    ├── return_hist.png
    ├── correlation.png
    ├── cumulative_returns.png
    ├── correlation_analysis.png
    ├── drawdown_2022.png
    └── portfolio_vs_nvda.png
```

---

## Part 1: Interactive Analysis Tool (`one.py`)

A command-line tool that accepts any valid Yahoo Finance tickers and a date range,
then automatically downloads historical price data, computes four key financial metrics,
and saves four charts to the `images/` directory.

### How to Run
```bash
pip install -r requirements.txt
python3 one.py
```

### Usage
```
Enter tickers (e.g. AAPL MSFT TSLA):
> AAPL MSFT TSLA
Start date:
> 2020-03-04
End date:
> 2024-04-05
```

Accepts flexible date formats — `2020-01-01`, `Jan 1 2020`, `2020/01/01`, `20200101` etc.
Uses `python-dateutil` to parse any recognisable date string automatically.

### Input Validation

- Tickers must contain letters only (e.g. `AAPL`, not `AA11`)
- End date must be strictly after start date
- Invalid or delisted tickers are detected after download and flagged with a clear error message
- Date parsing errors are caught and reported before any data is downloaded

### Output
```
         Ann. Return  Ann. Volatility  Sharpe Ratio  Max Drawdown
Ticker
AAPL          0.2557           0.3252        0.7862       -0.3091
MSFT          0.2788           0.3168        0.8801       -0.3715
TSLA          0.5147           0.6521        0.7892       -0.7363
```

### Charts (saved to `images/`)

| Chart | Description |
|-------|-------------|
| `price_chart.png` | Closing prices with MA20 and MA50 moving averages |
| `return_hist.png` | Daily return distribution histogram for each ticker |
| `correlation.png` | Pairwise correlation matrix heatmap |
| `cumulative_returns.png` | Cumulative growth of $1 invested from start date |

---

## Part 2: AI Stocks Deep Dive (`analysis.py`)

Fixed analysis of five AI-related stocks — NVDA, TSLA, MSFT, GOOGL, META — over
2019–2024 (1,258 trading days). Answers four specific questions about risk, correlation,
resilience, and diversification.
```bash
python3 analysis.py
```

### Stocks Analysed

| Ticker | Company | AI Relevance |
|--------|---------|--------------|
| NVDA | NVIDIA | GPU infrastructure powering AI training worldwide |
| MSFT | Microsoft | Major investor in OpenAI, integrating AI across all products |
| GOOGL | Alphabet | Investor in Anthropic, developed Gemini and TPU hardware |
| META | Meta | In-house AI research lab, open-sourced LLaMA model family |
| TSLA | Tesla | Autonomous driving, Dojo supercomputer, Optimus robot |

These five stocks were chosen because they each represent a different angle of the AI
investment thesis — hardware (NVDA), cloud/software (MSFT, GOOGL), consumer social (META),
and physical AI (TSLA).

---

### Q1: Best Risk-Adjusted Return (2019–2024)
```
         Ann. Return  Ann. Volatility  Sharpe Ratio  Max Drawdown
NVDA          0.6718           0.5177        1.2977       -0.6634
TSLA          0.7081           0.6470        1.0945       -0.7363
MSFT          0.3203           0.3049        1.0505       -0.3715
GOOGL         0.2460           0.3181        0.7733       -0.4432
META          0.2891           0.4363        0.6626       -0.7674
```

**NVDA had the best risk-adjusted return (Sharpe: 1.2977)**, despite not having the
highest raw return. TSLA delivered higher absolute returns (70.8% annualised) but with
significantly more volatility (64.7%), resulting in a lower Sharpe Ratio (1.09).
META had the worst risk-adjusted performance — high volatility combined with a relatively
modest return, partly due to its costly metaverse pivot in 2022–2023.

---

### Q2: NVDA Correlation with Others (2019–2024)
```
TSLA     0.5014
META     0.5518
GOOGL    0.6285
MSFT     0.7072
```

All correlations are above 0.5, confirming these five stocks move broadly together
as part of the wider technology sector — when rates rise or risk sentiment falls,
all five tend to sell off together.

TSLA shows the lowest correlation with NVDA (0.50), reflecting its additional exposure
to the EV industry, energy storage, and consumer sentiment around Elon Musk — factors
unrelated to the AI infrastructure cycle.

MSFT is most correlated with NVDA (0.71), likely because both companies are deeply
embedded in the same AI infrastructure stack: NVDA supplies the GPUs, MSFT runs them
in Azure and deploys them through OpenAI's products.

---

### Q3: Most Resilient During the 2022 Crash

2022 was defined by aggressive Federal Reserve rate hikes to combat inflation. Rising
rates hit high-growth technology stocks particularly hard, as their valuations depend
heavily on discounting future cash flows.
```
MSFT    -0.3558
GOOGL   -0.4363
NVDA    -0.6270
TSLA    -0.7272
META    -0.7374
```

**MSFT held up best (-35.6%)**, supported by its diversified revenue streams across
cloud (Azure), productivity software (Office 365), and gaming — making it less
sensitive to pure growth-stock sentiment.

META was the worst performer (-73.7%), collapsing due to a combination of the
rate-hike environment, a sharp decline in digital advertising revenue, and investor
scepticism about its expensive metaverse strategy under Mark Zuckerberg.

NVDA, despite being the long-term winner of the group, still fell 62.7% in 2022 —
a reminder that even the highest-quality companies carry significant drawdown risk
during macro-driven sell-offs.

---

### Q4: Equal-Weight Portfolio vs NVDA (2019–2024)

An equal-weight portfolio allocates 20% of capital to each of the five stocks,
rebalanced daily. Its daily return is simply the average of the five individual returns.
```
                     Portfolio        NVDA
Ann. Return             0.4471      0.6718
Ann. Volatility         0.3539      0.5177
Sharpe Ratio            1.2633      1.2977
```

Holding NVDA alone delivered higher absolute returns (67.2% vs 44.7% annualised),
but the equal-weight portfolio achieved a nearly identical Sharpe Ratio (1.26 vs 1.30)
with significantly lower volatility (35.4% vs 51.8%).

This illustrates a core principle of portfolio construction: **diversification reduces
risk without proportionally reducing risk-adjusted returns**. An investor who held
the portfolio rather than concentrating in NVDA would have experienced far smaller
drawdowns while still capturing most of the risk-adjusted upside.

---

## Metrics Explained

**Daily Return**

$$r_t = \frac{P_t - P_{t-1}}{P_{t-1}}$$

The percentage change in closing price from one trading day to the next.

**Annualised Return**

$$\mu = \bar{r} \times 252$$

The average daily return scaled to a full trading year (252 trading days).

**Annualised Volatility**

$$\sigma = \text{std}(r) \times \sqrt{252}$$

The standard deviation of daily returns scaled to annual frequency.
Volatility scales with the square root of time, not linearly.

**Sharpe Ratio**

$$S = \frac{\mu}{\sigma}$$

Return per unit of risk. Assumes a risk-free rate of zero for simplicity.
A Sharpe Ratio above 1.0 is generally considered good; above 2.0 is excellent.

**Max Drawdown**

$$\text{MDD} = \min\left(\frac{P_t}{\max_{s \leq t}(P_s)} - 1\right)$$

The largest peak-to-trough decline over the period. Measures worst-case loss
for an investor who bought at the peak.

**Cumulative Return**

$$C_t = \prod_{i=1}^{t}(1 + r_i)$$

The compounded growth of $1 invested at the start date. Uses multiplication
rather than addition because returns compound — a 10% gain followed by a
10% loss does not return to the starting value.

---

## Libraries

| Library | Version | Purpose |
|---------|---------|---------|
| `yfinance` | latest | Download historical market data from Yahoo Finance |
| `pandas` | latest | DataFrame manipulation, time series operations |
| `matplotlib` | latest | Chart generation and styling |
| `seaborn` | latest | Statistical visualisation (heatmaps) |
| `python-dateutil` | latest | Flexible date string parsing |
