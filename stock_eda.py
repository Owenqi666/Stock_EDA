import yfinance as yf
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
import os
from dateutil import parser as dateparser

def parse_date(prompt):
    date_str = input(prompt).strip()
    try:
        dt = dateparser.parse(date_str)
        return dt, dt.strftime('%Y-%m-%d')
    
    except Exception:
        print("Error: cannot recognise date format")
        exit()

def main():

    # User input
    tickers = input("Enter tickers (e.g. AAPL MSFT TSLA):\n> ").strip().upper().split()

    for ticker in tickers:
        if not ticker.isalpha():
            print(f"Error: invalid ticker '{ticker}', letters only")
            exit()

    start_dt, start_date = parse_date("Start date:\n> ")
    end_dt, end_date = parse_date("End date:\n> ")

    if end_dt <= start_dt:
        print("Error: end date must be after start date")
        exit()

    # Download data
    try:
        data = yf.download(tickers, start=start_date, end=end_date)

        if data.empty:
            raise ValueError("No data returned. Check your tickers and dates.")

        prices = data['Close']
        prices.dropna(inplace=True)

        missing = [t for t in tickers if t not in prices.columns]
        if missing:
            raise ValueError(f"Tickers not found: {missing}")

    except ValueError as e:
        print(f"Error: {e}")
        exit()
    except Exception as e:
        print(f"Unexpected error: {e}")
        exit()

    # Calculate returns
    returns = prices.pct_change().dropna()

    # Calculate statistics
    ann_ret  = returns.mean() * 252
    ann_vol  = returns.std() * (252 ** 0.5)
    sharpe   = ann_ret / ann_vol
    drawdown = (prices / prices.cummax() - 1).min()

    stats = pd.DataFrame({
        'Ann. Return':     ann_ret,
        'Ann. Volatility': ann_vol,
        'Sharpe Ratio':    sharpe,
        'Max Drawdown':    drawdown
    })

    print("\nPortfolio Statistics:\n")
    print(stats.round(4))

    # Plot 1: Closing prices + moving averages
    os.makedirs('images', exist_ok=True)
    fig, ax = plt.subplots(figsize=(14, 5))
    for ticker in tickers:
        ax.plot(prices[ticker], label=ticker, alpha=0.8)
        ax.plot(prices[ticker].rolling(20).mean(),
                linestyle='--', linewidth=1, alpha=0.6, label=f'{ticker} MA20')
        ax.plot(prices[ticker].rolling(50).mean(),
                linestyle=':',  linewidth=1, alpha=0.6, label=f'{ticker} MA50')
    ax.set_title('Stock Closing Prices with Moving Averages')
    ax.set_xlabel('Date')
    ax.set_ylabel('Price (USD)')
    ax.legend(fontsize=7)
    plt.tight_layout()
    plt.savefig('images/price_chart.png')
    plt.close()
    print("Saved: images/price_chart.png")

    # Plot 2: Daily return distribution
    fig, ax = plt.subplots(figsize=(14, 5))
    for ticker in tickers:
        ax.hist(returns[ticker], bins=50, alpha=0.5, label=ticker)
    ax.set_title('Daily Return Distribution')
    ax.set_xlabel('Daily Return')
    ax.set_ylabel('Frequency')
    ax.legend()
    plt.tight_layout()
    plt.savefig('images/return_hist.png')
    plt.close()
    print("Saved: images/return_hist.png")

    # Plot 3: Correlation heatmap
    fig, ax = plt.subplots(figsize=(8, 6))
    sns.heatmap(returns.corr(), annot=True, fmt='.2f', cmap='coolwarm', ax=ax)
    ax.set_title('Correlation Matrix')
    plt.tight_layout()
    plt.savefig('images/correlation.png')
    plt.close()
    print("Saved: images/correlation.png")

    # Plot 4: Cumulative returns
    fig, ax = plt.subplots(figsize=(14, 5))
    cumulative = (1 + returns).cumprod()
    for ticker in tickers:
        ax.plot(cumulative[ticker], label=ticker, alpha=0.8)
    ax.set_title('Cumulative Returns')
    ax.set_xlabel('Date')
    ax.set_ylabel('Growth of $1')
    ax.legend()
    plt.tight_layout()
    plt.savefig('images/cumulative_returns.png')
    plt.close()
    print("Saved: images/cumulative_returns.png")

    print("\nDone! All charts saved to images/")

if __name__ == '__main__':
    main()
