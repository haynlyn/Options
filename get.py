import yfinance as  yf
import datetime
import json
import pytz
import os
import extract_config as ec

EST_TIMEZONE = pytz.timezone('America/New_York')
DOWNLOAD_DIRS = ec.DOWNLOAD_DIR

os.makedirs(DOWNLOAD_DIRS, exist_ok=True)

# ticker = 'djt'
tickers = [
           'djt', # lol
           'googl', 'aapl', # tech stocks
           'voo', 'voog',   # ETFs
           ]

def iso_to_mine(isoformatstr):
    date, time = isoformatstr.split('T')
    time = time.replace(':', '.').replace('.', '-')
    return '--'.join([date, time])

# ytickers = yf.Tickers(tickers)
def get_options_data(ticker, date):
    now = datetime.datetime.now()
    data = ticker.option_chain(date)
    return now, data

def main():
    for symbol in tickers:
        ticker = yf.Ticker(symbol)
        options_exp_dates = ticker.options

        for date in options_exp_dates:
            try:
                print(f"Downloading {symbol}@{date} option data.")
                now, data = get_options_data(ticker, date)
                ts = now.timestamp()
                tzname = now.tzname()
                calls, puts, underlying = data
    
                # filename = f"{symbol}@{date}_{iso_to_mine(now.isoformat())}.json"

                filename_prefix = f"{symbol}@{date}_{iso_to_mine(now.isoformat())}"

                calls.to_csv(DOWNLOAD_DIRS/f"{filename_prefix}_calls.csv")
                puts.to_csv(DOWNLOAD_DIRS/f"{filename_prefix}_puts.csv")
            except Exception as e:
                print(e)

        try:
            to_save = {'ts': ts, 'tz': tzname,
                       'symbol': symbol, 'exp_date': date,
                        # 'calls': calls.to_dict(),
                        # 'puts': puts.to_dict(),
                        'underlying': underlying}

            with open(DOWNLOAD_DIRS/f"{filename_prefix}_stock.json", 'w') as wf:
                json.dump(to_save, wf)

        except Exception as e:
            print(e)

if __name__ == "__main__":
    main()
