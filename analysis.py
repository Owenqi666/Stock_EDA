import yfinance as yf
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns
import os

#Setup
TICKERS = ['NVDA', 'TSLA', 'MSFT', 'GOOGL', 'META']
START = '2019-01-01'
END   = '2024-01-01'

#Download data
print("Downloading data...")
data = yf.download(TICKERS, start=START, end=END)
prices = data['Close']
prices.dropna(inplace=True)
returns = prices.pct_change().dropna()

os.makedirs('images', exist_ok=True)
print(f"Data loaded: {prices.shape[0]} trading days\n")

#Topic1: Best risk-adjusted return (Sharpe Ratio)
ann_ret  = returns.mean() * 252
ann_vol  = returns.std() * (252 ** 0.5)
sharpe   = ann_ret / ann_vol
drawdown = (prices / prices.cummax() - 1).min()

stats = pd.DataFrame({
    'Ann. Return':     ann_ret,
    'Ann. Volatility': ann_vol,
    'Sharpe Ratio':    sharpe,
    'Max Drawdown':    drawdown
}).round(4)

print("── Q1: Risk-Adjusted Performance ─────────────")
print(stats.sort_values('Sharpe Ratio', ascending=False))
best = stats['Sharpe Ratio'].idxmax()
print(f"\nBest risk-adjusted return: {best} (Sharpe: {stats.loc[best, 'Sharpe Ratio']:.4f})")

#Topic2: NVDA correlation with others
corr = returns.corr()

print("\n── Q2: NVDA Correlation with Others ──────────")
print(corr['NVDA'].drop('NVDA').sort_values())

least_corr = corr['NVDA'].drop('NVDA').idxmin()
most_corr  = corr['NVDA'].drop('NVDA').idxmax()
print(f"\nMost correlated with NVDA:  {most_corr} ({corr.loc['NVDA', most_corr]:.4f})")
print(f"Least correlated with NVDA: {least_corr} ({corr.loc['NVDA', least_corr]:.4f})")

# Heatmap
fig, ax = plt.subplots(figsize=(8, 6))
sns.heatmap(corr, annot=True, fmt='.2f', cmap='coolwarm', ax=ax)
ax.set_title('Correlation Matrix (2019–2024)')
plt.tight_layout()
plt.savefig('images/correlation_analysis.png')
plt.close()
print("Saved: images/correlation_analysis.png")

# ── Q3: 2022 drawdown analysis ─────────────────
prices_2022  = prices.loc['2022-01-01':'2022-12-31']
returns_2022 = returns.loc['2022-01-01':'2022-12-31']
drawdown_2022 = (prices_2022 / prices_2022.cummax() - 1).min()

print("\n── Q3: Max Drawdown During 2022 Crash ─────────")
print(drawdown_2022.sort_values(ascending=False).round(4))
most_resilient = drawdown_2022.idxmax()
print(f"\nMost resilient in 2022: {most_resilient} (Max Drawdown: {drawdown_2022[most_resilient]:.4f})")

# Plot: 2022 cumulative returns
fig, ax = plt.subplots(figsize=(14, 5))
cumulative_2022 = (1 + returns_2022).cumprod()
for ticker in TICKERS:
    ax.plot(cumulative_2022[ticker], label=ticker, alpha=0.8)
ax.set_title('Cumulative Returns During 2022 Crash')
ax.set_xlabel('Date')
ax.set_ylabel('Growth of $1')
ax.legend()
plt.tight_layout()
plt.savefig('images/drawdown_2022.png')
plt.close()
print("Saved: images/drawdown_2022.png")

#Q4: Equal-weight portfolio vs NVDA
portfolio_returns = returns.mean(axis=1)  # average across all 5 tickers each day

port_ann_ret = portfolio_returns.mean() * 252
port_ann_vol = portfolio_returns.std() * (252 ** 0.5)
port_sharpe  = port_ann_ret / port_ann_vol

nvda_ann_ret = ann_ret['NVDA']
nvda_ann_vol = ann_vol['NVDA']
nvda_sharpe  = sharpe['NVDA']

print("\n── Q4: Equal-Weight Portfolio vs NVDA ─────────")
print(f"{'':20} {'Portfolio':>12} {'NVDA':>12}")
print(f"{'Ann. Return':20} {port_ann_ret:>12.4f} {nvda_ann_ret:>12.4f}")
print(f"{'Ann. Volatility':20} {port_ann_vol:>12.4f} {nvda_ann_vol:>12.4f}")
print(f"{'Sharpe Ratio':20} {port_sharpe:>12.4f} {nvda_sharpe:>12.4f}")

# Plot: portfolio vs NVDA cumulative returns
fig, ax = plt.subplots(figsize=(14, 5))
ax.plot((1 + portfolio_returns).cumprod(), label='Equal-Weight Portfolio', linewidth=2)
ax.plot((1 + returns['NVDA']).cumprod(),   label='NVDA', linewidth=2, linestyle='--')
ax.set_title('Equal-Weight Portfolio vs NVDA (2019–2024)')
ax.set_xlabel('Date')
ax.set_ylabel('Growth of $1')
ax.legend()
plt.tight_layout()
plt.savefig('images/portfolio_vs_nvda.png')
plt.close()
print("Saved: images/portfolio_vs_nvda.png")

print("\nAnalysis complete.")