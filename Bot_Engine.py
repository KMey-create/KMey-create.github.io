import time

import MetaTrader5 as Mt
import pandas as pd
# import plotly.express as px
#import plotly.graph_objects as go
import random
import logging
import json
from datetime import datetime

Mt.initialize()
id = "5524535"
pw = "UqXHi9mm"
server = "FxPro-MT5"
Mt.login(id, pw, server)


with open("volume_results", "r") as f:
    y = f.read()



symbols = Mt.symbols_get()
num_symbols = Mt.symbols_total()



request = {
    "action": Mt.TRADE_ACTION_DEAL,
    "symbol": "x",
    "volume": 0,
    "type": Mt.ORDER_TYPE_SELL,
}


orders = {}  # tokens
lots = json.loads(y) #volume
results = {} # order numbers
triggers = {}
banned_tickers = []


### Logger  ###
today = datetime.today()
filename = f"{today.month:02d}-{today.day:02d}-{today.year}.log"
loger = logging.getLogger('JustALogger')
formatter = logging.Formatter('%(asctime)s: %(levelname)s - %(message)s')

logging.basicConfig(level=logging.INFO)

filehandler = logging.FileHandler(filename)

filehandler.setFormatter(formatter)
loger.addHandler(filehandler)

### Logger  ###

def structure(symbol):
    price_ = 0
    percentage = 0
    global token
    token = 0
    global trigger
    trigger = 0
    try:
        for i in range(28, len(ohlc_data) - 1):

            if token == 0 and ohlc_data['chikou_span'][i-26] < ohlc_data['tenkan_sen'][i-26] and ohlc_data['chikou_span'][i-26] < ohlc_data['senkou_span_a'][i-26] and  ohlc_data['chikou_span'][i-26] < ohlc_data['senkou_span_b'][i-26] and ohlc_data['open'][i] < ohlc_data['senkou_span_b'][i-26]:
#                 ohlc_data['Sell'][i] = ohlc_data['chikou_span'][i - 26]
                price_ = ohlc_data['open'].iloc[i]
                token = -1
                trigger = 1

            elif not token == -1 and trigger == 1 and ohlc_data['chikou_span'][i-26] < ohlc_data['tenkan_sen'][i-26] and ohlc_data['chikou_span'][i-26] < ohlc_data['senkou_span_a'][i-26] and  ohlc_data['chikou_span'][i-26] < ohlc_data['senkou_span_b'][i-26] and ohlc_data['open'][i] < ohlc_data['senkou_span_b'][i-26]:
#                 ohlc_data['Sell'][i] = ohlc_data['chikou_span'][i - 26]
                if price_ > ohlc_data['open'].iloc[i]:
                    percentage += ((ohlc_data['open'].iloc[i] / price_) * 100 ) - 100
                    price_ = ohlc_data['open'].iloc[i]
                else:
                    percentage += ((ohlc_data['open'].iloc[i] / price_) * 100) - 100
                    price_ = ohlc_data['open'].iloc[i]

                token = -1
                trigger = 1

            elif token == -1 and trigger == 1 and ohlc_data['chikou_span'][i-26] > ohlc_data['kijun_sen'][i-26]:

#               ohlc_data['Buy'][i] = ohlc_data['chikou_span'][i - 26]
                if price_ > ohlc_data['open'].iloc[i]:
                    percentage += (-1) * (((ohlc_data['open'].iloc[i] / price_) * 100 ) - 100)
                    price_ = ohlc_data['open'].iloc[i]
                else:
                    percentage += (-1) * (((ohlc_data['open'].iloc[i] / price_) * 100) - 100)
                    price_ = ohlc_data['open'].iloc[i]

                token = -1
                trigger = 0

            elif token == -1 and trigger == 0 and ohlc_data['chikou_span'][i-26] < ohlc_data['tenkan_sen'][i-26] and ohlc_data['chikou_span'][i-26] < ohlc_data['senkou_span_a'][i-26] and  ohlc_data['chikou_span'][i-26] < ohlc_data['senkou_span_b'][i-26]:
#                 ohlc_data['Sell'][i] = ohlc_data['chikou_span'][i - 26]
                if price_ > ohlc_data['open'].iloc[i]:
                    percentage += ((ohlc_data['open'].iloc[i] / price_) * 100 ) - 100
                    price_ = ohlc_data['open'].iloc[i]
                else:
                    percentage += ((ohlc_data['open'].iloc[i] / price_) * 100) - 100
                    price_ = ohlc_data['open'].iloc[i]

                token = -1
                trigger = 1

            elif not token == 1 and trigger == 1 and ohlc_data['chikou_span'][i-26] > ohlc_data['tenkan_sen'][i-26] and ohlc_data['chikou_span'][i-26] > ohlc_data['senkou_span_a'][i-26] and  ohlc_data['chikou_span'][i-26] > ohlc_data['senkou_span_b'][i-26] and ohlc_data['open'][i] > ohlc_data['senkou_span_b'][i-26]:
#                ohlc_data['Buy'][i] = ohlc_data['chikou_span'][i - 26]
                if price_ > ohlc_data['open'].iloc[i]:
                    percentage += (-1) * (((ohlc_data['open'].iloc[i] / price_) * 100 ) - 100)
                    price_ = ohlc_data['open'].iloc[i]
                else:
                    percentage += (-1) * (((ohlc_data['open'].iloc[i] / price_) * 100) - 100)
                    price_ = ohlc_data['open'].iloc[i]


                token = 1
                trigger = 1

            elif token == 1 and trigger == 1 and ohlc_data['chikou_span'][i-26] < ohlc_data['kijun_sen'][i-26]:
#                 ohlc_data['Sell'][i] = ohlc_data['chikou_span'][i - 26]
                if price_ > ohlc_data['open'].iloc[i]:
                    percentage += ((ohlc_data['open'].iloc[i] / price_) * 100 ) - 100
                    price_ = ohlc_data['open'].iloc[i]
                else:
                    percentage += ((ohlc_data['open'].iloc[i] / price_) * 100) - 100
                    price_ = ohlc_data['open'].iloc[i]

                token = 1
                trigger = 0

            elif token == 1 and trigger == 0 and ohlc_data['chikou_span'][i-26] > ohlc_data['tenkan_sen'][i-26] and ohlc_data['chikou_span'][i-26] > ohlc_data['senkou_span_a'][i-26] and  ohlc_data['chikou_span'][i-26] > ohlc_data['senkou_span_b'][i-26]:
#                ohlc_data['Buy'][i] = ohlc_data['chikou_span'][i - 26]
                if price_ > ohlc_data['open'].iloc[i]:
                    percentage += (-1) * (((ohlc_data['open'].iloc[i] / price_) * 100 ) - 100)
                    price_ = ohlc_data['open'].iloc[i]
                else:
                    percentage += (-1) * (((ohlc_data['open'].iloc[i] / price_) * 100) - 100)
                    price_ = ohlc_data['open'].iloc[i]

                token = 1
                trigger = 1


            else:
                continue

        print(symbol, percentage,"%", Mt.symbol_info(symbol)._asdict()['path'][:5] == "Forex",  Mt.symbol_info(symbol)._asdict()['path'])
        orders[symbol] = int(token)
        lots[symbol] = float(Mt.symbol_info(symbol)._asdict()['volume_min'])
        triggers[symbol] = int(trigger)

    except Exception as e:
        loger.warning(e, "In making Structure()", symbol)



    if percentage < 85 and Mt.symbol_info(symbol)._asdict()['path'][:6] == "Stocks":
        banned_tickers.append(symbol)
        print(symbol, "Banned")
    elif percentage < 8.1 and Mt.symbol_info(symbol)._asdict()['path'][:5] == "Forex":
        banned_tickers.append(symbol)
        print(symbol, "Banned")
    elif percentage < 85 and not Mt.symbol_info(symbol)._asdict()['path'][:5] == "Forex" :
        banned_tickers.append(symbol)
        print(symbol, "Banned")
    else:
        execution(symbol)



def execution(ticker):
    token = orders[ticker]
    point = Mt.symbol_info(ticker)._asdict()['point']
    trigger = triggers[ticker]
    volume = lots[ticker]
    price = float(Mt.symbol_info(name)._asdict()['ask'])

    try:

        if token == 0 and ohlc_data['chikou_span'].iloc[-27] < ohlc_data['tenkan_sen'].iloc[-27] and ohlc_data['chikou_span'].iloc[-27] < ohlc_data['senkou_span_a'].iloc[-27] and ohlc_data['chikou_span'].iloc[-27] < ohlc_data['senkou_span_b'].iloc[-27] and ohlc_data['open'].iloc[-1] < ohlc_data['senkou_span_b'].iloc[-27]:

            try:
                request['type'] = Mt.ORDER_TYPE_SELL
                request['volume'] = volume
                request['symbol'] = ticker
                request['sl'] = price * 0,975
                request['tp'] = price * 28
                order = Mt.order_send(request)
                time.sleep(2)
                print(order)
                loger.info(order)
                time.sleep(1)
                triggers[ticker] = 1
                orders[ticker] = -1


            except Exception as e:
                loger.info(e, "in Execution()", ticker)




        elif not token == -1 and trigger == 1 and ohlc_data['chikou_span'].iloc[-27] < ohlc_data['tenkan_sen'].iloc[-27] and ohlc_data['chikou_span'].iloc[-27] < ohlc_data['senkou_span_a'].iloc[-27] and \
                    ohlc_data['chikou_span'].iloc[-27] < ohlc_data['senkou_span_b'].iloc[-27] and ohlc_data['open'].iloc[-1] < \
                    ohlc_data['senkou_span_b'].iloc[-27]:

            try:
                position = Mt.positions_get(symbol=ticker)[0]._asdict()['ticket']
                order_number = position
                request['type'] = Mt.ORDER_TYPE_SELL
                request['volume'] = volume
                request['symbol'] = ticker
                request['position'] = int(order_number)
                order = Mt.order_send(request)
                time.sleep(2)
                print(order)
                print("Ticket:", position, ":Ticker:", ticker)
                loger.info(order)
                time.sleep(1)
                triggers[ticker] = 1
                orders[ticker] = -1



            except Exception as e:
                loger.debug(e, "in Execution()", ticker)

            try:
                request['type'] = Mt.ORDER_TYPE_SELL
                request['volume'] = volume
                request['symbol'] = ticker

                request['tp'] = price * 28

                order = Mt.order_send(request)
                time.sleep(2)
                print(order)
                print("Ticket:", order, ":Ticker:", ticker)
                loger.info(order)
                time.sleep(1)
                triggers[ticker] = 1
                orders[ticker] = -1

            except Exception as e:
                loger.debug(e, "in Execution()", ticker)


        elif token == -1 and trigger == 1 and ohlc_data['chikou_span'].iloc[-27] > ohlc_data['kijun_sen'].iloc[-27]:
            try:
                position = Mt.positions_get(symbol=ticker)[0]._asdict()['ticket']
                order_number = position
                request['type'] = Mt.ORDER_TYPE_BUY
                request['volume'] = volume
                request['symbol'] = ticker
                request['position'] = int(order_number)
                order = Mt.order_send(request)
                time.sleep(2)
                print(order)
                print("Ticket:", position, ":Ticker:", ticker)
                loger.info(order)
                time.sleep(1)
                triggers[ticker] = 0
                orders[ticker] = -1



            except Exception as e:
                loger.debug(e, "in Execution()", ticker)

            try:

                request['type'] = Mt.ORDER_TYPE_BUY
                request['volume'] = volume
                request['symbol'] = ticker

                request['tp'] = price * 28
                order = Mt.order_send(request)
                time.sleep(2)
                print(order)
                print("Ticket:", order, ":Ticker:", ticker)
                loger.info(order)
                time.sleep(1)
                triggers[ticker] = 0
                orders[ticker] = -1


            except Exception as e:
                loger.debug(e, "in Execution()", ticker)





        elif token == -1 and trigger == 0 and ohlc_data['chikou_span'].iloc[-27] < ohlc_data['tenkan_sen'].iloc[-27] and \
                    ohlc_data['chikou_span'].iloc[-27] < ohlc_data['senkou_span_a'].iloc[-27] and ohlc_data['chikou_span'].iloc[-27] < ohlc_data['senkou_span_b'].iloc[-27]:

            try:
                position = Mt.positions_get(symbol=ticker)[0]._asdict()['ticket']
                order_number = position
                request['type'] = Mt.ORDER_TYPE_SELL
                request['volume'] = volume
                request['symbol'] = ticker
                request['position'] = int(order_number)
                order = Mt.order_send(request)
                time.sleep(2)
                print(order)
                print("Ticket:", position, ":Ticker:", ticker)
                loger.info(order)
                time.sleep(1)
                triggers[ticker] = 1
                orders[ticker] = -1


            except Exception as e:
                loger.debug(e, "in Execution()", ticker)
            try:

                request['type'] = Mt.ORDER_TYPE_BUY
                request['volume'] = volume
                request['symbol'] = ticker

                request['tp'] = price * 28
                order = Mt.order_send(request)
                time.sleep(2)
                print(order)
                print("Ticket:", order, ":Ticker:", ticker)
                loger.info(order)
                time.sleep(1)
                triggers[ticker] = 0
                orders[ticker] = -1


            except Exception as e:
                loger.debug(e, "in Execution()", ticker)

        elif not token == 1 and trigger == 1 and ohlc_data['chikou_span'].iloc[-27] > ohlc_data['tenkan_sen'].iloc[-27] and ohlc_data['chikou_span'].iloc[-27] > ohlc_data['senkou_span_a'].iloc[-27] and \
                    ohlc_data['chikou_span'].iloc[-27] > ohlc_data['senkou_span_b'].iloc[-27] and ohlc_data['open'].iloc[-1] > \
                    ohlc_data['senkou_span_b'].iloc[-27]:
            try:
                position = Mt.positions_get(symbol=ticker)[0]._asdict()['ticket']
                order_number = position
                request['type'] = Mt.ORDER_TYPE_BUY
                request['volume'] = volume
                request['symbol'] = ticker
                request['position'] = int(order_number)
                order = Mt.order_send(request)
                time.sleep(2)
                print(order)
                print("Ticket:", position, ":Ticker:", ticker)
                loger.info(order)
                time.sleep(1)
                triggers[ticker] = 1
                orders[ticker] = 1


            except Exception as e:
                loger.debug(e, "in Execution()", ticker)
            try:

                request['type'] = Mt.ORDER_TYPE_BUY
                request['volume'] = volume
                request['symbol'] = ticker

                request['tp'] = price * 28
                order = Mt.order_send(request)
                time.sleep(2)
                print(order)
                print("Ticket:", order, ":Ticker:", ticker)
                loger.info(order)
                time.sleep(1)
                triggers[ticker] = 0
                orders[ticker] = -1


            except Exception as e:
                loger.debug(e, "in Execution()", ticker)

        elif token == 1 and trigger == 1 and ohlc_data['chikou_span'].iloc[-27] < ohlc_data['kijun_sen'].iloc[-27]:

            try:
                position = Mt.positions_get(symbol=ticker)[0]._asdict()['ticket']
                order_number = position
                request['type'] = Mt.ORDER_TYPE_SELL
                request['volume'] = volume
                request['symbol'] = ticker
                request['position'] = int(order_number)
                order = Mt.order_send(request)
                time.sleep(2)
                print(order)
                print("Ticket:", position, ":Ticker:", ticker)
                loger.info(order)
                time.sleep(1)
                triggers[ticker] = 0
                orders[ticker] = 1


            except Exception as e:
                loger.debug(e, "in Execution()", ticker)


        elif token == 1 and trigger == 0 and ohlc_data['chikou_span'].iloc[-27] > ohlc_data['tenkan_sen'].iloc[-27] and \
                    ohlc_data['chikou_span'].iloc[-27] > ohlc_data['senkou_span_a'].iloc[-27] and ohlc_data['chikou_span'].iloc[-27] > ohlc_data['senkou_span_b'].iloc[-27]:

            try:
                position = Mt.positions_get(symbol=ticker)[0]._asdict()['ticket']
                order_number = position
                request['type'] = Mt.ORDER_TYPE_BUY
                request['volume'] = volume
                request['symbol'] = ticker
                request['position'] = int(order_number)
                order = Mt.order_send(request)
                time.sleep(2)
                print(order)
                print("Ticket:", position, ":Ticker:", ticker)
                loger.info(order)
                time.sleep(1)
                triggers[ticker] = 1
                orders[ticker] = 1


            except Exception as e:
                loger.debug(e, "in Execution()", ticker)
            try:

                request['type'] = Mt.ORDER_TYPE_BUY
                request['volume'] = volume
                request['symbol'] = ticker

                order = Mt.order_send(request)
                time.sleep(2)
                print(order)
                print("Ticket:", ":Ticker:", ticker)
                loger.info(order)
                time.sleep(1)
                triggers[ticker] = 0
                orders[ticker] = -1


            except Exception as e:
                loger.debug(e, "in Execution()", ticker)

        else:
            time.sleep(5)

    except Exception as e:
        print(e)


#######################################################################################
######################################################################################
#######################################################################################

while len(orders) < 2222:

    for i in range(0, len(Mt.positions_get()) - 1):
        try:

            position = Mt.positions_get()[i]._asdict()['ticket']
            symb = Mt.positions_get()[i]._asdict()['symbol']
            execution(symb)
            time.sleep(1)
        except Exception as e:
            loger.info(e)
            print(e)

    try:

        choice = random.randint(0, num_symbols - 1)
        name = str(symbols[choice]._asdict()['name'])
        print(name)




        ohlc_data = pd.DataFrame(Mt.copy_rates_range(name,
                                                     Mt.TIMEFRAME_D1,
                                                     datetime(2020, 1, 25),
                                                     datetime.now()))


        # Tenkan-sen (Conversion Line): (9-period high + 9-period low)/2))
        nine_period_high = ohlc_data['close'].rolling(window=9).max()
        nine_period_low = ohlc_data['close'].rolling(window=9).min()
        ohlc_data['tenkan_sen'] = (nine_period_high + nine_period_low) / 2
        # Kijun-sen (Base Line): (26-period high + 26-period low)/2))
        period26_high = ohlc_data['close'].rolling(window=26).max()
        period26_low = ohlc_data['close'].rolling(window=26).min()
        ohlc_data['kijun_sen'] = (period26_high + period26_low) / 2
        # Senkou Span A (Leading Span A): (Conversion Line + Base Line)/2))
        ohlc_data['senkou_span_a'] = ((ohlc_data['tenkan_sen'] + ohlc_data['kijun_sen']) / 2).shift(26)
        # Senkou Span B (Leading Span B): (52-period high + 52-period low)/2))
        period52_high = ohlc_data['close'].rolling(window=52).max()
        period52_low = ohlc_data['close'].rolling(window=52).min()
        ohlc_data['senkou_span_b'] = ((period52_high + period52_low) / 2).shift(26)
        # The most current closing price plotted 26 time periods behind (optional)
        ohlc_data['chikou_span'] = ohlc_data['close'].shift(-26)
        ohlc_data['Buy'] = "NaN"
        ohlc_data['Sell'] = "NaN"

        time.sleep(2)

        if name in banned_tickers:
            print("AAAAA, Banned Ticker found :: ", name, " ::")
            continue
        else:
            if not name in orders:

                structure(name)

            else:

                execution(name)


    except Exception as e:
        print("err after choice", e)

####################################################################################

####################################################################################

print("Start Saving")
with open("token_results.txt", "w") as f:

    f.write(json.dumps(orders))
with open("volume_results", "w") as gg:
    gg.write(json.dumps(lots))
with open("order_numbers_results", "w") as ff:
    ff.write(json.dumps(results))
print("Everythong Saved <3 ...")

