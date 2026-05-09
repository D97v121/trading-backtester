import pandas as pd

def sma_crossover(df, short_window=50, long_window=200):
    """
    Buy when short-term moving average crosses above long-term moving average.
    Sell when it crosses back below.
    """
    df = df.copy()
    df['Close'] = pd.to_numeric(df['Close'], errors='coerce')

    # Calculate moving averages
    df['sma_short'] = df['Close'].rolling(window=short_window).mean()
    df['sma_long'] = df['Close'].rolling(window=long_window).mean()

    # Generate signals on crossover points only
    df['signal'] = 0
    df.loc[df['sma_short'] > df['sma_long'], 'position'] = 1
    df.loc[df['sma_short'] <= df['sma_long'], 'position'] = 0
    df['signal'] = df['position'].diff()
    df.loc[df['signal'] > 0, 'signal'] = 1
    df.loc[df['signal'] < 0, 'signal'] = -1

    return df


def rsi_strategy(df, period=14, oversold=30, overbought=70):
    """
    Buy when RSI drops below oversold threshold.
    Sell when RSI rises above overbought threshold.
    """
    df = df.copy()
    df['Close'] = pd.to_numeric(df['Close'], errors='coerce')

    # Calculate RSI
    delta = df['Close'].diff()
    gain = delta.where(delta > 0, 0).rolling(window=period).mean()
    loss = -delta.where(delta < 0, 0).rolling(window=period).mean()
    rs = gain / loss
    df['rsi'] = 100 - (100 / (1 + rs))

    # Generate signals
    df['signal'] = 0
    df.loc[df['rsi'] < oversold, 'signal'] = 1
    df.loc[df['rsi'] > overbought, 'signal'] = -1

    return df


def bollinger_bands(df, window=20, num_std=2):
    """
    Buy when price drops below lower Bollinger Band.
    Sell when price rises above upper Bollinger Band.
    """
    df = df.copy()
    df['Close'] = pd.to_numeric(df['Close'], errors='coerce')

    # Calculate bands
    df['sma'] = df['Close'].rolling(window=window).mean()
    df['std'] = df['Close'].rolling(window=window).std()
    df['upper_band'] = df['sma'] + (num_std * df['std'])
    df['lower_band'] = df['sma'] - (num_std * df['std'])

    # Generate signals
    df['signal'] = 0
    df.loc[df['Close'] < df['lower_band'], 'signal'] = 1
    df.loc[df['Close'] > df['upper_band'], 'signal'] = -1

    return df