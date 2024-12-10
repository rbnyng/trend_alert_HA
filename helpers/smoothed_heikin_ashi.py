import pandas as pd

def heikin_ashi_color(haOpen, haClose):
    if isinstance(haOpen, (int, float)) and isinstance(haClose, (int, float)):
        if haClose > haOpen:
            return 'green'
        elif haClose < haOpen:
            return 'red'
        else:
            return '?'
    else:
        raise ValueError("haOpen and haClose must be scalar values for each row.")

def calculate_smoothed_heikin_ashi(data, period=20):
    """
    Calculate Heikin-Ashi values (Open, Close, Low, High) based on Exponential Moving Averages (EMAs)
    of the original Open, Close, Low, and High prices over the specified period.

    Args:
    - data (pd.DataFrame): DataFrame containing 'Open', 'Close', 'High', 'Low' columns.
    - period (int): Period over which to calculate the EMAs.

    Returns:
    - pd.DataFrame: Original DataFrame with added columns for Heikin-Ashi values and EMAs.
    """
    # Calculate EMAs
    data['openMA'] = data['Open'].ewm(span=period, adjust=False).mean()
    data['closeMA'] = data['Close'].ewm(span=period, adjust=False).mean()
    data['highMA'] = data['High'].ewm(span=period, adjust=False).mean()
    data['lowMA'] = data['Low'].ewm(span=period, adjust=False).mean()

    # Calculate haClose
    data['haClose'] = (data['openMA'] + data['highMA'] + data['lowMA'] + data['closeMA']) / 4.0

    # Initialize haOpen using the same logic as haClose for the first row
    data['haOpen'] = data['haClose'].copy()  # Start with haOpen equal to haClose

    # Compute haOpen using a loop for subsequent rows
    for i in range(1, len(data)):
        data.loc[i, 'haOpen'] = (data.loc[i - 1, 'haOpen'] + data.loc[i - 1, 'haClose']) / 2.0

    # Calculate haLow and haHigh
    data['haLow'] = data[['lowMA', 'haOpen', 'haClose']].min(axis=1)
    data['haHigh'] = data[['highMA', 'haOpen', 'haClose']].max(axis=1)

    # Calculate HA_Color
    data['HA_Color'] = data.apply(lambda row: heikin_ashi_color(row['haOpen'], row['haClose']), axis=1)

    return data

if __name__ == "__main__":
    print("This script is intended to be imported as a module and not run directly.")