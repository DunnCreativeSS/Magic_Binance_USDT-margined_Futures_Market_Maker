import json
import threading
from time import sleep
from binance.client import Client
import ccxt
import math
from datetime import timedelta
import sys
from binance.enums import *

#pprint(sys.argv[1])
import linecache
import os
import traceback
import logging
from cryptofeed import FeedHandler
from cryptofeed.defines import TICKER
from cryptofeed.callback import TickerCallback

# not all imports shown for clarity
from cryptofeed.exchanges import Binance

from os.path        import getmtime
import requests
import json
import urllib
with open('reqs.txt') as e:
    data = e.read()
count = 0
reqs = {}
for line in data.split('\n'):
    if count == 0:
        reqs[line.replace('/','')] = {}
        coin = line.replace('/','')
    if count == 1:
        reqs[coin]['low'] = float(line)
    if count == 1:
        reqs[coin]['high'] = float(line)
    if count == 2:
        reqs[coin]['weight'] = float(line)
        count = -1
    count = count + 1

import requests
r = requests.get("https://api.binance.com/api/v1/ticker/24hr").json()
for t in r:
    if t['symbol'] in reqs:
        reqs[t['symbol']]['volume$m'] = float(t['quoteVolume']) / 1000000

r = requests.get("https://api.binance.com/api/v1/ticker/bookTicker").json()
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

from binance.client import Client   
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
willpairs = ['BUSD/DAI','BUSD/USDT','USDC/USDT','TUSD/USDT','USDT/DAI','USDC/BUSD','PAX/USDT','TUSD/BUSD','PAX/BUSD','SUSD/USDT']

margins = ["USDC/USDT", "BUSD/USDT", "USDC/BUSD"]
willpairs = margins
def PrintException():
    #if apiKey == firstkey:
    exc_type, exc_obj, tb = sys.exc_info()
    f = tb.tb_frame
    lineno = tb.tb_lineno
    filename = f.f_code.co_filename
    linecache.checkcache(filename)
    line = linecache.getline(filename, lineno, f.f_globals)
    string = 'EXCEPTION IN ({}, LINE {} "{}"): {}'.format(filename, lineno, line.strip(), exc_obj)
    if 'binance Account has insufficient balance for requested action' not in string and 'MIN_NOTIONAL' not in string:
            print(string)
    abc=123#pprint(string)
    
class rest_ws ( object ):
    def __init__( self, orderRateLimit, pairs, creates, cancels, openorders, MAX_LAYERS):
        jload = {}
        self.MAX_LAYERS = MAX_LAYERS
        with open('conf.json', 'r') as f:
            jload = json.loads(f.read())
        binApi2 =  {jload['apikey']:jload['apisecret']}
        key = jload['apikey']
        abc=123#pprint(key)
        self.client = ccxt.binance(
            {"apiKey": key,
            "secret": binApi2[key],
             'options': {'defaultType': 'margin'},

    'enableRateLimit': True,
        'rateLimit': orderRateLimit
    })
        self.key = key
        self.client.options['defaultType'] = 'margin'
        self.orderRateLimit = orderRateLimit
        self.pairs = pairs[key]
        self.creates = {}
        self.cancels = {}
        self.openorders = {}
        self.ordersTo = []
        self.equity_usd_init = None
        self.equity_btc_init = None
        self.edits = []
        self.editOs = []
        self.goforit = True
        self.goforit2 = True
        lev = float(jload['lev'])
        settings = {jload['apikey']:{'TP': float(jload['TP']) * lev, 'SL': float(jload['SL']) * lev, 'max_skew_mult': float(jload['max_skew_mult']), 'qty_div': float(jload['qty_div']), 'lev': lev
                    }
                    }
        self.TP = settings[key]['TP']
        self.SL = settings[key]['SL']
        self.max_skew_mult = settings[key]['max_skew_mult']
        self.qty_div = settings[key]['qty_div']
        self.lev = settings[key]['lev']
        
        self.ask_ords = {}
        self.bid_ords = {}
        self.positions = {}
        self.lbo = {}
        self.lao = {}
        self.equity_usd = 0
        self.equity_btc = 0
        self.bids = {}
        #self.client3 = Client(key, binApi2[key])
        #self.client.set_sandbox_mode(True)
        self.client2 = {}
        self.client2[key] = (ccxt.binance({    "apiKey": key,
             'options': {'defaultType': 'margin'},
    "secret": binApi2[key],
    'enableRateLimit': True
}))
        
        #pprint(self.client[key].options)
        #pprint(dir(self.client)) 
        #pprint(dir(self.client))
        
        
        #print(m)
        #sleep(100)
        # then start the socket manager
        self.mids = {}
        t = threading.Thread(target=self.fhsetup, args=())
        t.daemon = True
        t.start()
        #t = threading.Thread(target=self.update_orders, args=())
        #t.daemon = True
        #t.start()
        t = threading.Thread(target=self.update_positions, args=())
        t.daemon = True
        t.start()
        t = threading.Thread(target=self.failSafeReset, args=())
        t.daemon = True
        t.start()
    #pprint((self.orderRateLimit / 1000) * len(alist))
        t = threading.Timer((self.orderRateLimit / 1000) * len(pairs), self.resetGoforit)
        t.daemon = True
        t.start()
        

        
    def fhsetup (self):
        fh = FeedHandler()
        m = self.client.fetchMarkets()

        # ticker, trade, and book are user defined functions that
        # will be called when ticker, trade and book updates are received
        ticker_cb = {TICKER: TickerCallback(self.ticker)}


        tArr = []
        for market in m:
            if market['active'] == True:
                sym = (market['symbol'])
                if 'USDT' in sym:
                    tArr.append(sym.replace('/','-'))
        tArr = []
        for sym in willpairs:
            
            tArr.append(sym.replace('/','-'))
        tArr.append('SUSD-USDT')
        tArr.append('BTC-USDT')
        #3print(tArr)
        #sleep(100)
        fh.add_feed(Binance(pairs=tArr, channels=[TICKER], callbacks=ticker_cb))

        fh.run()
    def get_spot_old( self, pair ):
        #print('getspotold2! ' + pair)
        #sleep(1)
        #pprint(self.rest_ws.client2.fetchTicker( pair )['bid'])
        #keys = []
        #for key in binApi2:
        #    keys.append(key)
       # ran = keys[random.randint(0, len(keys)-1)]
        mids = self.client2[self.key].fetchTicker( pair )
        self.mids[pair] = {'bid': mids['bid'], 'ask': mids['ask']}
        return mids['bid']
    def get_spot( self, pair ):
        #pprint(self.rest_ws.client2.fetchTicker( pair )['bid'])
        try:
            self.bids[pair] = self.mids[ pair ]['bid']

        except:
            self.bids[pair] = self.get_spot_old(pair)
        return self.bids[pair]
    def update_positions( self ):
        while True:
            try:
                
                positions       = self.client.fetchBalance({'type':'margin'})
                margin_iso = self.client.sapi_get_margin_isolated_account() 
                #print(margin_iso)
                f = self.client.fetch_balance({'type':'future'})
                d = self.client.fetch_balance({'type':'delivery'})
                #print(f)
                #print(d)
                wp = []
                for w in willpairs:
                    for w2 in w.split('/'):
                        wp.append(w2)
                self.positions = {}
                #print(positions)
                for p in positions['total']:
                    #print(positions['total'][p])
                    try:
                        if p == 'USDT':
                            pos = {}
                            pos['positionAmt'] = positions['total'][p]
                            pos['notional'] = positions['total'][p]#positions['total'][p] * (self.mids[p + '/USDT']['bid'] + self.mids[p + '/USDT']['ask']) / 2 
                            self.positions[p] = pos
                        if p != 'USDT' and p in wp:
                            pos = {}
                            pos['positionAmt'] = positions['total'][p]
                            if pos['positionAmt'] > 0:
                                pos['notional'] = positions['total'][p] * self.get_spot(p + '/USDT')
                            else:
                                pos['notional'] = 0
                            self.positions[p] = pos
                    except:

                            PrintException()
                for p in positions:
                    try:
                        if 'total' in positions['total'][p]:
                            if p == 'USDT':
                                pos = {}
                                pos['positionAmt'] = positions['total'][p]
                                pos['notional'] = positions['total'][p]#positions['total'][p] * (self.mids[p + '/USDT']['bid'] + self.mids[p + '/USDT']['ask']) / 2 
                                self.positions['total'][p] = pos
                            if p != 'USDT':
                                pos = {}
                                pos['positionAmt'] = positions['total'][p]
                                if pos['positionAmt'] > 0:
                                    pos['notional'] = positions['total'][p] * self.get_spot(p + '/USDT')
                                else:
                                    pos['notional'] = 0
                                self.positions['total'][p] = pos
                    except:
                        abc=123#PrintException()
                #info = self.client3.get_margin_account()
                #print(info)
                t = 0 
                bals = {}
                for bal in self.positions:
                    if self.positions[bal]['notional'] > 0:
                        bals[bal] = self.positions[bal]['notional']
                    t = t + self.positions[bal]['notional']
                bal = self.client.fetchBalance()
                b1 = float(bal['info']['totalNetAssetOfBtc'])
                b2 = float(bal['info']['totalAssetOfBtc'])
                usd = b1
                btc = b1
                if b2 > b1:
                    usd =  b2
                    btc = b2
                btcusdt = self.client.fetchTicker('BTC/USDT')
                mid = (btcusdt['bid'] + btcusdt['ask'] ) / 2
                usd = usd * mid
                print(usd)
                self.equity_usd = usd
                self.equity_btc = btc
                if self.equity_usd_init == None:
                    self.equity_usd_init = self.equity_usd
                    self.equity_btc_init = self.equity_btc
                #print(bals)
                #print(self.equity_usd)
                #print(self.positions)
                sleep(1)
                """
                for pos in positions:
                    pair = pos['symbol'].replace('USDT', '/USDT')
                    if pair in self.pairs:
                        pos['positionAmt'] = float(pos['positionAmt'])
                        pos['entryPrice'] = float(pos['entryPrice'])
                        pos['unRealizedProfit'] = float(pos['unRealizedProfit'])
                        pos['leverage'] = float(self.lev)
                        pos['notional'] = float(pos['notional'])
                        notional = math.fabs(pos['positionAmt']) * pos['entryPrice']
                        #fee = self.feeRate * notional
                        #notional = notional - fee
                        if notional > 0:
                            notionalplus = notional + pos['unRealizedProfit']
                            percent = ((notionalplus / notional) -1) * 100

                            pos['ROE'] = percent * pos['leverage']
                        else:
                            pos['ROE'] = 0
                        self.positions[ pair] = pos
                sleep(1)
                """
            except:
                PrintException()
                sleep(1)
    def update_orders(self, fut):
        if True:
            try:
                sleep(self.orderRateLimit / 1000)
               # if fut not in margins:
                data        = self.client.fetchOpenOrders( fut )
                #else:
                #    data = self.client3.get_open_margin_orders(symbol=fut.replace('/',''))
                self.openorders[fut] = []
                abc=123#print(data)
                for o in data:
                    #print(o)
                    #print(o['side'])
                    #fut = o['symbol'].replace('USD', '/USD')
                    #o['id'] = int(o['orderId'])
                    if fut not in self.openorders:
                        self.openorders[fut] = []
                    o['id'] = o['info']['orderId']
                    self.openorders[fut].append(o)
                    #print(o)
            #for fut in self.pairs:
                #fut = fut
                try:
                    if len(self.openorders[fut]) > 0:
                        abc=123#self.pprint('lenopenorders ' + fut + ': ' + str(len(self.openorders[fut])))
                    ask_ords        = [ o for o in self.openorders[fut] if o['side'].upper() == 'SELL'  ] 
                    bid_ords        = [ o for o in self.openorders[fut] if o['side'].upper() == 'BUY'  ]
                    #if 'BAT' in fut:
                    #    for o in self.openorders[fut]:
                    #        abc=123#self.pprint(o)
                    self.ask_ords[fut] = ask_ords
                    self.bid_ords[fut] = bid_ords
                    self.lbo[fut] = len(bid_ords)
                    self.lao[fut] = len(ask_ords)
                    cancel_oids = []
                    orig_ids = []
                    if self.MAX_LAYERS < len( bid_ords ):
                        cancel_oids += [ int(o['id']) for o in bid_ords[ 3 : ]]
                        orig_ids += [ (o['clientOrderId']) for o in bid_ords[ 3 : ]]
                    if self.MAX_LAYERS < len( ask_ords ):
                        cancel_oids += [ int(o['id']) for o in ask_ords[ 3 : ]]
                        orig_ids += [ (o['clientOrderId']) for o in ask_ords[ 3 : ]]
                    coids = []
                    oroids = []
                    count = 0
                    for idd in cancel_oids:
                        if count < 9:
                            coids.append(idd)
                            oroids.append(orig_ids[count])
                            count = count + 1
                    cancel_oids = coids
                    orig_ids = oroids
                    try:
                        #if self.cancels[fut] == False:
                        if len(cancel_oids) > 0:#self.firstkey == self.client.apiKey and 
                            
                            self.cancels[fut] = True
                            abc=123#self.pprint(self.client.apiKey + ': cancel '  + fut + ': from ' + str(len(bid_ords)) + ' bid_ords and ' + str(len(ask_ords)) + ' asks, cancelling: ' + str(len(cancel_oids)))
                            #abc=123#self.pprint({'symbol': fut, 'orderIdList': cancel_oids})
                            
                            t = threading.Thread(target=self.batch_delete_orders, args=(fut, cancel_oids, orig_ids))
                            t.daemon = True
                            t.start()
                            self.cancels[fut] = False
                            for oid in cancel_oids:
                                for order in self.openorders[fut]:
                                    if oid == order['id']:
                                        self.openorders[fut].remove(order)
                           # abc=123#self.pprint(cancel)

                        if 'BAT' in fut:# and self.firstkey == self.client.apiKey:
                            bat = len(self.bid_ords['BAT/USDT']) + len(self.ask_ords['BAT/USDT'])
                            #if len(self.bid_ords['BAT/USDT']) > self.MAX_LAYERS or len(self.ask_ords['BAT/USDT']) > self.MAX_LAYERS:
                            ran = self.random.randint(0, 50)
                            #print(ran)
                            if ran < 2:
                                abc=123#self.pprint(self.client.apiKey + ': lenorders BAT ' + str(bat))
                                #abc=123#self.pprint(self.client.apiKey + ': lenaskorders BAT ' + str(len(self.ask_ords['BAT/USDT'])))
                    except Exception as e:
                        abc=123#self.pprint('leno' + str(e))
                        PrintException()
                        self.cancels[fut] = False
                except:
                    PrintException()
                    sleep(2)
            except Exception as e:
                abc=123#self.pprint('leno' + str(e))
                self.openorders[fut] = 0
                PrintException()  
        sleep(self.orderRateLimit / 1000)#len(self.pairs) / 2) 
            
    def failSafeReset( self ):
        while True:
            try:
                t = threading.Timer(5, self.resetGoforit)
                t.daemon = True
                #self.num_threads = #self.num_threads + 1
                t.start()
                sleep(5)
            except:
                PrintException()
                sleep(5)
        proc = threading.Thread(target=self.failSafeReset, args=())
        abc=123#abc=123#self.pprint('4 proc')
        proc.start()
        proc.terminate() 
        sleep(5) 
    
   
    async def ticker(self, feed, symbol, bid, ask, timestamp, receipt_timestamp):
        
        #if symbol == willpairs[0].replace('/','-'):
            #print(f'Timestamp: {timestamp} Feed: {feed} Symbol: {symbol} Bid: {bid} Ask: {ask}')
        self.mids[symbol.replace('-','/')] = {"bid": float(bid), "ask": float(ask)}


    def error(self, e: 'BinanceApiException'):
        print(e.error_code + e.error_message)
    
    def resetGoforit2( self ):
        try:
            self.goforit2 = True
            abc=123#self.pprint(self.client.apiKey + ': self.goforit2')
            #self.num_threads = #self.num_threads - 1

            return
        except:
            proc = threading.Thread(target=self.resetGoforit2, args=())
            PrintException()
            
    def resetGoforit( self ):
        try:
            self.goforit = True
            #abc=123#self.pprint(self.goforit)
            #self.num_threads = #self.num_threads - 1

            return
        except:
            proc = threading.Thread(target=self.resetGoforit, args=())
            abc=123#abc=123#self.pprint('6 proc')
            proc.start()
            proc.terminate() 
            sleep(5)
    def resetGoforit( self ):
        self.goforit =  True
    

    def edit_order( self, clientOrderId, oid, fut, type, dir, qty, prc, brokerPhrase ):
        done = False
        order = {
                "clientOrderId": clientOrderId,
                "id": oid,
                "symbol" : fut.replace('/',''),
                "side" : dir.upper(),
                "type" : type.upper(),
                "amount": self.client.amount_to_precision(fut, qty),
                "price": prc,
                "newClientOrderId": brokerPhrase,
                "timeInForce": 'GTX'
            }
        print('edit ' + str(order))
        order = (fut.replace('/',''), type.upper(), dir.upper(), self.client.amount_to_precision(fut, qty), self.client.price_to_precision(fut, prc), {"newClientOrderId": brokerPhrase, "timeInForce": 'GTX'})
       # self.editOs.append(order  )
        #if len(self.editOs) >= 5:
        #    while done == False:
        try:


            if True:
                #abc=123#self.pprint('edit ' + fut)
                self.goforit = False
                #self.num_threads = #self.num_threads + 1
                t = threading.Timer(self.orderRateLimit / 1000 * 5, self.resetGoforit)
                t.daemon = True
                t.start()
                #await self.asyncio.sleep(self.orderRateLimit / 1000)
                #self.num_threads = #self.num_threads + 1
                cancel_oids = []

                orig_ids = []
                self.editOs = self.openorders[fut]

                for o in self.editOs:
                    if 'id' in o:
                        cancel_oids.append(int(o['id']))
                        orig_ids.append((o['clientOrderId']))
                        o.pop('id', None)
                #print(cancel_oids)
                abc=123#print('EXCEPTION' + str(cancel_oids))
                abc=123#print('EXCEPTION' + str(self.editOs))
                d = self.batch_delete_orders(fut, cancel_oids, orig_ids)
               # print(d)
                orders = [self.client.encode_uri_component(self.client.json(order), safe=",") for order in self.editOs]
                if qty < 11:
                    qty = 11
                if qty > 1:
                    #if fut not in margins:
                    response = self.client.createOrder(fut, type.upper(), dir.upper(), self.client.amount_to_precision(fut, qty), self.client.price_to_precision(fut, prc), {"newClientOrderId": brokerPhrase})
                    #print(response)
                """   
                else:
                    qty = qty * 3

                    if dir.upper() == 'BUY':
                        create_margin_order(
                                symbol=fut.replace('/',''),
                                side=SIDE_BUY,
                                type=ORDER_TYPE_LIMIT,
                                timeInForce=TIME_IN_FORCE_GTC,
                                quantity=self.client.amount_to_precision(fut, qty),
                                price=self.client.price_to_precision(fut, prc))
                    else:
                        create_margin_order(
                                symbol=fut.replace('/',''),
                                side=SIDE_SELL,
                                type=ORDER_TYPE_LIMIT,
                                timeInForce=TIME_IN_FORCE_GTC,
                                quantity=self.client.amount_to_precision(fut, qty),
                                price=self.client.price_to_precision(fut, prc))
                """
                #print(response)

                #params = {
                #    'batchOrders' : self.client.json(self.editOs)
                #}

                #orders = [self.client.encode_uri_component(self.client.json(order), safe=",") for order in self.editOs]
                #response = self.client.apiPrivatePostBatchOrders(params)
                abc=123#self.pprint('batchoed: ' + str(response))
                #b = self.client.apiPrivatePostBatchOrders( {'batchOrders': json.dumps(self.editOs).replace(', ', ',')})
                #print(b)
                abc=123#print(d)
                self.editOs = self.editOs[ 5 : ]
                #self.client.editOrder( oid, fut, type, dir, qty, prc, params  )
                if 'XLM' in fut  and self.client.apiKey == self.firstkey:
                    abc=123#abc=123#self.pprint(fut + ' edited!')
                done = True
                self.edits[fut] = False
            else:
                #if 'XLM' in fut:
                abc=123#self.pprint(fut + ' edit blocked! ' + str(self.goforit) + ' ' + str(self.goforit2))
                done = True
                self.edits[fut] = False
                sleep(self.orderRateLimit / 1000 * len(self.pairs) / 2)
        except Exception as e:
            if 'Unknown order sent' not in str(e):
                PrintException()


            self.edits[fut] = False
            done = True
            sleep(self.orderRateLimit / 1000)
    def create_order( self, fut, type, dir, qty, prc, tif, brokerPhrase ):
        
        try:
            if tif != None: 
                order = {
                    "symbol" : fut.replace('/',''),
                    "side" : dir.upper(),
                    "type" : type.upper(),
                    "amount": self.client.amount_to_precision(fut, qty),
                    "price": self.client.price_to_precision(fut, prc),
                    "newClientOrderId": brokerPhrase,
                    "timeInForce": 'GTX'
                }
                order = (fut.replace('/',''), type.upper(), dir.upper(), self.client.amount_to_precision(fut, qty), self.client.price_to_precision(fut, prc), {"newClientOrderId": brokerPhrase})
       
            else:
                order = {
                    "symbol" : fut.replace('/',''),
                    "side" : dir.upper(),
                    "type" : type.upper(),
                    "amount": self.client.amount_to_precision(fut, qty),
                    "newClientOrderId": brokerPhrase
                }
                order = (fut.replace('/',''), type.upper(), dir.upper(), self.client.amount_to_precision(fut, qty), self.client.price_to_precision(fut, prc), {"newClientOrderId": brokerPhrase, "timeInForce": 'GTX'})
       
            print('create ' + str(order))
            #if len(self.ordersTo) < 5:
            #    self.ordersTo.append(order)
            #if len(self.ordersTo) >= 5:    
            if True :#and len(self.ordersTo) >= 5:
                try:
                    #abc=123#self.pprint('create ' + fut)
                    self.goforit = False
                    #self.num_threads = #self.num_threads + 1
                    t = threading.Timer((self.orderRateLimit / 1000) * 5, self.resetGoforit)
                    t.daemon = True
                    t.start()
                    exchange = self.client

                    #await self.asyncio.sleep(self.orderRateLimit / 1000)
                    
                    abc=123#print(self.ordersTo)
                    abc=123#print(len(self.ordersTo))
                    orders = [self.client.encode_uri_component(self.client.json(order), safe=",") for order in self.ordersTo]
                    if qty < 11:
                        qty = 11
                    if qty > 1:
                    #if fut not in margins:
                        #print(self.client.amount_to_precision(fut, qty))
                        response = self.client.createOrder(fut, type.upper(), dir.upper(), self.client.amount_to_precision(fut, qty), self.client.price_to_precision(fut, prc), {"newClientOrderId": brokerPhrase})
                    """
                    else:
                        qty = qty * 3
                        
                        if dir.upper() == 'BUY':
                            create_margin_order(
                                    symbol=fut.replace('/',''),
                                    side=SIDE_BUY,
                                    type=ORDER_TYPE_LIMIT,
                                    timeInForce=TIME_IN_FORCE_GTC,
                                    quantity=self.client.amount_to_precision(fut, qty),
                                    price=self.client.price_to_precision(fut, prc))
                        else:
                            create_margin_order(
                                    symbol=fut.replace('/',''),
                                    side=SIDE_SELL,
                                    type=ORDER_TYPE_LIMIT,
                                    timeInForce=TIME_IN_FORCE_GTC,
                                    quantity=self.client.amount_to_precision(fut, qty),
                                    price=self.client.price_to_precision(fut, prc))
                    """
                    #print(response)

                    self.ordersTo = self.ordersTo[ 5 : ]
                    #o = self.client.createOrder(fut, type, dir, qty, prc, {"timeInForce": 'GTX', "newClientOrderId": brokerPhrase} )
                    
                    #print(o)

                    done = True
                    
                    self.creates[fut] = False
                except:
                    done = True
                    PrintException()
                    self.ordersTo = []
            else:
                #if 'XLM' in fut:
                    #abc=123#self.pprint(fut + ' order blocked!')
                done = True
                sleep(self.orderRateLimit / 1000 * len(self.pairs) / 2)
                    
        except:

            #done = True
            PrintException()
            self.creates[fut] = False
            done = True
            sleep(self.orderRateLimit / 1000)
    def cancel_them( self, oid, fut ):
        done = False
        #print('cancel ' + fut)
        while done == False:
            try:
                #await self.asyncio.sleep(self.orderRateLimit / 1000)
                if self.goforit == True and self.goforit2 == True:
                    self.goforit = False
                    #self.num_threads = #self.num_threads + 1
                    t = threading.Timer(self.orderRateLimit / 1000, self.resetGoforit)
                    t.daemon = True
                    t.start()
                    #if fut not in margins:
                    c = self.client.cancelOrder( oid , fut )
                    print(c)
                    #else:
                     #   result = self.client3.cancel_margin_order(
                      ##      symbol=fut.replace('/',''),
                      #      orderId=oid)

                    done = True
                    self.cancels[fut] = False
                else:
                    done = True

                    sleep(self.orderRateLimit / 1000* len(self.pairs) / 2)
                    
            except Exception as e:
                done = True
                self.cancels[fut] = False
                if 'Unknown order sent' not in str(e):
                    PrintException()
                    sleep(self.orderRateLimit / 1000)
                    if self.client.apiKey == self.firstkey:
                        abc=123#abc=123#self.pprint(fut + ' cancel exception!')
                else:
                    orders = [ o for o in self.openorders[fut] ]
                    for order in orders:
                        if oid == order['id']:
                            self.openorders[fut].remove(order)
                            #abc=123#self.pprint('removing ' + fut)
                #PrintException()
                
                #self.logger.warn( 'Order cancellations failed: %s' % oid )x
    def batch_delete_orders ( self, fut, cancel_oids, orig_ids ):
        try:
            serialize_to_string = "[{}]".format(','.join(map(str, cancel_oids)))
            order_id_list_encoded = urllib.parse.urlencode({'value': serialize_to_string}).replace('value=', '')
            serialize_to_string2 = "[{}]".format(','.join(map(str, orig_ids)))
            order_id_list_encoded2 = urllib.parse.urlencode({'value': serialize_to_string2}).replace('value=', '')
            orders = self.client.encode_uri_component(self.client.json(cancel_oids), safe=",")
            abc=123#print(order_id_list_encoded)
            abc=123#print(orders)
            abc=123#print({
            #    'symbol': fut.replace('/',''),
            #    'orderIdList': order_id_list_encoded
           # })
            for oid in cancel_oids: 
                #if fut not in margins:
                c = self.client.cancelOrder( oid , fut )
                print(c)
                #else:
                 #   result = self.client3.cancel_margin_order(
                  #      symbol=fut.replace('/',''),
                   #     orderId=oid)

            #response = self.client.apiPrivateDeleteBatchOrders({
            #    'symbol': fut.replace('/',''),
            #    'orderIdList': order_id_list_encoded
            #})
            
            abc=123#print(response)
        except:
            PrintException()   