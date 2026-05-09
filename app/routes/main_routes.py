from flask import Blueprint, render_template, request, jsonify
from app.data.fetcher import fetch_data
from app.backtester.engine import Backtester
from app.backtester.strategies import sma_crossover, rsi_strategy, bollinger_bands
import pandas as pd

main_bp = Blueprint('main', __name__)

STRATEGIES = {
    'sma_crossover': sma_crossover,
    'rsi': rsi_strategy,
    'bollinger_bands': bollinger_bands
}

@main_bp.route('/')
def index():
    return render_template('index.html')

@main_bp.route('/run', methods=['POST'])
def run_backtest():
    data = request.get_json()

    ticker = data.get('ticker', 'AAPL').upper()
    start_date = data.get('start_date', '2020-01-01')
    end_date = data.get('end_date', '2023-01-01')
    strategy_name = data.get('strategy', 'sma_crossover')
    starting_capital = float(data.get('starting_capital', 10000))

    strategy_fn = STRATEGIES.get(strategy_name)
    if not strategy_fn:
        return jsonify({'error': 'Invalid strategy'}), 400

    try:
        df = fetch_data(ticker, start_date, end_date)
        bt = Backtester(df, strategy_fn, starting_capital)
        results = bt.run()

        portfolio = results['portfolio'].reset_index()
        portfolio['date'] = portfolio['date'].astype(str)
        portfolio['value'] = portfolio['value'].fillna(0)

        trades = results['trades']
        if not trades.empty:
            trades['date'] = trades['date'].astype(str)
            trades_list = trades.to_dict(orient='records')
        else:
            trades_list = []

        # Flatten MultiIndex if needed and calculate buy and hold benchmark
        bh_df = df.copy()
        if isinstance(bh_df.columns, pd.MultiIndex):
            bh_df.columns = bh_df.columns.get_level_values(0)
        bh_close = pd.to_numeric(bh_df['Close'], errors='coerce')

        print(f"bh_close head: {bh_close.head()}")
        print(f"bh_close dtype: {bh_close.dtype}")
        print(f"first_price type: {type(bh_close.iloc[0])}")
        print(f"first_price value: {bh_close.iloc[0]}")

        first_price = bh_close.iloc[0]
        shares_bh = starting_capital / first_price

        buy_and_hold = []
        for date, price in bh_close.items():
            value = shares_bh * price
            buy_and_hold.append({'date': str(date), 'value': round(float(value), 2) if not pd.isna(value) else 0})

        return jsonify({
            'metrics': {k: float(v) if not pd.isna(v) else 0 for k, v in results['metrics'].items()},
            'portfolio': portfolio.to_dict(orient='records'),
            'trades': trades_list,
            'buy_and_hold': buy_and_hold
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500