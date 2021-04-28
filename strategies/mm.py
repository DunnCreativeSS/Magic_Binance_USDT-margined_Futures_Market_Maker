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
class Place_Orders( object ):
    def __init__( self, BinanceSocketManager, process_m_message, Client, random, pprint, firstkey, lev, bm, client, multiprocessing, brokerKey, qty_div, orderRateLimit, max_skew_mult, get_precision, math, TP, SL, asyncio, sleep, threading, PrintException, ticksize_floor, ticksize_ceil, pairs, fifteens, tens, fives, threes, con_size, get_spot, equity_btc, positions, get_ticksize, vols, get_bbo, openorders, equity_usd, randomword, logger, PCT_LIM_LONG, PCT_LIM_SHORT, DECAY_POS_LIM, MIN_ORDER_SIZE, CONTRACT_SIZE, MAX_LAYERS, BTC_SYMBOL, RISK_CHARGE_VOL, BP ):
        self.BP = BP
        self.TP = TP
        self.SL = SL
        self.twosecsblock = {}
        self.BinanceSocketManager = BinanceSocketManager
        self.process_m_message = process_m_message
        self.Client = Client
        self.pprint = pprint
        self.lbo = {}
        self.lao = {}
        self.ask_ords = {}
        self.bid_ords = {}
        self.lev = lev
        self.firstkey = firstkey
        self.multiprocessing = multiprocessing
        self.brokerKey = brokerKey
        self.get_precision = get_precision
        self.math = math
        self.pairs = pairs
        self.qty_div = qty_div
        self.max_skew_mult = max_skew_mult
        self.creates = {}
        self.edits = {}
        self.editOs = []
        self.cancels = {}
        self.goforit = True
        self.goforit2 = True
        self.slBlock = {}
        self.tradeBlock = {}
        for fut in self.pairs:
            self.cancels[fut] = False
            self.creates[fut] = False
            self.edits[fut] = False
            self.slBlock[fut] = False
            self.tradeBlock[fut] = False
            self.lbo[fut] = 0
            self.lao[fut] = 0
            self.ask_ords[fut] = []
            self.bid_ords[fut] = []
        self.sleep = sleep
        self.trades = {}
        self.asyncio = asyncio
        self.threading = threading
        self.start_threads = None
        self.num_threads = 0
        self.PrintException = PrintException
        self.ticksize_ceil = ticksize_ceil
        self.ticksize_floor = ticksize_floor
        self.PCT_LIM_LONG = PCT_LIM_LONG
        self.PCT_LIM_SHORT = PCT_LIM_SHORT
        self.DECAY_POS_LIM = DECAY_POS_LIM
        self.MIN_ORDER_SIZE = MIN_ORDER_SIZE
        self.CONTRACT_SIZE = CONTRACT_SIZE
        self.MAX_LAYERS = MAX_LAYERS
        self.BTC_SYMBOL = BTC_SYMBOL
        self.RISK_CHARGE_VOL = RISK_CHARGE_VOL

        self.fifteens = fifteens
        self.tens = tens
        self.fives = fives
        self.threes = threes
        self.con_size = con_size
        self.get_spot = get_spot
        self.client = client
        self.ordersTo = []
        print('placekey: ' + self.client.apiKey)
        self.get_ticksize = get_ticksize
        self.get_bbo = get_bbo
        self.randomword = randomword
        self.random = random
        self.logger = logger

        self.orderRateLimit = orderRateLimit
        self.openorders = openorders
        self.vols = vols
        self.equity_btc = equity_btc
        self.equity_usd = equity_usd
        self.positions = positions
        self.new_thread = True
        #conn_key = bm.start_multiplex_socket(['!ticker@arr'], self.process_m_message)
        self.bm = bm

        
        # then start the socket manager
        #self.bm.start()
    
        
    def start_user_thread(self):
    
        
        while True:
            try:
                """
                self.new_thread = False
                self.pprint('test ws...')
                self.sleep(60)
                if self.new_thread == False:
                    self.pprint('new websockets then...')
                    self.bm.close()
                    self.sleep(4)
                    bin_client = self.Client(self.client.apiKey, self.client.secret)
                    #bm = self.BinanceSocketManager(bin_client, n=self.client.apiKey, user_timeout=60)
                    self.bm = self.BinanceSocketManager(bin_client, n=self.client.apiKey, user_timeout=60)
                    # start any sockets here, i.e a trade socket
                    #
                    
                    #if client.apiKey == firstkey:
                    #conn_key = bm.start_multiplex_socket(['!bookTicker'], self.process_m_message)
                    # then start the socket manager
                    #bm.start()
                    self.user_thread = self.bm.start_user_socket(self.process_message)
                    self.bm.start()
                """
            except:
                self.PrintException()
    def process_message(self, msg):
        abc=123
    def update_positions( self ):
        while True:
            try:
                
                positions       = self.client.fapiPrivateGetPositionRisk()
                #print('lala')
                #print(positions)
                
                for pos in positions:
                    pair = pos['symbol'].replace('USDT', '/USDT')
                    if pair in self.pairs:
                        pos['positionAmt'] = float(pos['positionAmt'])
                        pos['entryPrice'] = float(pos['entryPrice'])
                        pos['unRealizedProfit'] = float(pos['unRealizedProfit'])
                        pos['leverage'] = float(self.lev)
                        pos['notional'] = float(pos['notional'])
                        notional = self.math.fabs(pos['positionAmt']) * pos['entryPrice']
                        #fee = self.feeRate * notional
                        #notional = notional - fee
                        if notional > 0:
                            notionalplus = notional + pos['unRealizedProfit']
                            percent = ((notionalplus / notional) -1) * 100

                            pos['ROE'] = percent * pos['leverage']
                        else:
                            pos['ROE'] = 0
                        self.positions[ pair] = pos
                self.sleep(1)
            except:
                self.PrintException(self.client.apiKey)
                self.sleep(1)
    def update_orders(self):
        while True:
            data        = self.client.fapiPrivateGetOpenOrders()
            for fut in self.openorders:
                self.openorders[fut] = []
            print(data)
            for o in data:
                fut = o['symbol'].replace('USD', '/USD')
                o['id'] = int(o['orderId'])
                if fut not in self.openorders:
                    self.openorders[fut] = []
                
                self.openorders[fut].append(o)
            for fut in self.pairs:
                #fut = fut
                try:
                    if len(self.openorders[fut]) > 0:
                        self.pprint('lenopenorders ' + fut + ': ' + str(len(self.openorders[fut])))
                    ask_ords        = [ o for o in self.openorders[fut] if o['side'].upper() == 'SELL'  ] 
                    bid_ords        = [ o for o in self.openorders[fut] if o['side'].upper() == 'BUY'  ]
                    #if 'BAT' in fut:
                    #    for o in self.openorders[fut]:
                    #        self.pprint(o)
                    self.ask_ords[fut] = ask_ords
                    self.bid_ords[fut] = bid_ords
                    self.lbo[fut] = len(bid_ords)
                    self.lao[fut] = len(ask_ords)
                    cancel_oids = []
                    orig_ids = []
                    if 3 < len( bid_ords ):
                        cancel_oids += [ int(o['id']) for o in bid_ords[ 3 : ]]
                        orig_ids += [ (o['clientOrderId']) for o in bid_ords[ 3 : ]]
                    if 3 < len( ask_ords ):
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
                            self.pprint(self.client.apiKey + ': cancel '  + fut + ': from ' + str(len(bid_ords)) + ' bid_ords and ' + str(len(ask_ords)) + ' asks, cancelling: ' + str(len(cancel_oids)))
                            #self.pprint({'symbol': fut, 'orderIdList': cancel_oids})
                            
                            t = self.threading.Thread(target=self.batch_delete_orders, args=(fut, cancel_oids, orig_ids))
                            t.daemon = True
                            t.start()
                            self.cancels[fut] = False
                            for oid in cancel_oids:
                                for order in self.openorders[fut]:
                                    if oid == order['id']:
                                        self.openorders[fut].remove(order)
                           # self.pprint(cancel)

                        if 'BAT' in fut:# and self.firstkey == self.client.apiKey:
                            bat = len(self.bid_ords['BAT/USDT']) + len(self.ask_ords['BAT/USDT'])
                            #if len(self.bid_ords['BAT/USDT']) > self.MAX_LAYERS or len(self.ask_ords['BAT/USDT']) > self.MAX_LAYERS:
                            ran = self.random.randint(0, 50)
                            #print(ran)
                            if ran < 2:
                                self.pprint(self.client.apiKey + ': lenorders BAT ' + str(bat))
                                #self.pprint(self.client.apiKey + ': lenaskorders BAT ' + str(len(self.ask_ords['BAT/USDT'])))
                    except Exception as e:
                        self.pprint('leno' + str(e))
                        self.PrintException(self.client.apiKey)
                        self.cancels[fut] = False
                except Exception as e:
                    self.pprint('leno' + str(e))
                    self.PrintException(self.client.apiKey)  
            self.sleep(self.orderRateLimit / 1000 * 40)#len(self.pairs) / 2) 
            
    def batch_delete_orders ( self, fut, cancel_oids, orig_ids ):
        try:
            serialize_to_string = "[{}]".format(','.join(map(str, cancel_oids)))
            order_id_list_encoded = urllib.parse.urlencode({'value': serialize_to_string}).replace('value=', '')
            serialize_to_string2 = "[{}]".format(','.join(map(str, orig_ids)))
            order_id_list_encoded2 = urllib.parse.urlencode({'value': serialize_to_string2}).replace('value=', '')
            orders = self.client.encode_uri_component(self.client.json(cancel_oids), safe=",")
            print(order_id_list_encoded)
            print(orders)
            print({
                'symbol': fut.replace('/',''),
                'orderIdList': order_id_list_encoded
            })

            response = self.client.fapiPrivateDeleteBatchOrders({
                'symbol': fut.replace('/',''),
                'orderIdList': order_id_list_encoded
            })
            
            print(response)
        except:
            self.PrintException(self.client.apiKey)                
    def run( self ):
        t = self.threading.Thread(target=self.update_orders, args=())
        t.daemon = True
        t.start()
        self.num_threads = self.num_threads + 1
        t = self.threading.Thread(target=self.update_positions, args=())
        t.daemon = True
        t.start()
        self.num_threads = self.num_threads + 1
        while  True:
            try:
                """
                t.start()
                t = self.threading.Thread(target=self.start_user_thread, args=())
                t.daemon = True
                self.num_threads = self.num_threads + 1
                t.start()
                """
                t = self.threading.Thread(target=self.failSafeReset, args=())
                t.daemon = True
                self.num_threads = self.num_threads + 1
                t.start()
                
            except:
                self.PrintException(self.client.apiKey)
            while True:
                try:
                    self.start_threads = self.threading.active_count() 
                    if self.client.apiKey == self.firstkey:
                        self.pprint(self.client.apiKey + ': start thread place_orders: ' + str(self.start_threads))
                    for fut in self.pairs:
                        try:
                            t = self.threading.Thread(target=self.place_orders, args=(fut,))
                            t.daemon = True
                            
                            t.start()
                        except:
                            self.PrintException(self.client.apiKey)
                    done = False
                    while done == False:
                        num_threads = self.threading.active_count()  - self.num_threads
                        if self.client.apiKey == self.firstkey:
                            abc=123#self.pprint('num thread place_orders: ' + str(num_threads) + ' and self.num_threads: ' + str(self.num_threads))
                        if num_threads < self.start_threads + len(self.pairs) / 3:
                            done = True
                            abc=123#self.pprint('restart threads...')
                            self.sleep(5)
                        else:
                            self.sleep(5)
                except:
                    self.PrintException(self.client.apiKey)
    def failSafeReset( self ):
        while True:
            try:
                t = self.threading.Timer(5, self.resetGoforit)
                t.daemon = True
                self.num_threads = self.num_threads + 1
                t.start()
                self.sleep(5)
            except:
                self.PrintException(self.client.apiKey)
                self.sleep(5)
        proc = self.threading.Thread(target=self.failSafeReset, args=())
        abc=123#self.pprint('4 proc')
        proc.start()
        proc.terminate() 
        sleep(5) 
    def resetGoforit2( self ):
        try:
            self.goforit2 = True
            self.pprint(self.client.apiKey + ': self.goforit2')
            self.num_threads = self.num_threads - 1

            return
        except:
            proc = self.threading.Thread(target=self.resetGoforit2, args=())
            self.PrintException(self.client.apiKey)
            
    def resetGoforit( self ):
        try:
            self.goforit = True
            #self.pprint(self.goforit)
            self.num_threads = self.num_threads - 1

            return
        except:
            proc = self.threading.Thread(target=self.resetGoforit, args=())
            abc=123#self.pprint('6 proc')
            proc.start()
            proc.terminate() 
            sleep(5)
    def tradeUnblock( self, fut ):
        self.sleep(2)
        #self.pprint('unblock trade ' + fut)
        self.tradeBlock[fut] = False
    def slUnblock( self, fut ):
        self.sleep(60)# * 60)
        self.pprint(self.client.apiKey + ': unblock sl ' + fut)
        self.slBlock[fut] = False
    def place_orders( self, fut ):

        
        
        con_sz  = self.con_size        
        
        
        while True:
            
            try:
                try:    

                    #self.pprint(fut + ': ' + str(self.positions[fut]['ROE']))
                    if self.positions[fut]['ROE'] > self.TP and self.positions[fut]['ROE'] != 0:
                        
                        #sleep(10)
                        direction = 'sell'
                        if float(self.positions[fut]['positionAmt']) < 0:
                            direction = 'buy'
                        qty = self.math.fabs(float(self.positions[fut]['positionAmt']))
                        #self.creates[fut] = True
                        if qty > 5:
                            if self.client.apiKey == self.firstkey:
                                self.pprint(self.client.apiKey + ': ' + fut + ' takeprofit! ' + str(self.positions[fut]['ROE']) + ' dir: ' + direction + ' qty ' + str(qty))
                        
                            if self.client.apiKey == self.firstkey:
                                abc=123#self.pprint(str(qty) + ' ' + fut)
                            try:
                                o = self.client.createOrder(fut, "Market", direction, qty, None, {"newClientOrderId":"x-" + self.brokerKey + "-" + self.randomword(20)})
                                
                                #print(o)
                                #self.create_order(  fut, "Market", direction, qty, None, "GTC","x-" + self.brokerKey + "-" + self.randomword(20))
                            except Exception as e:
                                self.PrintException(self.client.apiKey)
                                self.pprint(e)
                        self.positions[fut]['ROE'] = 0
                    if self.positions[fut]['ROE'] < self.SL and self.positions[fut]['ROE'] != 0:
                        
                        direction = 'sell'
                        if float(self.positions[fut]['positionAmt']) < 0:
                            direction = 'buy'
                        qty = self.math.fabs(float(self.positions[fut]['positionAmt']))
                        #self.creates[fut] = True
                        if self.client.apiKey == self.firstkey:
                            abc=123#self.pprint(str(qty) + ' ' + fut)
                        self.slBlock[fut] = True
                        t = self.threading.Thread(target=self.slUnblock, args=(fut,))
                        t.daemon = True
                        t.start()
                        if qty > 5:
                            if self.client.apiKey == self.firstkey:
                                self.pprint(self.client.apiKey + ': ' + fut + ' stoploss! ' + str(self.positions[fut]['ROE']) + ' dir: ' + direction + ' qty ' + str(qty))
                        
                            try:
                                o = self.client.createOrder(fut, "Market", direction, qty, None, {"newClientOrderId":"x-" + self.brokerKey + "-" + self.randomword(20)})
                                #print(o)
                                #self.create_order(  fut, "Market", direction, qty, None, "GTC","x-" + self.brokerKey + "-" + self.randomword(20))
                            except Exception as e:
                                self.PrintException(self.client.apiKey)
                                self.pprint(e)
                        self.positions[fut]['ROE'] = 0
                except:
                    self.PrintException(self.client.apiKey)
                spot            = self.get_spot(fut)
                bal_btc         = self.equity_btc
                pos             = float(self.positions[ fut ][ 'notional' ])
                pos_lim_long    = bal_btc * self.PCT_LIM_LONG * 20 #/ len(self.futures)
                pos_lim_short   = bal_btc * self.PCT_LIM_SHORT * 20 #/ len(self.futures)
                #self.pprint(pos_lim_long)
                #expi            = self.futures[ fut ][ 'expi_dt' ]
                #tte             = max( 0, ( expi - datetime.utcnow()).total_seconds() / SECONDS_IN_DAY )
                pos_decay       = 1.0 - self.math.exp( -self.DECAY_POS_LIM * 8035200 )
                pos_lim_long   *= pos_decay
                pos_lim_short  *= pos_decay
                pos_lim_long   -= pos
                pos_lim_short  += pos
                pos_lim_long    = max( 0, pos_lim_long  )
                pos_lim_short   = max( 0, pos_lim_short )
                
                min_order_size_btc = (self.MIN_ORDER_SIZE * self.CONTRACT_SIZE) / spot
                #self.pprint(min_order_size_btc) #0.0006833471711135484 0.08546200188472201
                qtybtc  = 1 / spot #(bal_btc * 20 / 500) / len(pairs)

                nbids   = self.MAX_LAYERS + 1#min( self.math.trunc( pos_lim_long  / qtybtc ), self.MAX_LAYERS )
                nasks   = self.MAX_LAYERS + 1 #min( self.math.trunc( pos_lim_short / qtybtc ), self.MAX_LAYERS )
                
                place_bids = nbids > 0
                place_asks = nasks > 0
                
                if not place_bids and not place_asks:
                    abc=123#self.pprint( 'No bid no offer for %s' % fut, min_order_size_btc )
                    continue
                    
                
                #self.pprint(fut)
                #self.pprint('asks')
                #self.pprint(ask_mkt)
                #self.pprint(asks)
                #self.pprint('bids')
                #self.pprint(bid_mkt)
                #self.pprint(bids)
                
                
                for i in range( max( nbids, nasks)):
                    # BIDS
                    
                    tsz = float(self.get_ticksize( fut ))            
                    # Perform pricing
                    vol = max( self.vols[ self.BTC_SYMBOL ], self.vols[ fut ] )
                    eps         = self.BP * vol * self.RISK_CHARGE_VOL
                    riskfac     = self.math.exp( eps )
                    bbo     = self.get_bbo( fut )
                    bid_mkt = bbo[ 'bid' ]
                    ask_mkt = bbo[ 'ask' ]

                    MKT_IMPACT          =  0.01
                    MKT_IMPACT          *= self.BP
                    if 'XLM' in fut and self.client.apiKey == self.firstkey:
                        abc=123#self.pprint(bbo)
                    if bid_mkt is None and ask_mkt is None:
                        bid_mkt = ask_mkt = spot
                    elif bid_mkt is None:
                        bid_mkt = min( spot, ask_mkt )
                    elif ask_mkt is None:
                        ask_mkt = max( spot, bid_mkt )
                    mid_mkt = 0.5 * ( bid_mkt + ask_mkt )
                    #if 'TRX' in fut:
                        #print('lenords ' + fut + ': ' + str(len(self.openorders[fut])))
                    try:
                        ords        = self.openorders[fut]
                    except:
                        ords = []
                    cancel_oids = []
                    bid_ords    = ask_ords = []
                    
                    if place_bids:
                        
                        bid_ords        = [ o for o in ords if o['side'].upper() == 'BUY'  ]
                        #self.pprint(len(bid_ords))
                        len_bid_ords    = ( len( bid_ords ))
                        bid0            = bid_mkt#mid_mkt * self.math.exp( -MKT_IMPACT )
                        
                        bids    = [ bid0 * 1 + (0.001 * -i) for i in range( 0, nbids + 1 ) ]
                        #bids    = [ bid0 * riskfac ** -i for i in range( 1, nbids + 1 ) ]
                        bidsn2 = []
                        bidsn2.append(bid0)
                        for p in bids:
                            bidsn2.append(p)
                        bids = bidsn2
                        bids[ 0 ]   = self.ticksize_floor( bids[ 0 ], tsz )
                        
                        print(bids)
                        for a in bids:
                            diff = a / bids[0]
                            diff = diff - 1
                            diff = diff * 100
                            self.pprint('diff bid ' + fut + ': ' + str(diff))
                        """
                        nbids2 = []
                        c = 0
                        for b in bids:
                            if c > 0:
                                nbids2.append(b)
                            c = c + 1
                        bids = nbids2
                        nbids = nbids- 1
                        bids[ 0 ]   = self.ticksize_floor( bids[ 0 ], tsz )
                        """
                        #print(bids)
                    if place_asks:
                        
                        ask_ords        = [ o for o in ords if o['side'].upper() == 'SELL' ]    
                        #self.pprint(len(ask_ords))
                        len_ask_ords    = ( len( ask_ords ) )
                        ask0            = ask_mkt#mid_mkt * self.math.exp(  MKT_IMPACT )
                        
                        asks    = [ ask0 * 1 + (0.001 * i) for i in range( 0, nasks + 1 ) ]
                        #print(asks)
                        #asks    = [ ask0 * riskfac ** i for i in range( 1, nasks + 1 ) ]
                        asksn2 = []
                        asksn2.append(ask0)
                        for p in asks:
                            asksn2.append(p)
                        asks = asksn2
                        asks[ 0 ]   = self.ticksize_ceil( asks[ 0 ], tsz  )
                        print(asks)
                        for a in asks:
                            diff = a / asks[0]
                            diff = diff - 1
                            diff = diff * 100
                            self.pprint('diff ask ' + fut + ': ' + str(diff))
                        """
                        nasks2 = []+++
                        c = 0
                        for b in asks:+++++++
                            if c > 0:
                                nasks2.append(b)
                            c = c + 1
                        asks = nasks2
                        nasks = nasks - 1
                        asks[ 0 ]   = self.ticksize_floor( asks[ 0 ], tsz )
                        """
                    bprices = []
                    aprices = []
                    for bid in bid_ords:
                        bprices.append(float(bid['price']))
                    for ask in ask_ords:
                        aprices.append(float(ask['price']))
                    if place_bids and i < nbids:

                        if i > 0:
                            prc = self.ticksize_floor( min( bids[ i], bids[ i - 1 ] - tsz ), tsz )
                        else:
                            prc = bids[ 0 ]

                        qty = ((self.equity_usd * float(self.lev)) * relativeOrderSizes[fut] / float(self.qty_div)) / prc  #/ self.qty_div / 6) / prc#round( prc * qtybtc )   / spot                     
                        if qty * prc < 6:
                            qty = 6 / prc
                        max_skew = qty * prc * self.max_skew_mult
                        self.pprint('i lbo: ' + str(i) + ' ' + str(len_bid_ords))
                        if i < len_bid_ords:    

                            oid = bid_ords[ i ]['id']
                            clientOrderId = bid_ords[ i ]['clientOrderId']
                            oid = float(oid)
                            #self.pprint(oid)
                            try:
                                
                                if fut not in self.twosecsblock:
                                    self.twosecsblock[fut] = {}
                                if i not in self.twosecsblock[fut]:
                                    self.twosecsblock[fut][i] = False
                                if prc not in bprices and self.twosecsblock[fut][i] == False and self.slBlock[fut] == False:
                                    #print('qtye: ' + str(qty))
                                    
                                    self.edits[fut] = True
                                    self.pprint('vol edit buy: ' + str(prc))
                                    
                                    e = self.edit_order( clientOrderId, oid, fut, "Limit", "buy", qty, prc, "x-" + self.brokerKey + "-" + self.randomword(20) )
                                    print(e)
                                    self.twosecsblock[fut][i] = True
                                    t = self.threading.Thread(target=self.twosecsreset, args=(fut, i))
                                    t.daemon = True
                                    t.start()
                                elif  self.edits[fut] == False and self.slBlock[fut] == False and  self.twosecsblock[fut][i] == False :
                                    self.pprint('vol edit inbprices ' + str(prc) + ' in bprices!')
                                elif self.edits[fut] == True:
                                    self.pprint('vol edit selfedits true ' + fut)
                                elif self.slBlock[fut] == True:
                                    self.pprint('vol edit selfslblock true ' + fut)
                            except Exception as e:
                                self.PrintException(self.client.apiKey)     
                        else:
                            #self.pprint(qty * prc)
                            try:
                                if 'CHZ' in fut:
                                    print(float(self.positions[fut]['notional']))
                                    print(qty)

                                    print(float(self.positions[fut]['notional']) <= qty * prc * self.max_skew_mult)
                                if qty * prc > 5:
                                    if fut not in self.twosecsblock:
                                        self.twosecsblock[fut] = {}
                                    
                                    if i not in self.twosecsblock[fut]:
                                        self.twosecsblock[fut][i] = False
                                    if float(self.positions[fut]['notional']) <= qty *prc * self.max_skew_mult  and self.twosecsblock[fut][i] == False and self.creates[fut] == False and self.slBlock[fut] == False and self.tradeBlock[fut] == False and self.lbo[fut] <= 2:
                                        #print('qty1: ' + str(qty))
                                        #self.creates[fut] = True
                                        if 'HOT' in fut:
                                            print('vol new buy: ' + str(prc))
                                        o = self.create_order(  fut, "Limit", 'buy', qty, prc, "GTX", "x-" + self.brokerKey + "-" + self.randomword(20))
                                        #print(o)
                                        #self.num_threads = self.num_threads + 1
                                        self.twosecsblock[fut][i] = True
                                        t = self.threading.Thread(target=self.twosecsreset, args=(fut, i))
                                        t.daemon = True
                                        t.start()
                                    elif float(self.positions[fut]['notional']) > qty *prc * self.max_skew_mult :
                                        self.pprint(fut + ' not buying maxskew, pos: ' + str(float(self.positions[fut]['notional'])) + ' mod: ' + str(qty * prc *  self.max_skew_mult))
                                    """
                                    if self.lbo[fut] > self.MAX_LAYERS and i > self.MAX_LAYERS:
                                        t = self.threading.Thread(target=self.cancel_them, args=(self.bid_ords[fut][ i - 1 ]['id'], fut,))
                                        t.daemon = True
                                        t.start()
                                    """
                            except Exception as e:
                                self.PrintException(self.client.apiKey)
                                #self.logger.warn( 'Bid order failed: %s bid for %s'
                                #                    % ( prc, qty ))

                    # OFFERS

                    if place_asks and i < nasks :

                        if i > 0:
                            prc = self.ticksize_ceil( max( asks[ i ], asks[ i - 1 ] + tsz ), tsz )
                        else:
                            prc = asks[ 0 ]
                            
                        qty = ((self.equity_usd * float(self.lev)) * relativeOrderSizes[fut] / float(self.qty_div)) / prc  # / self.qty_div / 6) / prc#round( prc * qtybtc ) / spot
                        if qty * prc < 6:
                            qty = 6 / prc
                        self.pprint('i lbo: ' + str(i) + ' ' + str(len_ask_ords))
                        if i < len_ask_ords:
                            oid = ask_ords[ i ]['id']
                            clientOrderId = ask_ords[ i ]['clientOrderId']
                            oid = float(oid)
                            #self.pprint(oid)
                            try:
                                
                                if fut not in self.twosecsblock:
                                    self.twosecsblock[fut] = {}
                                
                                if i not in self.twosecsblock[fut]:
                                    self.twosecsblock[fut][i] = False
                                if prc not in aprices  and self.twosecsblock[fut][i] == False and self.slBlock[fut] == False:
                                    #print('qtye2: ' + str(qty))
                                    self.edits[fut] = True
                                    self.pprint('vol edit sell: ' + str(prc))
                                    e = self.edit_order( clientOrderId, oid, fut, "Limit", "sell", qty, prc,"x-" + self.brokerKey + "-" + self.randomword(20) )
                                    print(e)
                                    self.twosecsblock[fut][i] = True
                                    t = self.threading.Thread(target=self.twosecsreset, args=(fut, i))
                                    t.daemon = True
                                    t.start()
                                elif self.edits[fut] == False and self.slBlock[fut] == False and  self.twosecsblock[fut][i] == False :
                                    self.pprint('vol edit inbprices ' + str(prc) + ' in bprices!')
                                
                                elif self.edits[fut] == True:
                                    self.pprint('vol edit selfedits true ' + fut)
                                elif self.slBlock[fut] == True:
                                    self.pprint('vol edit selfslblock true ' + fut)
                                
                            except Exception as e:
                                self.PrintException(self.client.apiKey)

                        else:
                            try: #1000 > -60 
                                if qty * prc > 5:
                                    if fut not in self.twosecsblock:
                                        self.twosecsblock[fut] = {}
                                        
                                    if i not in self.twosecsblock[fut]:
                                        self.twosecsblock[fut][i] = False
                                    if float(self.positions[fut]['notional']) >= qty * prc * self.max_skew_mult * -1  and self.twosecsblock[fut][i] == False and self.creates[fut] == False and self.slBlock[fut] == False and self.tradeBlock[fut] == False and self.lao[fut] <= 2:    
                                        #print('qty2: ' + str(qty))
                                        #self.creates[fut] = True
                                        o = self.create_order(  fut, "Limit", 'sell', qty, prc, "GTX", "x-" + self.brokerKey + "-" + self.randomword(20) )
                                        
                                        if 'HOT' in fut:
                                            print('vol new buy: ' + str(prc))
                                        #print(o)
                                        self.twosecsblock[fut][i] = True
                                        t = self.threading.Thread(target=self.twosecsreset, args=(fut, i))
                                        t.daemon = True
                                        t.start()
                                    elif float(self.positions[fut]['notional']) < qty * prc * self.max_skew_mult * -1:
                                        self.pprint(fut + ' not selling maxskew, pos: ' + str(float(self.positions[fut]['notional'])) + ' mod: ' + str(qty * prc *  self.max_skew_mult * -1))
                                    """
                                    if self.lao[fut] > self.MAX_LAYERS and i > self.MAX_LAYERS:
                                        t = self.threading.Thread(target=self.cancel_them, args=(self.ask_ords[fut][ i - 1 ]['id'], fut,))
                                        t.daemon = True
                                        t.start()
                                    """
                            
                            except Exception as e:
                                self.PrintException(self.client.apiKey)
                                #self.logger.warn( 'Offer order failed: %s at %s'
                                #                    % ( qty, prc ))

                
            except:
                self.PrintException(self.client.apiKey)
        proc = self.threading.Thread(target=self.place_orders, args=(fut,))
        abc=123#self.pprint('5 proc')
        proc.start()
        proc.terminate() 
        sleep(5)

    def edit_order( self, clientOrderId, oid, fut, type, dir, qty, prc, brokerPhrase ):
        done = False
        order = {
                "clientOrderId": clientOrderId,
                "id": oid,
                "symbol" : fut.replace('/',''),
                "side" : dir.upper(),
                "type" : type.upper(),
                "quantity": self.client.amount_to_precision(fut, qty),
                "price": self.client.price_to_precision(fut, prc),
                "newClientOrderId": brokerPhrase,
                "timeInForce": 'GTX'
            }
        self.editOs.append(order  )
        if len(self.editOs) >= 5:
            while done == False:
                try:


                    if self.goforit == True and self.goforit2 == True:
                        #self.pprint('edit ' + fut)
                        self.goforit = False
                        self.num_threads = self.num_threads + 1
                        t = self.threading.Timer(self.orderRateLimit / 1000 * 5, self.resetGoforit)
                        t.daemon = True
                        t.start()
                        #await self.asyncio.sleep(self.orderRateLimit / 1000)
                        self.num_threads = self.num_threads + 1
                        cancel_oids = []

                        orig_ids = []
                        for o in self.editOs:
                            if 'id' in o:
                                cancel_oids.append(int(o['id']))
                                orig_ids.append((o['clientOrderId']))
                                o.pop('id', None)
                        print('EXCEPTION' + str(cancel_oids))
                        print('EXCEPTION' + str(self.editOs))
                        d = self.batch_delete_orders(fut, cancel_oids, orig_ids)
                        orders = [self.client.encode_uri_component(self.client.json(order), safe=",") for order in self.editOs]


                        response = self.client.fapiPrivatePostBatchOrders({
                            'batchOrders': '[' + ','.join(orders [ : 5 ]) + ']'
                        })

                        #params = {
                        #    'batchOrders' : self.client.json(self.editOs)
                        #}

                        #orders = [self.client.encode_uri_component(self.client.json(order), safe=",") for order in self.editOs]
                        #response = self.client.fapiPrivatePostBatchOrders(params)
                        self.pprint('batchoed: ' + str(response))
                        #b = self.client.fapiPrivatePostBatchOrders( {'batchOrders': json.dumps(self.editOs).replace(', ', ',')})
                        #print(b)
                        print(d)
                        self.editOs = self.editOs[ 5 : ]
                        #self.client.editOrder( oid, fut, type, dir, qty, prc, params  )
                        if 'XLM' in fut  and self.client.apiKey == self.firstkey:
                            abc=123#self.pprint(fut + ' edited!')
                        done = True
                        self.edits[fut] = False
                    else:
                        #if 'XLM' in fut:
                        self.pprint(fut + ' edit blocked! ' + str(self.goforit) + ' ' + str(self.goforit2))
                        done = True
                        self.edits[fut] = False
                        self.sleep(self.orderRateLimit / 1000 * len(self.pairs) / 2)
                except Exception as e:
                    if 'Unknown order sent' not in str(e):
                        self.PrintException(self.client.apiKey)

                    if 'XLM' in fut  and self.client.apiKey == self.firstkey:
                        abc=123#self.pprint(fut + ' edit exception!')
                    self.edits[fut] = False
                    done = True
                    self.sleep(self.orderRateLimit / 1000)
    def create_order( self, fut, type, dir, qty, prc, tif, brokerPhrase ):
        
        
        try:
            order = {
                "symbol" : fut.replace('/',''),
                "side" : dir.upper(),
                "type" : type.upper(),
                "quantity": self.client.amount_to_precision(fut, qty),
                "price": self.client.price_to_precision(fut, prc),
                "newClientOrderId": brokerPhrase,
                "timeInForce": 'GTX'
            }
            if len(self.ordersTo) < 5:
                self.ordersTo.append(order)
            if len(self.ordersTo) >= 5:    
                if self.goforit == True and self.goforit2 == True :#and len(self.ordersTo) >= 5:
                    try:
                        #self.pprint('create ' + fut)
                        self.goforit = False
                        self.num_threads = self.num_threads + 1
                        t = self.threading.Timer((self.orderRateLimit / 1000) * 5, self.resetGoforit)
                        t.daemon = True
                        t.start()
                        exchange = self.client

                        #await self.asyncio.sleep(self.orderRateLimit / 1000)
                        
                        print(self.ordersTo)
                        print(len(self.ordersTo))
                        orders = [self.client.encode_uri_component(self.client.json(order), safe=",") for order in self.ordersTo]


                        response = self.client.fapiPrivatePostBatchOrders({
                            'batchOrders': '[' + ','.join(orders[ : 5 ]) + ']'
                        })



                        #params = {
                        #    'batchOrders' : self.client.json(self.ordersTo)
                        #}
                        #orders = [self.client.encode_uri_component(self.client.json(order), safe=",") for order in self.ordersTo]
                        #response = self.client.fapiPrivatePostBatchOrders(params)
                        self.pprint('batcho: ' + str(response))
                        
                        print('qty: ' + str(qty))
                        print('prc: ' + str(prc))
                        print('qty * prc: ' + str(qty * prc))
                        
                        #b = self.client.fapiPrivatePostBatchOrders( {'batchOrders': json.dumps(self.ordersTo).replace(', ', ',')})
                        #print(b)
                        self.ordersTo = self.ordersTo[ 5 : ]
                        #o = self.client.createOrder(fut, type, dir, qty, prc, {"timeInForce": 'GTX', "newClientOrderId": brokerPhrase} )
                        
                        #print(o)
                        if 'XLM' in fut and self.client.apiKey == self.firstkey:
                            abc=123#self.pprint(fut + ' ordered!')
                        done = True
                        
                        self.creates[fut] = False
                    except:
                        done = True
                        self.PrintException(self.client.apiKey)
                        self.ordersTo = []
                else:
                    #if 'XLM' in fut:
                        #self.pprint(fut + ' order blocked!')
                    done = True
                    self.sleep(self.orderRateLimit / 1000 * len(self.pairs) / 2)
                        
        except:
            if 'XLM' in fut and self.client.apiKey == self.firstkey:
                abc=123#self.pprint(fut + ' order exception!')
            #done = True
            self.PrintException(self.client.apiKey)
            self.creates[fut] = False
            done = True
            self.sleep(self.orderRateLimit / 1000)
    def twosecsreset( self, fut, i ):
        self.sleep(2)
        self.twosecsblock[fut][i] = False
    def cancel_them( self, oid, fut ):
        done = False
        
        while done == False:
            try:
                #await self.asyncio.sleep(self.orderRateLimit / 1000)
                if self.goforit == True and self.goforit2 == True:
                    self.goforit = False
                    self.num_threads = self.num_threads + 1
                    t = self.threading.Timer(self.orderRateLimit / 1000, self.resetGoforit)
                    t.daemon = True
                    t.start()
                    self.client.cancelOrder( oid , fut )
                    done = True
                    self.cancels[fut] = False
                else:
                    done = True

                    self.sleep(self.orderRateLimit / 1000* len(self.pairs) / 2)
                    
            except Exception as e:
                done = True
                self.cancels[fut] = False
                if 'Unknown order sent' not in str(e):
                    self.PrintException(self.client.apiKey)
                    self.sleep(self.orderRateLimit / 1000)
                    if self.client.apiKey == self.firstkey:
                        abc=123#self.pprint(fut + ' cancel exception!')
                else:
                    orders = [ o for o in self.openorders[fut] ]
                    for order in orders:
                        if oid == order['id']:
                            self.openorders[fut].remove(order)
                            #self.pprint('removing ' + fut)
                #self.PrintException(self.client.apiKey)
                
                #self.logger.warn( 'Order cancellations failed: %s' % oid )x