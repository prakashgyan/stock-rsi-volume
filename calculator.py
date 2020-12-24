import yfinance as yf
import numpy as np
import pandas as pd
from datetime import datetime, timedelta
import time
import timeit

pd.set_option('display.max_rows', 1000)
pd.set_option('display.max_columns', 20)

companies = pd.read_csv('Yahoo_Company_codes.csv')
# Dropping Description column is all values are null
if companies.Description.notnull().sum() == 0: companies.drop('Description', axis=1, inplace=True)

"""Rules for Calculation"""
# period = '1mo'  # time frame of data to get for calculation of RSI
# RSI_buy_sell = [25, 75]  # SELL if less than 25 buy when more than 75
# VOL_RATIO_buy_sell = 3  # BUY/SELL when volume ratio is more than 3
# timeofevent = datetime.now().strftime("%c")

yahoo_tickers = yf.Tickers(' '.join([x for x in companies.YahooCD.values]))

def get_current_rsi(yahoo_ticker, period='12mo'):
    # yahoo_ticker = yf.Ticker(comp_cd)
    ticker_last_X_days = yahoo_ticker.history(period=period)[['Close','Volume']]
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
    volumes = np.array(ticker_last_X_days.Volume[-2:])
    return ticker_last_X_days.RSI[-1], float(volumes[-1] / volumes[-2])


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



# print('Querying for a very long list will take a minute or two\n')

# companies['RSI'] = companies.YahooCD.apply(get_current_rsi)
# # companies['beta'] = companies.YahooCD.apply(get_beta)
# companies['Buy/Sell'] = companies.RSI.apply(
#     lambda x: 'BUY' if x < RSI_buy_sell[0] else ('SELL' if x > RSI_buy_sell[1] else '-'))
# companies['vol_Ratio'] = companies.YahooCD.apply(volume)
# companies['VR Purchase'] = companies.vol_Ratio.apply(lambda x: 'BUY/SELL' if x > VOL_RATIO_buy_sell else '-')
# companies.to_json('data_json.json')

# table = companies

def get_table(form_data, df = companies):
    # try:    
    RSI_buy_sell = [int(x) for x in form_data['rsi_buy_sell'].split(',') ]
    VOL_RATIO_buy_sell = int(form_data['vol_ratio_trigger'])
    period = form_data['period']
    # print(RSI_buy_sell,VOL_RATIO_buy_sell,period)
    # except :
    #     period = '1mo'  # time frame of data to get for calculation of RSI
    #     RSI_buy_sell = [25, 75]  # SELL if less than 25 buy when more than 75
    #     VOL_RATIO_buy_sell = 3  # BUY/SELL when volume ratio is more than 3
    rsi_volume = pd.DataFrame([get_current_rsi(ticker,period) for ticker in yahoo_tickers.tickers], columns=['RSI','Vol_Ratio']).reindex(df.index)
    df = pd.concat([df, rsi_volume],axis=1 )
    # df['RSI'] = df.YahooCD.apply(get_current_rsi)
    # # companies['beta'] = companies.YahooCD.apply(get_beta)
    df['Buy/Sell'] = df.RSI.apply(
        lambda x: 'BUY' if x < RSI_buy_sell[0] else ('SELL' if x > RSI_buy_sell[1] else '-'))
    # df['vol_Ratio'] = df.YahooCD.apply(volume)
    df = df[['YahooCD','RSI','Buy/Sell','Vol_Ratio']]
    df['VR Purchase'] = df.Vol_Ratio.apply(lambda x: 'BUY/SELL' if x > VOL_RATIO_buy_sell else '-')
    # # companies.to_json('data_json.json')
    timeofevent = datetime.utcnow() + timedelta(hours=5,minutes=30)
    return df , f'[IST] {timeofevent.strftime("%c")}', [period,str(RSI_buy_sell)[1:-1],VOL_RATIO_buy_sell]

# if __name__ == '__main__':
#     timea = time.time()
#     print(get_table())
#     print(f'Total Time taken : {time.time()-timea}')    