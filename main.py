import yfinance as yf
import numpy as np
import pandas as pd

pd.set_option('display.max_rows', 1000)
pd.set_option('display.max_columns', 20)

companies = pd.read_csv('inputs_files/Yahoo_Company_codes.csv')
# Dropping Description column is all values are null
if companies.Description.notnull().sum() == 0: companies.drop('Description', axis=1, inplace=True)

"""Rules for Calculation"""
period = '12mo'  # time frame of data to get for calculation of RSI
RSI_buy_sell = [25, 75]  # SELL if less than 25 buy when more than 75
VOL_RATIO_buy_sell = 3  # BUY/SELL when volume ratio is more than 3


def get_current_rsi(comp_cd):
    yahoo_ticker = yf.Ticker(comp_cd)
    ticker_last_X_days = yahoo_ticker.history(period=period)[['Close']]
    # ticker_live = yahoo_ticker.info['ask']
    ticker_last_X_days['Change'] = ticker_last_X_days.Close.rolling(2).apply(lambda x: x[-1] - x[0])
    ticker_last_X_days['Upward_movement'] = ticker_last_X_days.Change.apply(lambda x: x if x > 0 else 0)
    ticker_last_X_days['Downward_movement'] = ticker_last_X_days.Change.apply(lambda x: -x if x < 0 else 0)
    up_mean = ticker_last_X_days.Upward_movement[:14].mean()
    down_mean = ticker_last_X_days.Downward_movement[:14].mean()
    ticker_last_X_days['Avg_upward_movement'] = None
    ticker_last_X_days['Avg_downward_movement'] = None
    avg_mov_updater(ticker_last_X_days, up_mean, down_mean)
    ticker_last_X_days[
        'Relative_strength'] = ticker_last_X_days.Avg_upward_movement / ticker_last_X_days.Avg_downward_movement
    ticker_last_X_days['RSI'] = 100 - 100 / (ticker_last_X_days.Relative_strength + 1)
    return ticker_last_X_days.RSI[-1]


def avg_mov_updater(df, upavg, downavg):
    new_upavg = upavg
    new_downavg = downavg
    up_to_be_updated = df.Upward_movement[14:]
    down_to_be_updated = df.Downward_movement[14:]
    up_updated = [None] * 13 + [new_upavg]
    down_updated = [None] * 13 + [new_downavg]

    for i, j in zip(up_to_be_updated, down_to_be_updated):
        new_upavg = (new_upavg * 13 + i) / 14
        new_downavg = (new_downavg * 13 + j) / 14
        up_updated.append(new_upavg)
        down_updated.append(new_downavg)

    df['Avg_upward_movement'] = up_updated
    df['Avg_downward_movement'] = down_updated


# def get_beta(comp_cd):
# try :
#     return yf.Ticker(comp_cd).info['beta']
# except :
#     return ''

def volume(comp_cd):
    yahoo_ticker = yf.Ticker(comp_cd)
    volumes = np.array(yahoo_ticker.history()[['Volume']][-2:])
    return float(volumes[-1] / volumes[-2])


print('Querying for a very long list will take a minute or two\n')

print('Calculating RSI\'s')
companies['RSI'] = companies.YahooCD.apply(get_current_rsi)
# companies['beta'] = companies.YahooCD.apply(get_beta)
print('Calculating buy/sell on RSI')
companies['Buy/Sell'] = companies.RSI.apply(
    lambda x: 'BUY' if x < RSI_buy_sell[0] else ('SELL' if x > RSI_buy_sell[1] else ''))
print('Calculating Volume Ratio')
companies['vol_Ratio'] = companies.YahooCD.apply(volume)
print('Calculating buy/sell on Volume Ratio')
companies['VR Purchase'] = companies.vol_Ratio.apply(lambda x: 'BUY/SELL' if x > VOL_RATIO_buy_sell else '')
print('Done')
print(companies)
