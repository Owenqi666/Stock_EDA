# Stock EDA

Exploratory data analysis of stock market data using Python.
Two components: an interactive analysis tool and a deep dive into AI-related stocks.

---

## Part 1: Interactive Analysis Tool (`stock_eda.py`)

Enter any tickers and date range — the tool downloads historical data,
computes key financial metrics, and generates four charts automatically.

### How to Run
```bash
pip install -r requirements.txt
python3 stock_eda.py
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

Accepts flexible date formats: `2020-01-01`, `Jan 1 2020`, `2020/01/01` etc.

### Input Validation

- Tickers must be letters only (e.g. `AAPL`, not `AA11`)
- End date must be after start date
- Invalid or delisted tickers are flagged before download

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
| `return_hist.png` | Daily return distribution histogram |
| `correlation.png` | Correlation matrix heatmap |
| `cumulative_returns.png` | Cumulative growth of $1 invested |

---

## Part 2: AI Stocks Deep Dive (`analysis.py`)

Fixed analysis of five AI-related stocks — NVDA, TSLA, MSFT, GOOGL, META —
over 2019–2024, answering four specific questions.
```bash
python3 analysis.py
```

### Stocks Analysed

| Ticker | Company | AI Relevance |
|--------|---------|--------------|
| NVDA | NVIDIA | GPU infrastructure for AI training |
| MSFT | Microsoft | Major investor in OpenAI |
| GOOGL | Alphabet | Investor in Anthropic, built Gemini |
| META | Meta | In-house AI research (LLaMA) |
| TSLA | Tesla | Autonomous driving, Dojo supercomputer |

### Q1: Best Risk-Adjusted Return (2019–2024)
```
         Ann. Return  Ann. Volatility  Sharpe Ratio  Max Drawdown
NVDA          0.6718           0.5177        1.2977       -0.6634
TSLA          0.7081           0.6470        1.0945       -0.7363
MSFT          0.3203           0.3049        1.0505       -0.3715
GOOGL         0.2460           0.3181        0.7733       -0.4432
META          0.2891           0.4363        0.6626       -0.7674
```

**NVDA had the best risk-adjusted return (Sharpe: 1.2977)**, despite not having
the highest raw return. TSLA had higher absolute returns but significantly more volatility.

### Q2: NVDA Correlation with Others
```
TSLA     0.5014
META     0.5518
GOOGL    0.6285
MSFT     0.7072
```

All correlations are above 0.5, confirming these stocks move together as part of
the broader tech sector. TSLA is the least correlated with NVDA (0.50), reflecting
its exposure to the EV industry rather than pure software/AI. MSFT is most correlated
(0.71), likely due to its deep integration with AI infrastructure via OpenAI.

### Q3: Most Resilient During the 2022 Crash
```
MSFT    -0.3558
GOOGL   -0.4363
NVDA    -0.6270
TSLA    -0.7272
META    -0.7374
```

**MSFT held up best in 2022 (-35.6%)**, while META collapsed -73.7% due to its
metaverse pivot and advertising revenue decline. NVDA, despite being the long-term
winner, still fell 62.7% during the rate-hike cycle — a reminder that high-growth
stocks carry significant downside risk.

### Q4: Equal-Weight Portfolio vs NVDA
```
                     Portfolio        NVDA
Ann. Return             0.4471      0.6718
Ann. Volatility         0.3539      0.5177
Sharpe Ratio            1.2633      1.2977
```

Holding NVDA alone gave higher returns, but the equal-weight portfolio achieved
a nearly identical Sharpe Ratio (1.26 vs 1.30) with significantly lower volatility
(35% vs 52%). This illustrates the core benefit of diversification: similar
risk-adjusted performance with less concentration risk.

---

## Metrics Explained

**Annualised Return**

$$\mu = \bar{r} \times 252$$

**Annualised Volatility**

$$\sigma = \text{std}(r) \times \sqrt{252}$$

**Sharpe Ratio**

$$S = \frac{\mu}{\sigma}$$

**Max Drawdown**

$$\text{MDD} = \min\left(\frac{P_t}{\max_{s \leq t}(P_s)} - 1\right)$$

**Daily Return**

$$r_t = \frac{P_t - P_{t-1}}{P_{t-1}}$$

**Cumulative Return**

$$C_t = \prod_{i=1}^{t}(1 + r_i)$$

## Libraries

- `yfinance` — market data download
- `pandas` — data manipulation
- `matplotlib` / `seaborn` — visualisation
- `python-dateutil` — flexible date parsing
