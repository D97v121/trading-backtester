import pandas as pd
import numpy as np

class Backtester:
    def __init__(self, df, strategy_fn, starting_capital=10000):
        # Store the price data, strategy function, and starting capital
        self.df = df.copy()
        self.strategy_fn = strategy_fn
        self.starting_capital = starting_capital

    def run(self):
        # Work on a copy so we don't modify the original data
        df = self.df.copy()

        # Flatten MultiIndex columns that yfinance sometimes returns
        if isinstance(df.columns, pd.MultiIndex):
            df.columns = df.columns.get_level_values(0)

        df['Close'] = pd.to_numeric(df['Close'], errors='coerce')

        # Apply the strategy to generate buy/sell signals
        df = self.strategy_fn(df)

        # Initialize portfolio state
        cash = self.starting_capital
        shares = 0
        portfolio_values = []
        trades = []

        # Step through each day chronologically
        for i, row in df.iterrows():
            price = row['Close']
            signal = row.get('signal', 0)

            # Buy signal — spend all cash on shares
            if signal == 1 and cash > 0:
                shares = cash / price
                cash = 0
                trades.append({'date': i, 'action': 'BUY', 'price': price, 'shares': shares})

            # Sell signal — convert all shares back to cash
            elif signal == -1 and shares > 0:
                cash = shares * price
                trades.append({'date': i, 'action': 'SELL', 'price': price, 'shares': shares})
                shares = 0

            # Record total portfolio value for this day
            portfolio_value = cash + (shares * price)
            portfolio_values.append({'date': i, 'value': portfolio_value})

        # Convert lists to DataFrames for easy analysis
        results_df = pd.DataFrame(portfolio_values).set_index('date')
        trades_df = pd.DataFrame(trades)

        return {
            'portfolio': results_df,
            'trades': trades_df,
            'metrics': self._calculate_metrics(results_df)
        }

    def _calculate_metrics(self, portfolio_df):
        # Extract the series of daily portfolio values
        values = portfolio_df['value']

        # Total return as a percentage
        total_return = (values.iloc[-1] - self.starting_capital) / self.starting_capital * 100

        # Daily returns for volatility and Sharpe calculation
        daily_returns = values.pct_change().dropna()

        # Sharpe ratio — annualized risk-adjusted return (252 trading days/year)
        sharpe = (daily_returns.mean() / daily_returns.std()) * np.sqrt(252) if daily_returns.std() != 0 else 0

        # Max drawdown — largest peak-to-trough drop
        rolling_max = values.cummax()
        drawdown = (values - rolling_max) / rolling_max
        max_drawdown = drawdown.min() * 100

        # Annualized return accounts for the length of the backtest period
        annualized_return = ((values.iloc[-1] / self.starting_capital) ** (252 / len(values)) - 1) * 100

        return {
            'total_return': round(total_return, 2),
            'annualized_return': round(annualized_return, 2),
            'sharpe_ratio': round(sharpe, 2),
            'max_drawdown': round(max_drawdown, 2),
            'final_value': round(values.iloc[-1], 2)
        }