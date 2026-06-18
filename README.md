# Algorithmic Trading Backtester

A full-stack web application that simulates algorithmic trading strategies against historical stock data and compares performance against a buy-and-hold benchmark.

**Live demo:** coming soon

<img width="1015" height="587" alt="Screenshot 2026-06-18 at 11 35 36 AM" src="https://github.com/user-attachments/assets/bb395055-92b6-42c8-a68f-a031c228c6cc" />

## What it does

Enter any stock ticker, date range, starting capital, and trading strategy — the backtester simulates how that strategy would have performed historically and gives you a full breakdown of the results including a side-by-side comparison against simply buying and holding the stock.

## Strategies

**SMA Crossover** — buys when the 50-day moving average crosses above the 200-day moving average and sells when it crosses back below. A classic trend-following strategy.

**RSI (Relative Strength Index)** — buys when the stock is oversold (RSI below 30) and sells when it is overbought (RSI above 70). A mean-reversion approach.

**Bollinger Bands** — buys when price drops below the lower band and sells when it rises above the upper band. Captures volatility-based price movements.

## Performance Metrics

Each backtest produces the following metrics for both the strategy and buy-and-hold benchmark:

- Total return
- Annualized return
- Sharpe ratio (risk-adjusted return)
- Max drawdown (worst peak-to-trough decline)
- Final portfolio value

## Tech Stack

Python · Flask · pandas · NumPy · Chart.js · Bootstrap · Yahoo Finance API

## Quick Start

```bash
git clone https://github.com/D97v121/trading-backtester.git
cd trading-backtester
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
flask --app wsgi run --debug
```

Open `http://127.0.0.1:5000` in your browser.

## Project Structure

```
trading-backtester/
├── app/
│   ├── backtester/
│   │   ├── engine.py
│   │   └── strategies.py
│   ├── data/
│   │   └── fetcher.py
│   ├── routes/
│   │   └── main_routes.py
│   └── templates/
│       └── index.html
└── wsgi.py
```
