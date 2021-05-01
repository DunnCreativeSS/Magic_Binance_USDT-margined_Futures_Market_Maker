# These vars load from database :

#        p = p
#        toreplace.append(p)
#    pairs[key] = toreplace
#pprint(pairs)
from rest_ws_impl import rest_ws
with open('reqs.txt') as e:
    data = e.read()
count = 0
reqs = {}
for line in data.split('\n'):
    if count == 0:
        reqs[line.replace('/','')] = {}
        coin = line.replace('/','')
    elif count == 1:
        reqs[coin]['low'] = float(line)
    elif count == 2:
        reqs[coin]['high'] = float(line)
    elif count == 3:
        reqs[coin]['weight'] = float(line)
        count = -1
    count = count + 1

import requests
r = requests.get("https://fapi.binance.com/fapi/v1/ticker/24hr").json()
for t in r:
    if t['symbol'] in reqs:
        reqs[t['symbol']]['volume$m'] = float(t['quoteVolume']) / 1000000

r = requests.get("https://fapi.binance.com/fapi/v1/ticker/bookTicker").json()
for t in r:
    if t['symbol'] in reqs:
        reqs[t['symbol']]['low$'] = (reqs[t['symbol']]['low'] * float(t['bidPrice'])) / 3 * 1.3
        reqs[t['symbol']]['high$'] = (reqs[t['symbol']]['high'] * float(t['bidPrice'])) / 3 * 1.3

from operator import itemgetter
highs = {}
highwhos = {}
wwhos = {}
vwhos = {}
wvwhos = {}
weights = {}
volumes = {}
wvs = {}
for req in reqs:
    if 'high$' in reqs[req]:
        highs[req] = reqs[req]['high$']
        weights[req] = reqs[req]['high$'] * reqs[req]['weight']
        volumes[req] = reqs[req]['high$'] * reqs[req]['volume$m']
        wvs[req] = reqs[req]['high$'] * reqs[req]['volume$m'] * reqs[req]['weight']
        highwhos[reqs[req]['high$']] = req
        wwhos[weights[req]] = req
        vwhos[volumes[req]] = req
        wvwhos[wvs[req]] = req
Ks = sorted(list(highs.values()))
Ks = Ks[:10]# Or you can use sorted() on the keys 
print('The higher # coins required in the spread, in $, assuming 3x lev, list sorted lowest to highest and only showing top 10')
for k in sorted(Ks): print(highwhos[k], k) 
print('Sum: ' + str(sum(Ks)))

Ks = sorted(list(weights.values()))
Ks = Ks[:10]# Or you can use sorted() on the keys 
print('The higher # coins required in the spread, in $, assuming 3x lev, multiplied by the weight of that coin out of mm points, list sorted lowest to highest and only showing top 10 - followed by the original $ amount')
for k in sorted(Ks): print(wwhos[k], k, highs[wwhos[k]]) 
asum = 0
for k in sorted(Ks): asum = asum + highs[wwhos[k]]
print('Sum: ' + str(asum))

Ks = sorted(list(volumes.values()))
Ks = Ks[:10]# Or you can use sorted() on the keys 
print('The higher # coins required in the spread, in $, assuming 3x lev, multiplied by the 24hr volume of that coin in $m, list sorted lowest to highest and only showing top 10 - followed by the original $ amount')

for k in sorted(Ks): print(vwhos[k], k, highs[vwhos[k]])  
asum = 0
for k in sorted(Ks): asum = asum + highs[vwhos[k]]
print('Sum: ' + str(asum))
Ks = sorted(list(wvs.values()))
Ks = Ks[:10]# Or you can use sorted() on the keys 

print('The higher # coins required in the spread, in $, assuming 3x lev, multiplied by both the above mods (altogether score), list sorted lowest to highest and only showing top 10 - followed by the original $ amount')

for k in sorted(Ks): print(wvwhos[k], k, highs[wvwhos[k]]) 
asum = 0
willpairs = []
relativeOrderSizes = {}
for k in sorted(Ks): asum = asum + highs[wvwhos[k]]
for k in sorted(Ks): willpairs.append(wvwhos[k].replace('USD', '/USD'))
for k in sorted(Ks): relativeOrderSizes[wvwhos[k].replace('USD', '/USD')] = highs[wvwhos[k]] / asum
print('Sum: ' + str(asum))
print(willpairs)
print(relativeOrderSizes)
jload = {}
import json
with open('conf.json', 'r') as f:
    jload = json.loads(f.read())

binApi2 =  {jload['apikey']:jload['apisecret']}

lev = float(jload['lev'])
settings = {jload['apikey']:{'TP': float(jload['TP']) * lev, 'SL': float(jload['SL']) * lev, 'max_skew_mult': float(jload['max_skew_mult']), 'qty_div': float(jload['qty_div']), 'lev': lev
            }
            }

import requests

usdtm = requests.get("https://fapi.binance.com/fapi/v1/ticker/bookTicker").json()
coinm = requests.get("https://dapi.binance.com//dapi/v1/ticker/bookTicker").json()
usdtv = requests.get("https://fapi.binance.com/fapi/v1/ticker/24hr").json()
coinv = requests.get("https://dapi.binance.com/dapi/v1/ticker/24hr").json()
vs = []
vss = {}
"""
for inst in coinv:
    vss[inst['symbol']] = float(inst['volume'])
    vs.append(float(inst['volume']))
"""
for inst in usdtv:
    vss[inst['symbol']] = float(inst['volume'])
    vs.append(float(inst['volume']))

from time import sleep
avg = sum(vs) / len(vs)
aboveavgs = []
for inst in usdtv:
    if float(inst['volume']) > avg / 2:
        aboveavgs.append(inst['symbol'].replace('USDT', '/USDT'))
print(aboveavgs)
print('Avg/total volume for all coin margined futures last 24hr has been: $' + str(round(avg, 4)) + '/$' + str(round(sum(vs), 4)))
print('# instruments total: ' + str(len(vs)) + ', # instruments above avg vol: ' + str(len(aboveavgs)))
print('Outliers of volume: ' + str(max(vs)) + ' and ' + str(min(vs)))
vs.remove(max(vs))
vs.remove(min(vs))
#aboveavgs = []
avg = sum(vs) / len(vs)
for inst in usdtv:
    if float(inst['volume']) > avg / 2:
        if inst['symbol'].replace('USDT', '/USDT') not in aboveavgs:
            aboveavgs.append(inst['symbol'].replace('USDT', '/USDT'))
print('# instruments total: ' + str(len(vs)) + ', # instruments above avg vol less outliers: ' + str(len(aboveavgs)))

# These vars would be posted back to db for tracking users
pairs = {jload['apikey']: willpairs,#aboveavgs,#['XLM/USDT', 'ADA/USDT', 'DASH/USDT', 'ZEC/USDT', 'ATOM/USDT', 'IOST/USDT', 'THETA/USDT', 'XTZ/USDT', 'OMG/USDT', 'COMP/USDT', 'ZRX/USDT', 'KNC/USDT', 'ZIL/USDT', 'DOGE/USDT', 'RLC/USDT', 'BAT/USDT', 'IOTA/USDT', 'XMR/USDT'],
        '7hMrKo1CbbhS58I85uaZtfz2cKUFbDIXlZEIGzCqXEMu7V8QcqjYBonrU93GfH1U': ['XLM/USDT', 'ADA/USDT', 'DASH/USDT', 'ZEC/USDT', 'ATOM/USDT', 'IOST/USDT', 'THETA/USDT', 'XTZ/USDT', 'OMG/USDT', 'COMP/USDT', 'ZRX/USDT', 'KNC/USDT', 'ZIL/USDT', 'DOGE/USDT', 'RLC/USDT', 'BAT/USDT', 'IOTA/USDT', 'XMR/USDT'],
        }#'key':['array', 'of', 'usdt-margin', 'to', 'trade']}#'BTC/USDT'




#self.Place_Orders[self.rest_ws.client.apiKey].positions
#self.Place_Orders[self.rest_ws.client.apiKey].openorders
#self.Place_Orders[self.rest_ws.client.apiKey].equity_btc
#self.Place_Orders[self.rest_ws.client.apiKey].equity_usd
#self.Place_Orders[self.rest_ws.client.apiKey].trades




























#pprint(len(pairs))
fifteens = aboveavgs#['XLM/USDT', 'ADA/USDT', 'DASH/USDT', 'ZEC/USDT', 'ATOM/USDT']
tens = []#'OMG/USDT', 'COMP/USDT', 'ZRX/USDT', 'XMR/USDT', 'ZIL/USDT', 'KNC/USDT', 'XTZ/USDT', 'IOTA/USDT', 'BAT/USDT', 'IOST/USDT', 'THETA/USDT']
fives = []#'DOGE/USDT']
threes = []#'RLC/USDT']

#jarettrsdunn+alimm@gmail.com
#binApi = "8799eb6011f07a7dbba434907f71adc5f7e76af1fd12be26bb4e3294904e9852"
#binSecret = "e487c0edb6ec0f6fd839919858dce4a3f936d7d67fe0e6a4773b579173fe1355"

feeTiers = {0:{'maker': 0.02/100, 'bnbmaker': 0.018/100},
            1:{'maker': 0.016/100, 'bnbmaker': 0.0144/100},
            2:{'maker': 0.014/100, 'bnbmaker': 0.0128/100},
            3:{'maker': 0.012/100, 'bnbmaker': 0.0108/100},
            4:{'maker': 0.01/100, 'bnbmaker': 0.009/100},
            5:{'maker': 0.008/100, 'bnbmaker': 0.0072/100},
            6:{'maker': 0.006/100, 'bnbmaker': 0.0054/100},
            7:{'maker': 0.004/100, 'bnbmaker': 0.0036/100},
            8:{'maker': 0.002/100, 'bnbmaker': 0.0018/100},
            9:{'maker': 0, 'bnbmaker': 0}
            }
import multiprocessing

from strategies.mm import Place_Orders

from collections    import OrderedDict
from datetime       import datetime
import asyncio
import threading
from datetime import timedelta
import sys
#pprint(sys.argv[1])
import linecache
import os
import traceback
from os.path        import getmtime
import requests
#pprint(0)
"""
from cryptofeed import FeedHandler
from cryptofeed import FeedHandler
from cryptofeed.callback import BookCallback, TickerCallback, TradeCallback
from cryptofeed.defines import BID, ASK, FUNDING, L2_BOOK, OPEN_INTEREST, TICKER, TRADES
from cryptofeed.exchanges import BinanceFutures
fh = FeedHandler()
"""
#pprint(1)
mids = {}
async def ticker(feed, pair, bid, ask, timestamp, ex):
    global mids
    #pprint(f'Ex?: {ex} Timestamp: {timestamp} Feed: {feed} Pair: {pair} Bid: {bid} Ask: {ask}')
    
    if 'BINANCE' in feed:
        #ETH-USD_200925
        name = pair.replace('-', '/')
        #pprint(dt)


   # pprint(feed + '-' + name + '-' + dt +': ' + str( 0.5 * ( float(bid) + float(ask))))
    #mids[name] = {'ask': float(ask), 'bid':  float(bid)}
"""
pairs2 = requests.get('https://fapi.binance.com/fapi/v1/exchangeInfo').json()
bcontracts = []
for symbol in pairs2['symbols']:
    split = len(symbol['baseAsset'])
    normalized = symbol['symbol'][:split] + '-' + symbol['symbol'][split:]
    #pprint(normalized)
    bcontracts.append(normalized)
config = {TICKER: bcontracts}
"""

#fh.add_feed(BinanceFutures(config=config, callbacks={TICKER: TickerCallback(ticker)}))

#pprint(2)
def loop_in_thread():
    abc=123

from time           import sleep
from utils          import ( get_logger, lag, print_dict, print_dict_of_dicts, sort_by_key,
                             ticksize_ceil, ticksize_floor, ticksize_round )
import json
import random, string
import copy as cp
import argparse, logging, math, os, pathlib, sys, time, traceback
import ccxt

#t = threading.Thread(target=loop_in_thread, args=())
#t.daemon = True
#t.start()
#t = threading.Thread(target=loop_in_thread, args=())
#t.start()
# Add command line switches
parser  = argparse.ArgumentParser( description = 'Bot' )
d         = datetime.now()  - timedelta(hours = 0)
epoch = datetime(1970,1,1)
start_time = int(datetime.timestamp(d) * 1000)
#pprint(start_time)
d2 = int(datetime.timestamp(d) * 1000)
#pprint(d2)
epoch = datetime(1970,1,1)
st = int((d - epoch).total_seconds()) * 1000
st = start_time
days = ((d2 - start_time) / 1000 / 60 / 60 / 24)
#pprint(days)
import inspect
mmbot = None
def pprint(string):
    

    
    log = 'log.txt'
    with open(log, "a") as myfile:
        myfile.write(datetime.utcnow().strftime( '%Y-%m-%d %H:%M:%S' ) + ', line: ' + str(inspect.currentframe().f_back.f_lineno)  + ': ' + str(string) + '\n')
def PrintException():
    exc_type, exc_obj, tb = sys.exc_info()
    f = tb.tb_frame
    lineno = tb.tb_lineno
    filename = f.f_code.co_filename
    linecache.checkcache(filename)
    line = linecache.getline(filename, lineno, f.f_globals)
    string = 'EXCEPTION IN ({}, LINE {} "{}"): {}'.format(filename, lineno, line.strip(), exc_obj)
    print(string)
    #pprint(string)
    
    sleep(1)
# Use production platform/account
#parser.add_argument('key', metavar='K', type=str, nargs='+',
                  #  help='your key sir')
"""
parser.add_argument( '-key',
                     dest   = 'key',
                     action = 'store_true' )
parser.add_argument( '-p',
                     dest   = 'use_prod',
                     action = 'store_true' )

# Do not display regular status updates to terminal
parser.add_argument( '--no-output',
                     dest   = 'output',
                     action = 'store_false' )

# Monitor account only, do not send trades
parser.add_argument( '-m',
                     dest   = 'monitor',
                     action = 'store_true' )

# Do not restart bot on errors
parser.add_argument( '--no-restart',
                     dest   = 'restart',
                     action = 'store_false' )
"""
args    = parser.parse_args()
#jload['apikey'] = jload['apikey']
firstattempt = True
firstkey = jload['apikey']
"""
for key in binApi2:
    if firstattempt == True:
        firstattempt = False
        firstkey = jload['apikey']
pprint('argskey: ' + jload['apikey'])
"""



"""
if not args.use_prod:
    KEY     = ''
    SECRET  = ''
    URL     = 'https://test.deribit.com'
else:
    KEY     = ''
    SECRET  = ''
    URL     = 'https://www.deribit.com'
"""
BP                  = 1e-4      # one basis point
BTC_SYMBOL          = 'btc'
CONTRACT_SIZE       = 10     # USD
COV_RETURN_CAP      = 100       # cap on variance for vol estimate
DECAY_POS_LIM       = 0.1       # position lim decay factor toward expiry
EWMA_WGT_COV        = 4         # parameter in % points for EWMA volatility estimate
EWMA_WGT_LOOPTIME   = 0.1       # parameter for EWMA looptime estimate
FORECAST_RETURN_CAP = 20        # cap on returns for vol estimate
LOG_LEVEL           = logging.INFO
MIN_ORDER_SIZE      = 75
MAX_LAYERS          =  3        # max orders to layer the ob with on each side
MKT_IMPACT          =  0.01   # base 1-sided spread between bid/offer
NLAGS               =  2        # number of lags in time series
PCT                 = 100 * BP  # one percentage point
PCT_LIM_LONG        = 200    # % position limit long
PCT_LIM_SHORT       = 100       # % position limit short
PCT_QTY_BASE        = 0.05       # pct order qty in bps as pct of acct on each order
MIN_LOOP_TIME       =   14.6     # Minimum time between loops
RISK_CHARGE_VOL     =   0.75    # vol risk charge in bps per 100 vol
SECONDS_IN_DAY      = 3600 * 24
SECONDS_IN_YEAR     = 365 * SECONDS_IN_DAY
WAVELEN_MTIME_CHK   = 15        # time in seconds between check for file change
WAVELEN_OUT         = 15        # time in seconds between output to terminal
WAVELEN_TS          = 15        # time in seconds between time series update
VOL_PRIOR           = 100       # vol estimation starting level in percentage pts

    

    #DECAY_POS_LIM = data['RISK_CHARGE_VOL']['current']
    
EWMA_WGT_COV        *= PCT

MKT_IMPACT          *= BP
PCT_LIM_LONG        *= PCT
PCT_LIM_SHORT       *= PCT
PCT_QTY_BASE        *= BP
VOL_PRIOR           *= PCT


class MarketMaker( object ):
    
    def __init__( self, monitor=True, output=True ):
        self.key = jload['apikey']
        #pprint('key ' + self.key)
        # TP and SL are by position, and are calculated by unrealized % * leverage (and are close to the ROE % presented by the binance web interface)
        self.TP = 40
        self.SL = 20

        #max_skew_mult is how many times the desired order size it'll accept being in position long or short before it stops orderng in that direction. For example, if we have max_skew_mult=5 and the desired order size is $20 while we have $80 in position in that direction, it'll enter as $80<$20x5. However, if we had $120 in position in that same direction it wouldn't enter that order
        self.max_skew_mult = 10

        #this is the size of the order the algo will enter. if you have $30 in your account and the qty_div is 15, it will enter orders that are $30/15= $2 large. This calculation ignores leverage
        self.qty_div = 15

        #the leverage multiplier to use - if the script refuses to enter orders after changing this, you'll need to manually close your positions and re-run
        self.lev = 25

        #binance broker apikey to use
        self.brokerKey = 'v0tiKJjj'
        self.rest_ws = {}
        self.trades = {}    
        self.threethousandmin = None
        self.Place_Orders = {}
        self.equity_usd         = {}
        self.equity_btc     = {}
        self.equity_usd_init    = {}
        self.equity_btc_init    = {}
        self.con_size           = float( CONTRACT_SIZE )
        self.feeRate = None
        #self.rest_ws.client2 = {}
        self.goforit = True
        self.connecting = False
        self.openorders = {}
        self.orderbooks = {}
        self.bids = {}
        self.deltas             = OrderedDict()
        self.futures            = OrderedDict()
        self.futures_prv        = OrderedDict()
        self.logger             = None
        self.mean_looptime      = 1
        self.monitor            = monitor
        self.output             = output or monitor
        self.positions          = {}
        self.spread_data        = None
        self.this_mtime         = None
        self.ts                 = None
        self.vols               = OrderedDict()
        self.orderRateLimit = 100
        #self.proton = proto2()
        #self.proton.connect()
        #sleep(15)
        key = jload['apikey']
        lev = float(jload['lev'])
        settings = {jload['apikey']:{'TP': float(jload['TP']) * lev, 'SL': float(jload['SL']) * lev, 'max_skew_mult': float(jload['max_skew_mult']), 'qty_div': float(jload['qty_div']), 'lev': lev
                    }
                    }
        self.TP = settings[key]['TP']
        self.SL = settings[key]['SL']
        self.max_skew_mult = settings[key]['max_skew_mult']
        self.qty_div = settings[key]['qty_div']
        self.lev = settings[key]['lev']
    
    
    def getTrades( self, client, pair, endTime, quoteTotal, commissionTotal, returnTrades ):
        try:
            oldTime = 9999999999999999999999999999999999999
            
            if self.goforit == True:
                self.goforit =  False
                alist = []
                for key in pairs.keys():
                    for pair in pairs[key]:
                        if pair not in alist:
                            alist.append(pair)
                
                d         = datetime.now()  - timedelta(hours = 0)
                d2 = int(datetime.timestamp(d) * 1000)
                #pprint(d2)
                epoch = datetime(1970,1,1)
                st = int((d - epoch).total_seconds()) * 1000
                st = start_time - 60 * 2 * 1000
                days = ((d2 - st) / 1000 / 60 / 60 / 24)
                #pprint(days)
                #if start_time > st:
                #    st = start_time
                #    days    = ( datetime.now() - self.start_time ).total_seconds() / SECONDS_IN_DAY
                
                if endTime == 0:
                    trades = self.rest_ws.client.fapiPrivateGetUserTrades({"symbol": pair.replace('/',''), "limit": 1000, 'startTime': st })
                elif endTime != 9999999999999999999999999999999999999:
                    trades = self.rest_ws.client.fapiPrivateGetUserTrades({"symbol": pair.replace('/',''), "limit": 1000, 'startTime': st , 'endTime': endTime})
                else:
                    return False
                #pprint(len(trades))
                for t in trades:
                    returnTrades.append(t)
                    if t['time'] < oldTime:
                        oldTime = t['time']
                    commissionTotal = commissionTotal + float(t['commission'])
                    if float(t['quoteQty']) > 0:
                        quoteTotal = quoteTotal + float(t['quoteQty'])
                    else:
                        quoteTotal = quoteTotal - float(t['quoteQty'])
                    self.feeRate = float(t['commission']) / float(t['quoteQty'])
                if len(trades) < 999:
                    #if self.Place_Orders[self.rest_ws.client.apiKey] is not None:
                        #self.Place_Orders[self.rest_ws.client.apiKey].trades = returnTrades
                    return([quoteTotal, commissionTotal, days])
                else:
                    sleep(1)
                    return(self.getTrades(self.rest_ws.client, pair, oldTime, quoteTotal, commissionTotal, returnTrades))
            else:
                sleep(1)
                return(self.getTrades(self.rest_ws.client, pair, oldTime, quoteTotal, commissionTotal, returnTrades))    
        except:
            PrintException()
            sleep(1)
            return(self.getTrades(self.rest_ws.client, pair, oldTime, quoteTotal, commissionTotal, returnTrades))    
    def get_bbo( self, contract ): # Get best b/o excluding own orders
        
        # Get orderbook
        best_bid    = self.rest_ws.mids[contract]['bid']
        best_ask    = self.rest_ws.mids[contract]['ask']
        #print([best_bid, best_ask])
            
        if 'OCEAN' in contract:
            print({ 'bid': best_bid, 'ask': best_ask })
        return { 'bid': best_bid, 'ask': best_ask }
    
        
    def get_futures( self, client ): # Get all current futures instruments
        try:
            gogo = True
            try:
                if self.Place_Orders[self.rest_ws.client.apiKey].goforit2 == False:
                    gogo = False
            except:
                gogo = True
            if gogo == True:
                self.futures_prv    = cp.deepcopy( self.futures )
                sleep((self.orderRateLimit / 1.1 ) / 1000)
                insts               = self.rest_ws.client.fetchMarkets()

                #pprint(insts)
                #pprint(insts[0])
                self.futures        = sort_by_key( { 
                    i[ 'symbol' ]: i for i in insts if i['type'] == 'future' and i['active'] == True or i['type'] == 'delivery' and i['active'] == True
                } )
                
                #print((self.futures))
                sleep((self.orderRateLimit / 1.1 ) / 1000)
                account = self.rest_ws.client.fapiPrivateGetAccount()
                feeTier = account['feeTier']

                if self.feeRate == None:
                    self.feeRate = feeTiers[float(feeTier)]['maker']

                exchange_info = self.rest_ws.client.fapiPublicGetExchangeInfo()
                for rl in exchange_info['rateLimits']:
                    if rl['rateLimitType'] == 'ORDERS':
                        if rl['interval'] == 'MINUTE' and rl['intervalNum'] == 1 and self.rest_ws.client.rateLimit != 1.01 * (1000 * (60 / rl['limit'])):
                            self.orderRateLimit = 1.01 * (1000 * (60 / rl['limit']))
                            self.rest_ws.client.rateLimit = self.orderRateLimit
                            print (self.rest_ws.client.rateLimit)
                            if self.Place_Orders[self.rest_ws.client.apiKey] is not None:
                                self.Place_Orders[self.rest_ws.client.apiKey].orderRateLimit = self.orderRateLimit
                #sleep(100)
                #pprint(self.futures)
                #for k, v in self.futures.items():
                    #self.futures[ k ][ 'expi_dt' ] = datetime.strptime( 
                    #                                   v[ 'expiration' ][ : -4 ], 
                    #                                   '%Y-%m-%d %H:%M:%S' )
        except:
            PrintException()                    
        
    def get_pct_delta( self ):         
        self.update_status()
        return sum( self.deltas.values()) / float(self.equity_btc[self.rest_ws.client.apiKey])

    def get_spot_old( self, pair ):
        abc=123#pprint('getspotold!')
        sleep(1)
        #pprint(self.rest_ws.client2.fetchTicker( pair )['bid'])
        #keys = []
        #for key in binApi2:
        #    keys.append(key)
       # ran = keys[random.randint(0, len(keys)-1)]
        return self.rest_ws.self.rest_ws.client2[self.key].fetchTicker( pair )['bid']
    def get_spot( self, pair ):
        #pprint(self.rest_ws.client2.fetchTicker( pair )['bid'])
        try:
            self.bids[pair] = self.rest_ws.mids[ pair ]['bid']
        except:
            self.bids[pair] = self.get_spot_old(pair)
        return self.bids[pair]

    
    def get_precision( self, contract ):

        return self.futures[ contract ] ['info'] [ 'pricePrecision' ]

    
    def get_ticksize( self, contract ):
        
        return self.futures[ contract ] ['info'] ['filters'] [ 0 ] [ 'tickSize' ]
        
    
    

        
                                
    def cancelall(self, client):
        if self.rest_ws.client == None:
            for key in binApi2.keys():    
                self.rest_ws.client = ccxt.binance(
                    {"apiKey": key,
                    "secret": binApi2[key],
                     'options': {'defaultType': 'future'},

            'enableRateLimit': True,
        })

                #binance_futures.set_sandbox_mode(True)
                    

                
        
        for pair in pairs[self.rest_ws.client.apiKey]:

            try:
                ords        = self.openorders[self.rest_ws.client.apiKey][pair]
                for order in ords:
                    #pprint(order)
                    oid = order ['info'] ['orderId']
                   # pprint(order)
                    try:
                        gogo = True
                        try:
                            if self.Place_Orders[self.rest_ws.client.apiKey].goforit2 == False:
                                gogo = False
                        except:
                            gogo = True
                        if gogo == True:
                            sleep((self.orderRateLimit / 1.1 ) / 1000)
                            self.rest_ws.client.cancelOrder( oid , pair )
                    except Exception as e:
                        PrintException()
            except KeyError as e:
                pass
            except Exception as e:
                PrintException()
    def restart( self ):        
        try:
            strMsg = 'RESTARTING'
            #pprint( strMsg )
            #self.cancelall(None)
            strMsg += ' '
            
            #self.proton.connect()
            for i in range( 0, 5 ):
                strMsg += '.'
                #pprint( strMsg )
                #sleep( 1 )
        except:
            pass
        finally:
            os.execv( sys.executable, [ sys.executable ] + sys.argv )        
            
    def output_status ( self, client ):
        while True:
            try:
                #if self.rest_ws.client.apiKey == firstkey:
                now     = datetime.now()
                days    = ( now - self.start_time ).total_seconds() / SECONDS_IN_DAY
                abc=123#pprint( ' ********************************************************************' )
                abc=123#pprint( ' Start Time:        %s' % self.start_time.strftime( '%Y-%m-%d %H:%M:%S' ))
                abc=123#pprint( ' Current Time:      %s' % now.strftime( '%Y-%m-%d %H:%M:%S' ))
                abc=123#pprint( ' Days:              %s' % round( days, 1 ))
                abc=123#pprint( ' Hours:             %s' % round( days * 24, 1 ))
                abc=123#pprint( ' Spot Price:        %s' % self.get_spot('BTC/USDT'))
                
                equity_usd = self.equity_usd[self.rest_ws.client.apiKey]
                equity_btc = self.equity_btc[self.rest_ws.client.apiKey]
                abc=123#pprint(equity_usd)
                abc=123#pprint(self.equity_usd_init[self.rest_ws.client.apiKey])
                pnl_usd = equity_usd - self.equity_usd_init[self.rest_ws.client.apiKey]
                pnl_btc = equity_btc - self.equity_btc_init[self.rest_ws.client.apiKey]
                
                
                #pprint( '%% Delta:           %s%%'% round( self.get_pct_delta() / PCT, 1 ))
                #pprint( 'Total Delta (BTC): %s'   % round( sum( self.deltas.values()), 2 ))        
                #print_dict_of_dicts( {
                #    k: {
                #        'BTC': self.deltas[ k ]
                #    } for k in self.deltas.keys()
                #    }, 
                #    roundto = 2, title = 'Deltas' )
                
                #pprint(self.positions)
                if len(self.positions[self.rest_ws.client.apiKey]) > 1:
                    for k in self.positions[self.rest_ws.client.apiKey].keys():
                        try: 
                            abc = self.bids[k]
                        except:
                            self.bids[k] = self.get_bbo(k)['bid']
                    """
                    print_dict_of_dicts( {
                        k: {
                            'Contracts $ Value': round(self.positions[self.rest_ws.client.apiKey][ k ][ 'positionAmt' ] * self.bids[k] * 100) / 100
                        } for k in self.positions[self.rest_ws.client.apiKey].keys()
                        }, 

                        title = ' Positions' )
                    """
                    
                if not self.monitor:
                    """
                    print_dict_of_dicts( {
                        k: {
                            '%': self.vols[ k ]
                        } for k in self.vols.keys()
                        }, 
                        multiple = 100, title = ' Vols' )
                    """
                    #pprint( '\nMean Loop Time: %s' % round( self.mean_looptime, 2 ))
                    #self.cancelall()
                abc=123#pprint( '' )    
                abc=123#pprint(' ')
                days    = ( datetime.now() - self.start_time ).total_seconds() / SECONDS_IN_DAY
                abc=123#pprint(' Volumes Traded Projected Daily of Required (' + str(days) + ' days passed thus far...)')
                abc=123#pprint(' Equity: $' + str(round(self.equity_usd[self.rest_ws.client.apiKey]*100)/100))
                btc = self.get_spot('BTC/USDT')
                abc=123#pprint(' btc')
                percent = self.equity_usd[self.rest_ws.client.apiKey] / btc
                
                volumes = []
                tradet = 0
                feest = 0
                if self.rest_ws.goforit2 == True:
                    for pair in pairs[self.rest_ws.client.apiKey]:
                    
                        gettrades = self.getTrades(self.rest_ws.client, pair, 0, 0, 0, [])

                        #pprint(gettrades)
                        if gettrades != False:
                            volume = (gettrades[0] / (gettrades[2]))
                            feest = feest + gettrades[1]
                            tradet = tradet + volume * 30
                            printprint = True
                            if pair in fifteens:
                                volume = (volume / 15000)
                            elif pair in tens:
                                volume = (volume / 10000)
                            elif pair in fives:
                                volume = (volume / 5000)
                            elif pair in threes:
                                volume = (volume / 3000)
                            else:
                                printprint = False
                                volume = (volume / 25000)
                            volumes.append(volume)
                            #pprint(volume)
                            if printprint == True:
                                if volume > 0:
                                    #if self.threethousandmin == None:
                                    abc=123#pprint(' ' + pair + ': ' + str(round(volume*1000)/10) + '%' + ', (Real) USD traded: $' + str(round(gettrades[0]*100)/100) + ', fees paid: $' + str(round(gettrades[1] * 10000)/10000))
                                    #else:
                                    #    abc=123#pprint(' ' + pair + ': ' + str(round(volume*1000)/10) + '%' + ', w/ ' + str(self.threethousandmin * self.equity_usd[self.rest_ws.client.apiKey]) + '$ minimum for sustainable strategy: ' + str(round(volume*self.threethousandmin*1000)/10)  + '%, ' + str(round((volume * self.threethousandmin)*1000)/10) + '%'  + ' (Real) USD traded: $' + str(round(gettrades[0]*100)/100) + ', fees paid: $' + str(round(gettrades[1] * 10000)/10000))
                            else:
                                if gettrades[0] > 0:
                                    abc=123#pprint(' (Real) USD traded: $' + str(round(gettrades[0]*100)/100) + ', fees paid: $' + str(round(gettrades[1] * 10000)/10000))
                    volumes.sort()
                    h = 100
                    try:
                        for i in range(0,5):
                            if volumes[-i] < h and volumes[-i] > 0:
                                h = volumes[-i]
                                if h > 1:
                                    h = 1
                        try:
                            h = 1 / h
                        except:
                            h = 1
                        mult = h
                        h = h * self.equity_usd[self.rest_ws.client.apiKey]
                        print('')
                        print(' Approx. traded volumes over 30 days: ' + str(tradet) + ', in BTC: ' + str(round(tradet/btc*1000)/1000))
                        print(' Approx. Min Equity at ' + str(self.lev) + 'x in USD to Achieve 100% Daily Requirements Across 6 Highest %s Above: $' + str(round(h * 100)/100))
                        diff = h / self.equity_usd[self.rest_ws.client.apiKey]
                        btcneed = (((tradet * diff / btc) / 3000) )
                        print(' That\'s ' + str(round(diff*100)/100) + 'x the balance now, bringing projected USD/month to: ' + str(round(tradet * diff * 100)/100) + ', and BTC: ' + str(round((tradet * diff / btc)* 100)/100))
                        if self.threethousandmin is not None:
                            diff = self.threethousandmin
                            print(' With ' + str(self.threethousandmin) + 'x the balance now that we\'d need for the 3000 btc/month minimum, though, projected USD/month to: ' + str(round(tradet * diff * 100)/100) + ', and BTC: ' + str(round((tradet * diff / btc)* 100)/100))

                        apy = 365 / (gettrades[2])
                        pnl = (((self.equity_usd[self.rest_ws.client.apiKey] + feest) / self.equity_usd[self.rest_ws.client.apiKey]) -1) * 100
                        pnl2 = pnl * apy
                        print(' Now, if we were running in a trial mode of Binance Market Maker Program\'s Rebates, or if we had achieved these rates already, we would have earned $' + str(round(feest * 100)/100) + ' by now (on our actual equity), or rather earning ' + str(round(pnl*1000)/1000) + '% PnL so far, or ' + str(round(pnl2*1000)/1000) + ' % Annual Percentage Yield!')
                        
                        if btcneed < 1 and btcneed != 0:
                            h = h / btcneed
                            self.threethousandmin = (round(h * 100)/100) / self.equity_usd[self.rest_ws.client.apiKey]

                            print(' For 3000 btc/month volumes, would make the equity minimum approx. $' + str(round(h * 100)/100))
                    except:
                        abc=123
                print(' ')
                print(' Equity ($):        %7.2f'   % equity_usd)
                print(' P&L ($)            %7.2f'   % pnl_usd)
                print(' Equity (BTC):      %7.4f'   % equity_btc)
                print(' P&L (BTC)          %7.4f'   % pnl_btc)
                print(' ')
                potential = pnl_usd+(((feest+feest)/0.016)*0.02)
                potentialday = potential / days
                potential2k = potential / (self.equity_usd[self.rest_ws.client.apiKey] / 2000)
                potential2kday = potential2k / days
                print(' Potential earned if we had fee rebate: $' + str(round(potential* 1000) / 1000))
                print(' potentialday: ' + str(potentialday))
                print(' potential2k: ' + str(potential2k))
                print(' potential2kday: ' + str(potential2kday))
                log = 'rebate.txt'
                
                with open(log, "a") as myfile:
                    myfile.write(datetime.utcnow().strftime( '%Y-%m-%d %H:%M:%S' ) + ', ' + self.rest_ws.client.apiKey + ': Potential earned: $' + str(round(potential* 1000) / 1000) + ', that\'s $' + str(round(potentialday*1000)/1000) + '/day, with $2k it would be $' + str(round(potential2k*1000)/1000) + ' by now or $' + str(round(potential2kday*1000)/1000) + '/day!\n')
                #sleep(240)
                    
            except Exception as e:
                #PrintException()    
                PrintException()
                sleep(10)
        proc = threading.Thread(target=self.output_status, args=())
        abc=123#pprint('3 proc')
        proc.start()
        proc.terminate()     
        sleep(5)    
    def run( self ):
        #pprint('1')
        key = self.key
        #self.create_self.rest_ws.client(key)

        self.openorders[key] = {}
        self.positions[key] = {}
        
        self.equity_btc[key] = None
        self.equity_usd[key] = None
        self.equity_btc_init[key] = None
        self.equity_usd_init[key] = None
        self.Place_Orders[key] = None
        #pprint('2')
        done = False
        
            
        self.rest_ws = rest_ws(self.orderRateLimit, pairs, None, None, None)
        
        while done == False:
            try:
                t = threading.Thread(target=self.run_first, args=(self.rest_ws.client,))
                t.daemon = True
                t.start()
                done = True
            except:
                PrintException()
                sleep(2)

            
        t_ts = t_out = t_loop = t_mtime = datetime.now()
        #pprint('3')
    
                
        while True:
            try:
                client = self.rest_ws.client
                self.get_futures(self.rest_ws.client)
                client = self.rest_ws.client
                if self.Place_Orders[self.rest_ws.client.apiKey] is not None:
                    if self.Place_Orders[self.rest_ws.client.apiKey].equity_usd is not None:
                        self.equity_btc[self.rest_ws.client.apiKey] = self.Place_Orders[self.rest_ws.client.apiKey].equity_btc
                        self.equity_usd[self.rest_ws.client.apiKey] = self.Place_Orders[self.rest_ws.client.apiKey].equity_usd
                        self.positions[self.rest_ws.client.apiKey] = self.Place_Orders[self.rest_ws.client.apiKey].positions
                        print(self.positions)
                        self.openorders[self.rest_ws.client.apiKey] = self.Place_Orders[self.rest_ws.client.apiKey].openorders
                        self.trades[self.rest_ws.client.apiKey] = self.Place_Orders[self.rest_ws.client.apiKey].trades
                        if self.equity_usd_init[self.rest_ws.client.apiKey] == None and self.equity_usd[self.rest_ws.client.apiKey] > 0:
                            self.equity_usd_init[self.rest_ws.client.apiKey]    = self.equity_usd[self.rest_ws.client.apiKey]
                            self.equity_btc_init[self.rest_ws.client.apiKey]    = self.equity_btc[self.rest_ws.client.apiKey] 
                            #pprint(self.rest_ws.client.apiKey + ' equity starting: ' + str(self.equity_usd[self.rest_ws.client.apiKey]))
                self.get_futures(self.rest_ws.client)
                
                # Restart if a new contract is listed
                #if len( self.futures ) != len( self.futures_prv ):
                #    self.restart()
                
                
                t_now   = datetime.now()
                
                # Update time series and vols
                if ( t_now - t_ts ).total_seconds() >= WAVELEN_TS:
                    t_ts = t_now
                
                sleep(1)
                # ()
                
                # Display status to terminal
                if self.output:    
                    t_now   = datetime.now()
                
                # Restart if file change detected
                t_now   = datetime.now()
                if ( t_now - t_mtime ).total_seconds() > WAVELEN_MTIME_CHK:
                    t_mtime = t_now
                    #if getmtime( __file__ ) > self.this_mtime:
                    #    self.restart()
                
                t_now       = datetime.now()
                looptime    = ( t_now - t_loop ).total_seconds()
                
                # Estimate mean looptime
                w1  = EWMA_WGT_LOOPTIME
                w2  = 1.0 - w1
                t1  = looptime
                t2  = self.mean_looptime
                
                self.mean_looptime = w1 * t1 + w2 * t2
                
                t_loop      = t_now
                sleep_time  = MIN_LOOP_TIME - looptime
                #if sleep_time > 0:
                #    time.sleep( sleep_time )
                if self.monitor:
                    time.sleep( WAVELEN_OUT )
                self.update_timeseries()
                self.update_vols()
            except:
                PrintException()
                sleep(2)
    def randomword(self, length):
       letters = string.ascii_lowercase
       return ''.join(random.choice(letters) for i in range(length))
    def dorestart( self ):
        sleep( 90)
        self.restart()
    def run_first( self, client ):
        
        for pair in pairs[self.rest_ws.client.apiKey]:
            sleep((self.orderRateLimit / 1.1 ) / 1000)
            try:
                self.rest_ws.client.fapiPrivatePostLeverage({'symbol': pair.replace('/USDT', 'USDT'), 'leverage': int(self.lev)})
            except:
                PrintException()
                sleep((self.orderRateLimit / 1.1 ) / 1000)
                
        t = threading.Thread(target=self.dorestart, args=())
        t.daemon = True
        t.start()
        t = threading.Thread(target=self.updateBids, args=())
        t.daemon = True
        t.start()    
        
        t = threading.Thread(target=self.updatePositions, args=(self.rest_ws.client,))
        t.daemon = True
        t.start()    
        for pair in aboveavgs:
            t = threading.Thread(target=self.updateOrders, args=(self.rest_ws.client,pair,len(aboveavgs)))
            t.daemon = True
            t.start()    
        
        #self.cancelall()
        self.logger = get_logger( 'root', LOG_LEVEL )
        # Get all futures contracts
        self.get_futures(self.rest_ws.client)
        #sleep(10)
        """
        pairs = []
        for fut in self.futures.keys():
            try:
                self.get_spot_old(fut)
                pairs.append(fut)
            except:
                abc=123#pprint(fut)
        """
        self.start_time         = datetime.now()- timedelta(hours = 0)
        #t = threading.Thread(target=self.looptiloop, args=(self.rest_ws.client,))
        #t.start()
        self.this_mtime = getmtime( __file__ )
        self.symbols    = [ BTC_SYMBOL ] + list( pairs[self.rest_ws.client.apiKey]); self.symbols.sort()
        stemp = []
        for s in self.symbols:
            stemp.append(s)
        self.symbols = stemp
        self.deltas     = OrderedDict( { s: None for s in self.symbols } )
        
        # Create historical time series data for estimating vol
        ts_keys = self.symbols + [ 'timestamp' ]; ts_keys.sort()
        
        
        alist = ['btc', 'timestamp']
        for key in pairs.keys():
            for pair in pairs[key]:
                if pair not in alist:
                    alist.append(pair)
        self.ts = [
            OrderedDict( { f: None for f in alist } ) for i in range( NLAGS + 1 )
        ]
        print(self.ts)
        self.vols   = OrderedDict( { s: VOL_PRIOR for s in self.symbols } )
        #sleep(10)
        
        # start any sockets here, i.e a trade socket
        #
        
        self.Place_Orders[self.rest_ws.client.apiKey] = Place_Orders(self.rest_ws, random, pprint, firstkey, self.lev, multiprocessing, self.brokerKey, self.qty_div, self.orderRateLimit, self.max_skew_mult, self.get_precision, math, self.TP, self.SL, asyncio, sleep, threading, PrintException, ticksize_floor, ticksize_ceil, pairs[self.rest_ws.client.apiKey], fifteens, tens, fives, threes, self.con_size, self.get_spot, self.equity_btc[self.rest_ws.client.apiKey], self.positions[self.rest_ws.client.apiKey], self.get_ticksize, self.vols, self.get_bbo, self.openorders[self.rest_ws.client.apiKey], self.equity_usd[self.rest_ws.client.apiKey], self.randomword, self.logger, PCT_LIM_LONG, PCT_LIM_SHORT, DECAY_POS_LIM, MIN_ORDER_SIZE, CONTRACT_SIZE, MAX_LAYERS, BTC_SYMBOL, RISK_CHARGE_VOL, BP)
        alist = []
        for key in pairs.keys():
            for pair in pairs[key]:
                if pair not in alist:
                    alist.append(pair)
        for fut in alist:
            t = threading.Thread(target=self.updateOrders, args=(self.rest_ws.client,fut,len(alist),))
            t.daemon = True
            t.start()
        balance = self.rest_ws.client.fetch_balance()
        self.equity_usd[self.rest_ws.client.apiKey] = balance['USDT']['total']

        self.equity_btc[self.rest_ws.client.apiKey] = self.equity_usd[self.rest_ws.client.apiKey] / self.get_spot('BTC/USDT')
        if self.equity_usd_init[self.rest_ws.client.apiKey] == None and self.equity_usd[self.rest_ws.client.apiKey] > 0:
            self.equity_usd_init[self.rest_ws.client.apiKey]    = self.equity_usd[self.rest_ws.client.apiKey]
            self.equity_btc_init[self.rest_ws.client.apiKey]    = self.equity_btc[self.rest_ws.client.apiKey] 
            #pprint(self.rest_ws.client.apiKey + ' equity starting: ' + str(self.equity_usd[self.rest_ws.client.apiKey]))
        if self.Place_Orders[self.rest_ws.client.apiKey] is not None:
            self.Place_Orders[self.rest_ws.client.apiKey].equity_btc = self.equity_btc[self.rest_ws.client.apiKey]
            self.Place_Orders[self.rest_ws.client.apiKey].equity_usd = self.equity_usd[self.rest_ws.client.apiKey]
        try:
        
            self.positions[self.rest_ws.client.apiKey]  = OrderedDict( { f: {
                'size':         0,
                'positionAmt':      0,
                'indexPrice':   None,
                'markPrice':    None
            } for f in pairs[self.rest_ws.client.apiKey] } )
            sleep((self.orderRateLimit / 1.1 ) / 1000)
            
            positions       = self.rest_ws.client.fapiPrivateGetPositionRisk()

            #pprint('lala')
            #pprint(positions)
            
            for pos in positions:
                if pos['symbol'].split('USDT')[0] + '/USDT' in pairs[self.rest_ws.client.apiKey]:
                    pos['positionAmt'] = float(pos['positionAmt'])
                    pos['entryPrice'] = float(pos['entryPrice'])
                    pos['unRealizedProfit'] = float(pos['unRealizedProfit'])
                    pos['leverage'] = float(pos['leverage'])
                    notional = math.fabs(pos['positionAmt']) * pos['entryPrice']
                    #fee = self.feeRate * notional
                    #notional = notional - fee
                    if notional > 0:
                        notionalplus = notional + pos['unRealizedProfit']
                        percent = ((notionalplus / notional) -1) * 100

                        pos['ROE'] = percent * pos['leverage']
                    else:
                        pos['ROE'] = 0
                    self.positions[self.rest_ws.client.apiKey][ pos['symbol'].split('USDT')[0] + '/USDT'] = pos

                    #pprint(pos['ROE'])    
            if self.Place_Orders[self.rest_ws.client.apiKey] is not None:
                self.Place_Orders[self.rest_ws.client.apiKey].positions = self.positions[self.rest_ws.client.apiKey]
            
        except Exception as e:
            PrintException()
        try:
            t = threading.Thread(target=self.output_status, args=(self.rest_ws.client,))
            t.daemon = True
            t.start()
                

            t = threading.Thread(target=self.Place_Orders[self.rest_ws.client.apiKey].run(), args=())
            t.daemon = True
            t.start()


            
        except Exception as e:
            PrintException()    
        
          
        self.update_status()
        #sleep(3)
    def updateOrders(self, client, pair, length):
        sleep(1)
        #while True:
        try:
            #for pair in pairs[self.rest_ws.client.apiKey]:
            try:
                #pprint(pair)
                try:
                    sleep((self.orderRateLimit / random.randint(1,18) ) / 1000)
                    orders = self.rest_ws.client.fetchOpenOrders( pair )
                    for order in orders:
                        order['type'] = order['info']['status']
                        order['id'] = order['info']['orderId']
                        order['side'] = order['info']['side']
                        order['price'] = order['info']['price'] 
                    self.openorders[self.rest_ws.client.apiKey][pair] = orders
                    #pprint(pair)
                except Exception as e:
                    if 'does not have market symbol' in str(e):
                        try:
                            sleep((self.orderRateLimit / random.randint(1,18) ) / 1000)
                            orders = self.rest_ws.client.fetchOpenOrders( pair )
                            for order in orders:
                                order['type'] = order['info']['status']
                                order['id'] = order['info']['orderId']
                                order['side'] = order['info']['side']
                                order['price'] = order['info']['price']
                            self.openorders[self.rest_ws.client.apiKey][pair] = orders
                            #pprint(pair)
                        except Exception as e:
                            #if 'does not have market symbol' in str(e):
                                
                            PrintException()
                            sleep((self.orderRateLimit* 5))#/ random.randint(1,18) ) / 1000)
                            return (self.updateOrders(self.rest_ws.client, pair, length))
                    else:
                        sleep((self.orderRateLimit * 5))#/ random.randint(1,18) ) / 1000)
                        return (self.updateOrders(self.rest_ws.client, pair, length))
                    #PrintException()
            except:
                sleep((self.orderRateLimit * 5))# / random.randint(1,18) ) / 1000)
                return (self.updateOrders(self.rest_ws.client, pair, length))
            if self.Place_Orders[self.rest_ws.client.apiKey] is not None:
                self.Place_Orders[self.rest_ws.client.apiKey].openorders = self.openorders[self.rest_ws.client.apiKey]
                for pair in self.Place_Orders[self.rest_ws.client.apiKey].openorders:
                
                    ask_ords        = [ o for o in self.Place_Orders[self.rest_ws.client.apiKey].openorders[pair] if o['side'] == 'SELL' ] 
                    bid_ords        = [ o for o in self.Place_Orders[self.rest_ws.client.apiKey].openorders[pair] if o['side'] == 'BUY' ] 
                    self.lbo[pair] = len(bid_ords)
                    self.lao[pair] = len(ask_ords)
        except:
            sleep((self.orderRateLimit * 5))#/ random.randint(1,18) ) / 1000)
            return (self.updateOrders(self.rest_ws.client, pair, length))
    def updatePositions( self, client ):
        while True:
            try:
            
                gogo = True
                try:
                    if self.rest_ws.goforit2 == False:
                        gogo = False
                except:
                    gogo = True
                if True:# gogo == True:
                    sleep(1)
                    self.positions[self.rest_ws.client.apiKey]  = OrderedDict( { f: {
                        'size':         0,
                        'positionAmt':      0,
                        'indexPrice':   None,
                        'markPrice':    None
                    } for f in pairs[self.rest_ws.client.apiKey] } )
                    sleep((self.orderRateLimit / 1.1 ) / 1000)
                    positions       = self.rest_ws.client.fapiPrivateGetPositionRisk()

                    #pprint('lala')
                    #pprint(positions)
                    
                    for pos in positions:
                        if pos['symbol'].split('USDT')[0] + '/USDT' in pairs[self.rest_ws.client.apiKey]:
                            pos['positionAmt'] = float(pos['positionAmt'])
                            pos['entryPrice'] = float(pos['entryPrice'])
                            pos['unRealizedProfit'] = float(pos['unRealizedProfit'])
                            pos['leverage'] = float(pos['leverage'])
                            notional = math.fabs(pos['positionAmt']) * pos['entryPrice']
                            fee = self.feeRate * notional
                            notional = notional - fee
                            if notional > 0:
                                notionalplus = notional + pos['unRealizedProfit']
                                percent = ((notionalplus / notional) -1) * 100

                                pos['ROE'] = percent * pos['leverage']
                            else:
                                pos['ROE'] = 0

                            self.positions[self.rest_ws.client.apiKey][ pos['symbol'].split('USDT')[0] + '/USDT'] = pos
                            
                    if self.Place_Orders[self.rest_ws.client.apiKey] is not None:
                        self.Place_Orders[self.rest_ws.client.apiKey].positions = self.positions[self.rest_ws.client.apiKey]
                    #pprint(self.positions)    
            except Exception as e:
                PrintException()
                sleep(5)
    def updateBids( self ):
        while True:
            alist = []
            for key in pairs.keys():
                for pair in pairs[key]:
                    if pair not in alist:
                        alist.append(pair)
                        #pprint(pair)
            for pair in alist:
                try:
                    if pair in mids:
                        self.bids[pair] = self.rest_ws.mids[pair]['bid']
                    else:
                        self.bids[pair] = self.get_spot_old(pair)
                except:
                    #PrintException()
                    sleep(5)
    def looptiloop(self, client):
        while True:
        
            try:
                while True:
                    balance = self.rest_ws.client.fetch_balance()
                    self.equity_usd[self.rest_ws.client.apiKey] = balance['USDT']['total']

                    self.equity_btc[self.rest_ws.client.apiKey] = self.equity_usd[self.rest_ws.client.apiKey] / self.get_spot('BTC/USDT')
                    if self.equity_usd_init[self.rest_ws.client.apiKey] == None and self.equity_usd[self.rest_ws.client.apiKey] > 0:
                        self.equity_usd_init[self.rest_ws.client.apiKey]    = self.equity_usd[self.rest_ws.client.apiKey]
                        self.equity_btc_init[self.rest_ws.client.apiKey]    = self.equity_btc[self.rest_ws.client.apiKey] 
                        #pprint(self.rest_ws.client.apiKey + ' equity starting: ' + str(self.equity_usd[self.rest_ws.client.apiKey]))
                    if self.Place_Orders[self.rest_ws.client.apiKey] is not None:
                        self.Place_Orders[self.rest_ws.client.apiKey].equity_btc = self.equity_btc[self.rest_ws.client.apiKey]
                        self.Place_Orders[self.rest_ws.client.apiKey].equity_usd = self.equity_usd[self.rest_ws.client.apiKey]
                    sleep(1)
                    
            except Exception as e:
                abc=123#pprint(self.rest_ws.client.apiKey)
                PrintException()
                sleep(5)
            
                
                
                
                
                

    
    def update_status( self ):
          
             
        abc=123        
        #self.deltas = OrderedDict( 
        #    { k: float(self.positions[ k ][ 'positionAmt' ]) for k in pairs}
        #)
        

        
        
    
    def update_timeseries( self ):
        
        #if self.monitor:
            #return None
        
        for t in range( NLAGS, 0, -1 ):
            self.ts[ t ]    = cp.deepcopy( self.ts[ t - 1 ] )    
        spot                    = self.get_spot('BTC/USDT')
        self.ts[ 0 ][ BTC_SYMBOL ]    = spot
        alist = []
        for key in pairs.keys():
            for pair in pairs[key]:
                if pair not in alist:
                    alist.append(pair)
                    #pprint(pair)
        for c in alist:
            
            bbo = self.get_bbo( c )
            bid = bbo[ 'bid' ]
            ask = bbo[ 'ask' ]
            c = c
            if not bid is None and not ask is None:
                mid = 0.5 * ( bbo[ 'bid' ] + bbo[ 'ask' ] )
            else:
                continue
            self.ts[ 0 ][ c ]               = mid
        self.ts[ 0 ][ 'timestamp' ]  = datetime.now()
        #pprint(self.ts)
        
    def update_vols( self ):
        
        #if self.monitor:
           # return None
        w   = EWMA_WGT_COV
        ts  = self.ts
        
        t   = [ ts[ i ][ 'timestamp' ] for i in range( NLAGS + 1 ) ]
        p   = { c: None for c in self.vols.keys() }
        for c in ts[ 0 ].keys():
            p[ c ] = [ ts[ i ][ c ] for i in range( NLAGS + 1 ) ]
        #pprint('vols!')
        #pprint(t)
        if any( x is None for x in t ):
            return None
        #pprint('vols!')
        #pprint(p)
        for c in self.vols.keys():
            if any( x is None for x in p[ c ] ):
                return None
        
        NSECS   = SECONDS_IN_YEAR
        cov_cap = COV_RETURN_CAP / NSECS
        
        for s in self.vols.keys():
            
            x   = p[ s ]
            if len(x) > 1:            
                dx  = x[ 0 ] / x[ 1 ] - 1
                dt  = ( t[ 0 ] - t[ 1 ] ).total_seconds()
                v   = min( dx ** 2 / dt, cov_cap ) * NSECS
                v   = w * v + ( 1 - w ) * self.vols[ s ] ** 2
                
                self.vols[ s ] = math.sqrt( v )
        
        #pprint('vols!')
        for key in self.Place_Orders.keys():
            if self.Place_Orders[key] is not None:
                #pprint(self.vols)
                self.Place_Orders[key].vols = self.vols                    
try:
    
    



    #done of vars in db
    mmbot = MarketMaker(  )
    #pprint(0)
    mmbot.run()
except( KeyboardInterrupt, SystemExit ):
    print( "Cancelling open orders" )
    mmbot.cancelall(None)
    sys.exit()
except:
    #pprint( traceback.format_exc())
    print( traceback.format_exc())
    if mmbot.connecting == False:
        mmbot.cancelall(None)
        mmbot.connecting = True
        mmbot.restart()
        sleep(60)
        mmbot.connecting = False
