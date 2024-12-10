import pandas as pd

def apply_labels(df):
    df_copy = df.copy()
    
    df_copy['Alert'] = ''
    df_copy['Market_Condition'] = ''  
    
    # Determine market condition (Vectorized)
    bear_condition = (df_copy['haClose'] < df_copy['EMA_50']) & (df_copy['haClose'] < df_copy['EMA_200'])
    bull_condition = (df_copy['haClose'] > df_copy['EMA_50']) & (df_copy['haClose'] > df_copy['EMA_200'])
    sideways_condition = ~bear_condition & ~bull_condition  # Not bear and not bull

    df_copy.loc[bear_condition, 'Market_Condition'] = 'Bear'
    df_copy.loc[bull_condition, 'Market_Condition'] = 'Bull'
    df_copy.loc[sideways_condition, 'Market_Condition'] = 'Sideways'

    # --- Apply alerts based on market condition (Vectorized) ---

    # Bear Market Alerts
    long_alert_bear = bear_condition & (df_copy['HA_Color'] == 'green') & df_copy['HMA_color'].isin(['green', 'dark_green'])
    sell_alert_bear = bear_condition & (df_copy['HMA_color'].isin(['dark_orange', 'red']) | (df_copy['HA_Color'] == 'red'))

    df_copy.loc[long_alert_bear, 'Alert'] = 'Long Alert'
    df_copy.loc[sell_alert_bear, 'Alert'] = 'Sell Alert'

    # Bull Market Alerts
    long_alert_bull = bull_condition & (df_copy['HA_Color'] == 'green') & df_copy['HMA_color'].isin(['green', 'dark_green'])
    sell_alert_bull = bull_condition & ((df_copy['HMA_color'] == 'red') | (df_copy['HA_Color'] == 'red'))
    orange_hma_alert_bull = bull_condition & (df_copy['HMA_color'] == 'dark_orange')

    df_copy.loc[long_alert_bull, 'Alert'] = 'Long Alert'
    df_copy.loc[sell_alert_bull, 'Alert'] = 'Sell Alert'
    df_copy.loc[orange_hma_alert_bull, 'Alert'] = 'Orange HMA Alert'
    
    # Sideways Market Alerts
    long_alert_sideways = sideways_condition & (df_copy['HA_Color'] == 'green') & df_copy['HMA_color'].isin(['green', 'dark_green'])
    sell_alert_sideways = sideways_condition & (df_copy['HMA_color'].isin(['dark_orange', 'red']) | (df_copy['HA_Color'] == 'red'))

    df_copy.loc[long_alert_sideways, 'Alert'] = 'Long Alert'
    df_copy.loc[sell_alert_sideways, 'Alert'] = 'Sell Alert'

    return df_copy