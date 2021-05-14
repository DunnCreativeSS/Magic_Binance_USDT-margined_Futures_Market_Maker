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
cpercs = {'BUSD': 0.28125, 'DAI': 0.0625, 'USDT': 0.3125, 'USDC': 0.1875, 'TUSD': 0.0625, 'PAX': 0.0625, 'SUSD': 0.03125}

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
class Place_Orders( object ):
    def __init__( self, rest_ws, random, pprint, firstkey, lev, multiprocessing, brokerKey, qty_div, orderRateLimit, max_skew_mult, get_precision, math, TP, SL, asyncio, sleep, threading, PrintException, ticksize_floor, ticksize_ceil, pairs, fifteens, tens, fives, threes, con_size, get_spot, equity_btc, positions, get_ticksize, vols, get_bbo, openorders, equity_usd, randomword, logger, PCT_LIM_LONG, PCT_LIM_SHORT, DECAY_POS_LIM, MIN_ORDER_SIZE, CONTRACT_SIZE, MAX_LAYERS, BTC_SYMBOL, RISK_CHARGE_VOL, BP ):
        self.BP = BP
        self.TP = TP
        self.SL = SL
        self.rest_ws = rest_ws
        self.twosecsblock = {}
        abc=123#self.pprint = pprint
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
        self.rest_ws.creates = {}
        self.rest_ws.edits = {}
        self.editOs = []
        self.rest_ws.cancels = {}
        self.slBlock = {}
        self.tradeBlock = {}
        for fut in self.pairs:
            self.rest_ws.cancels[fut] = False
            self.rest_ws.creates[fut] = False
            self.rest_ws.edits[fut] = False
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
        #self.rest_ws.client = client
        abc=123#print('placekey: ' + self.rest_ws.client.apiKey)
        self.get_ticksize = get_ticksize
        self.get_bbo = get_bbo
        self.randomword = randomword
        self.random = random
        self.logger = logger

        self.orderRateLimit = orderRateLimit
        self.vols = vols
        self.equity_btc = equity_btc
        self.equity_usd = equity_usd
        self.rest_ws.positions = positions
        self.new_thread = True
        #conn_key = bm.start_multiplex_socket(['!ticker@arr'], self.process_m_message)
        #self.bm = bm

        
        # then start the socket manager
        #self.bm.start()
    
        
    def start_user_thread(self):
        abc=123
    def process_message(self, msg):
        abc=123
    
                 
    def run( self ):
        
        while  True:
            try:
                """
                t.start()
                t = self.threading.Thread(target=self.start_user_thread, args=())
                t.daemon = True
                self.num_threads = self.num_threads + 1
                t.start()
                """
                
                
            except:
                self.PrintException()
            while True:
                try:
                    self.equity_usd = self.rest_ws.equity_usd
                    self.equity_btc = self.rest_ws.equity_btc
                    self.start_threads = self.threading.active_count() 
                    if self.rest_ws.client.apiKey == self.firstkey:
                        abc=123#self.pprint(self.rest_ws.client.apiKey + ': start thread place_orders: ' + str(self.start_threads))
                    for fut in self.pairs:
                        try:
                            print(fut)
                            t = self.threading.Thread(target=self.place_orders, args=(fut,))
                            t.daemon = True
                            
                            t.start()
                        except:
                            self.PrintException()
                    done = False
                    while done == False:
                        num_threads = self.threading.active_count()  - self.num_threads
                        if self.rest_ws.client.apiKey == self.firstkey:
                            abc=123#abc=123#self.pprint('num thread place_orders: ' + str(num_threads) + ' and self.num_threads: ' + str(self.num_threads))
                        if num_threads < self.start_threads + len(self.pairs) / 3:
                            done = True
                            abc=123#abc=123#self.pprint('restart threads...')
                            self.sleep(5)
                        else:
                            self.sleep(5)
                except:
                    self.PrintException()
    
    def tradeUnblock( self, fut ):
        self.sleep(2)
        #abc=123#self.pprint('unblock trade ' + fut)
        self.tradeBlock[fut] = False
    def slUnblock( self, fut ):
        self.sleep(60)# * 60)
        abc=123#self.pprint(self.rest_ws.client.apiKey + ': unblock sl ' + fut)
        self.slBlock[fut] = False
    def place_orders( self, fut ):

        
        
        con_sz  = self.con_size        
        
        
        while True:
            
            try:
                try:    
                    """
                    #abc=123#self.pprint(fut + ': ' + str(self.rest_ws.positions[fut]['ROE']))
                    if self.rest_ws.positions[fut]['ROE'] > self.TP and self.rest_ws.positions[fut]['ROE'] != 0:
                        
                        #sleep(10)
                        direction = 'sell'
                        if float(self.rest_ws.positions[fut]['positionAmt']) < 0:
                            direction = 'buy'
                        qty = self.math.fabs(float(self.rest_ws.positions[fut]['positionAmt']))
                        #self.rest_ws.creates[fut] = True
                    
                        if self.rest_ws.client.apiKey == self.firstkey:
                            abc=123#self.pprint(self.rest_ws.client.apiKey + ': ' + fut + ' takeprofit! ' + str(self.rest_ws.positions[fut]['ROE']) + ' dir: ' + direction + ' qty ' + str(qty))
                    
                        if self.rest_ws.client.apiKey == self.firstkey:
                            abc=123#abc=123#self.pprint(str(qty) + ' ' + fut)
                        try:
                            self.sleep(self.orderRateLimit / 1000)
                            o = self.rest_ws.create_order(fut, "Market", direction, qty, None, None, "x-" + self.brokerKey + "-" + self.randomword(20))
                            #fut, type, dir, qty, prc, tif, brokerPhrase )
                            #print(o)
                            #self.rest_ws.create_order(  fut, "Market", direction, qty, None, "GTC","x-" + self.brokerKey + "-" + self.randomword(20))
                        except Exception as e:
                            self.PrintException()
                            abc=123#self.pprint(e)
                        self.rest_ws.positions[fut]['ROE'] = 0
                    if self.rest_ws.positions[fut]['ROE'] < self.SL and self.rest_ws.positions[fut]['ROE'] != 0 and self.slBlock[fut] == False:
                        
                        direction = 'sell'
                        if float(self.rest_ws.positions[fut]['positionAmt']) < 0:
                            direction = 'buy'
                        qty = self.math.fabs(float(self.rest_ws.positions[fut]['positionAmt']))
                        #self.rest_ws.creates[fut] = True
                        if self.rest_ws.client.apiKey == self.firstkey:
                            abc=123#abc=123#self.pprint(str(qty) + ' ' + fut)
                        self.slBlock[fut] = True
                        t = self.threading.Thread(target=self.slUnblock, args=(fut,))
                        t.daemon = True
                        t.start()
                        if self.rest_ws.client.apiKey == self.firstkey:
                            abc=123#self.pprint(self.rest_ws.client.apiKey + ': ' + fut + ' stoploss! ' + str(self.rest_ws.positions[fut]['ROE']) + ' dir: ' + direction + ' qty ' + str(qty))
                    
                        try:
                            self.sleep(self.orderRateLimit / 1000)
                            o = self.rest_ws.create_order(fut, "Market", direction, qty, None, None, "x-" + self.brokerKey + "-" + self.randomword(20))
                            #print(o)
                            #self.rest_ws.create_order(  fut, "Market", direction, qty, None, "GTC","x-" + self.brokerKey + "-" + self.randomword(20))
                        except Exception as e:
                            self.PrintException()
                            abc=123#self.pprint(e)
                        self.rest_ws.positions[fut]['ROE'] = 0

                    """
                except:
                    self.PrintException()

                spot            = self.get_spot(fut)
                bal_btc         = self.equity_btc
                try:
                    pos             = float(self.rest_ws.positions[ fut.split('/')[0] ][ 'notional' ])
                except:
                    pos = 0
                pos_lim_long    = bal_btc * self.PCT_LIM_LONG * 20 #/ len(self.futures)
                pos_lim_short   = bal_btc * self.PCT_LIM_SHORT * 20 #/ len(self.futures)
                #abc=123#self.pprint(pos_lim_long)
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
                #abc=123#self.pprint(min_order_size_btc) #0.0006833471711135484 0.08546200188472201
                qtybtc  = 1 / spot #(bal_btc * 20 / 500) / len(pairs)

                nbids   = self.MAX_LAYERS #min( self.math.trunc( pos_lim_long  / qtybtc ), self.MAX_LAYERS )
                nasks   = self.MAX_LAYERS  #min( self.math.trunc( pos_lim_short / qtybtc ), self.MAX_LAYERS )
                
                place_bids = nbids > 0
                place_asks = nasks > 0
                
                if not place_bids and not place_asks:
                    abc=123#abc=123#self.pprint( 'No bid no offer for %s' % fut, min_order_size_btc )
                    continue
                    
                
                #abc=123#self.pprint(fut)
                #abc=123#self.pprint('asks')
                #abc=123#self.pprint(ask_mkt)
                #abc=123#self.pprint(asks)
                #abc=123#self.pprint('bids')
                #abc=123#self.pprint(bid_mkt)
                #abc=123#self.pprint(bids)
                
                 # BIDS
                
                for i in range( max( nbids, nasks)):
                        
                    tsz = float(self.get_ticksize( fut ))  / 10
                    # Perform pricing
                    vol = max( self.vols[ self.BTC_SYMBOL ], self.vols[ fut ] )
                    eps         = self.BP * vol * self.RISK_CHARGE_VOL
                    riskfac     = self.math.exp( eps )
                    bbo     = self.get_bbo( fut )
                    bid_mkt = bbo[ 'bid' ]
                    ask_mkt = bbo[ 'ask' ]

                    MKT_IMPACT          =  0.01
                    MKT_IMPACT          *= self.BP
                    if 'OCEAN' in fut:
                        print([bid_mkt, ask_mkt])
                    if bid_mkt is None and ask_mkt is None:
                        bid_mkt = ask_mkt = spot
                    elif bid_mkt is None:
                        bid_mkt = min( spot, ask_mkt )
                    elif ask_mkt is None:
                        ask_mkt = max( spot, bid_mkt )
                    mid_mkt = 0.5 * ( bid_mkt + ask_mkt )
                    #if 'TRX' in fut:
                        #print('lenords ' + fut + ': ' + str(len(self.rest_ws.openorders[fut])))
                    try:
                        ords        = self.rest_ws.openorders[fut]
                    except:
                        ords = []
                    cancel_oids = []
                    bid_ords    = ask_ords = []
                    
                    if place_bids:
                        
                        bid_ords        = [ o for o in ords if o['side'].upper() == 'BUY'  ]
                        #abc=123#self.pprint(len(bid_ords))
                        len_bid_ords    = ( len( bid_ords ))
                        bid0            = bid_mkt#mid_mkt * self.math.exp( -MKT_IMPACT )
                        
                        bids    = [ bid0 * 1 + (0.001 * -i) for i in range( 1, nbids + 1 ) ]
                        #bids    = [ bid0 * riskfac ** -i for i in range( 1, nbids + 1 ) ]
                        bidsn2 = []
                        bidsn2.append(bid0)
                        c = 1
                        for p in bids:
                            if c <= 3 and c > 1:
                                bidsn2.append(p)
                            c = c + 1
                        bids = bidsn2
                        bids[ 0 ]   = self.ticksize_floor( bids[ 0 ] * 1 + (0.0001 * 0), tsz )
                        
                        abc=123#print(bids)
                        for a in bids:
                            diff = a / bids[0]
                            diff = diff - 1
                            diff = diff * 100
                            #print('diff bid ' + fut + ': ' + str(diff))
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
                        #abc=123#self.pprint(len(ask_ords))
                        len_ask_ords    = ( len( ask_ords ) )
                        ask0            = ask_mkt#mid_mkt * self.math.exp(  MKT_IMPACT )
                        
                        asks    = [ ask0 * 1 + (0.001 * i) for i in range( 1, nasks + 1 ) ]
                        #print(asks)
                        #asks    = [ ask0 * riskfac ** i for i in range( 1, nasks + 1 ) ]
                        asksn2 = []
                        asksn2.append(ask0)
                        c = 1
                        for p in asks:
                            if c <= 3 and c > 1:
                                asksn2.append(p)
                            c = c + 1
                        asks = asksn2
                        asks[ 0 ]   = self.ticksize_ceil( asks[ 0 ]  * 1 + (0.0001 * 0) , tsz  )
                        abc=123#print(asks)
                        for a in asks:
                            diff = a / asks[0]
                            diff = diff - 1
                            diff = diff * 100
                           # print('diff ask ' + fut + ': ' + str(diff))
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
                    if False:#len_bid_ords > 0 or len_ask_ords > 0:
                        print(fut)
                        print(bids)
                        print(asks)
                        print('lbo ' + str(len_bid_ords))
                        print('lao ' + str(len_ask_ords))
                        print(self.rest_ws.equity_usd)
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

                        qty = ((self.rest_ws.positions[fut.split('/')[1]]['notional']) / float(self.qty_div)) / prc  #/ self.qty_div / 6) / prc#round( prc * qtybtc )   / spot                     
                        #if qty * prc < 6:
                        #    qty = 6 / prc
                        qty = qty * cpercs[fut.split('/')[0]]
                        max_skew = qty * prc * self.max_skew_mult
                        abc=123#self.pprint('i lbo: ' + str(i) + ' ' + str(len_bid_ords))
                        if i < len_bid_ords:    

                            oid = bid_ords[ i ]['id']
                            clientOrderId = bid_ords[ i ]['clientOrderId']
                            oid = float(oid)
                            #abc=123#self.pprint(oid)
                            try:
                                
                                if fut not in self.twosecsblock:
                                    self.twosecsblock[fut] = {}
                                    self.twosecsblock[fut]['bids'] = {}
                                    self.twosecsblock[fut]['asks'] = {}
                                if i not in self.twosecsblock[fut]['bids']:
                                    self.twosecsblock[fut]['bids'][i] = False
                                if prc not in bprices:
                                    #print('qtye: ' + str(qty))
                                    
                                    self.rest_ws.edits[fut] = True
                                    abc=123#self.pprint('vol edit buy: ' + str(prc))
                                    self.sleep(self.orderRateLimit / 1000)
                                    e = self.rest_ws.edit_order( clientOrderId, oid, fut, "Limit", "buy", qty, prc, "x-" + self.brokerKey + "-" + self.randomword(20) )
                                    abc=123#print(e)
                                    if i > 0:
                                        self.twosecsblock[fut]['bids'][i] = True
                                    t = self.threading.Thread(target=self.twosecsresetb, args=(fut, i))
                                    t.daemon = True
                                    t.start()
                            except Exception as e:
                                self.PrintException()     
                        else:
                            #abc=123#self.pprint(qty * prc)
                            try:
                                if 'CHZ' in fut:
                                    abc=123#print(float(self.rest_ws.positions[fut]['notional']))
                                    abc=123#print(qty)

                                    abc=123#print(float(self.rest_ws.positions[fut]['notional']) <= qty * prc * self.max_skew_mult)
                                if qty * prc > 0.01:
                                    if fut not in self.twosecsblock:
                                        self.twosecsblock[fut] = {}
                                        
                                        self.twosecsblock[fut]['bids'] = {}
                                        self.twosecsblock[fut]['asks'] = {}
                                    if i not in self.twosecsblock[fut]['bids']:
                                        self.twosecsblock[fut]['bids'][i] = False
                                    if self.lbo[fut] <= 2:
                                        #print('qty1: ' + str(qty))
                                        #self.rest_ws.creates[fut] = True
                                        if 'HOT' in fut:
                                            abc=123#print('vol new buy: ' + str(prc))
                                        self.sleep(self.orderRateLimit / 1000)
                                        o = self.rest_ws.create_order(  fut, "Limit", 'buy', qty, prc, "GTX", "x-" + self.brokerKey + "-" + self.randomword(20))
                                        #print(o)
                                        #self.num_threads = self.num_threads + 1
                                        if i > 0:
                                            self.twosecsblock[fut]['bids'][i] = True
                                        t = self.threading.Thread(target=self.twosecsresetb, args=(fut, i))
                                        t.daemon = True
                                        t.start()
                                    elif float(self.rest_ws.positions[fut]['notional']) > qty *prc * self.max_skew_mult :
                                        abc=123#self.pprint(fut + ' not buying maxskew, pos: ' + str(float(self.rest_ws.positions[fut]['notional'])) + ' mod: ' + str(qty * prc *  self.max_skew_mult))
                                    """
                                    if self.lbo[fut] > self.MAX_LAYERS and i > self.MAX_LAYERS:
                                        t = self.threading.Thread(target=self.rest_ws.cancel_them, args=(self.bid_ords[fut][ i - 1 ]['id'], fut,))
                                        t.daemon = True
                                        t.start()
                                    """
                            except Exception as e:
                                self.PrintException()
                                #self.logger.warn( 'Bid order failed: %s bid for %s'
                                #                    % ( prc, qty ))

                    # OFFERS

                    if place_asks and i < nasks :

                        if i > 0:
                            prc = self.ticksize_ceil( max( asks[ i ], asks[ i - 1 ] + tsz ), tsz )
                        else:
                            prc = asks[ 0 ]
                            
                        qty = ((self.rest_ws.positions[fut.split('/')[1]]['notional'] )  / float(self.qty_div)) / prc  # / self.qty_div / 6) / prc#round( prc * qtybtc ) / spot
                        #if qty * prc < 6:
                        #    qty = 6 / prc
                        qty = qty * cpercs[fut.split('/')[0]]
                        abc=123#self.pprint('i lbo: ' + str(i) + ' ' + str(len_ask_ords))
                        if i < len_ask_ords:
                            oid = ask_ords[ i ]['id']
                            clientOrderId = ask_ords[ i ]['clientOrderId']
                            oid = float(oid)
                            #abc=123#self.pprint(oid)
                            try:
                                
                                if fut not in self.twosecsblock:
                                    self.twosecsblock[fut] = {}
                                    
                                    self.twosecsblock[fut]['bids'] = {}
                                    self.twosecsblock[fut]['asks'] = {}
                                if i not in self.twosecsblock[fut]['asks']:
                                    self.twosecsblock[fut]['asks'][i] = False
                                if prc not in aprices:
                                    #print('qtye2: ' + str(qty))
                                    self.rest_ws.edits[fut] = True
                                    abc=123#self.pprint('vol edit sell: ' + str(prc))
                                    self.sleep(self.orderRateLimit / 1000)
                                    e = self.rest_ws.edit_order( clientOrderId, oid, fut, "Limit", "sell", qty, prc,"x-" + self.brokerKey + "-" + self.randomword(20) )
                                    abc=123#print(e)
                                    if i > 0:
                                            
                                        self.twosecsblock[fut]['asks'][i] = True
                                    t = self.threading.Thread(target=self.twosecsreseta, args=(fut, i))
                                    t.daemon = True
                                    t.start()
                                elif self.rest_ws.edits[fut] == False and self.slBlock[fut] == False and  self.twosecsblock[fut]['asks'][i] == False :
                                    abc=123#self.pprint('vol edit inbprices ' + str(prc) + ' in bprices!')
                                
                                elif self.rest_ws.edits[fut] == True:
                                    abc=123#self.pprint('vol edit selfedits true ' + fut)
                                elif self.slBlock[fut] == True:
                                    abc=123#self.pprint('vol edit selfslblock true ' + fut)
                                
                            except Exception as e:
                                self.PrintException()

                        else:
                            try: #1000 > -60 
                                if qty * prc > 0.01:
                                    if fut not in self.twosecsblock:
                                        self.twosecsblock[fut] = {}
                                        
                                        self.twosecsblock[fut]['bids'] = {}
                                        self.twosecsblock[fut]['asks'] = {}
                                    if i not in self.twosecsblock[fut]['asks']:
                                        self.twosecsblock[fut]['asks'][i] = False
                                    if self.lao[fut] <= 2:    
                                        #print('qty2: ' + str(qty))
                                        #self.rest_ws.creates[fut] = True
                                        self.sleep(self.orderRateLimit / 1000)
                                        o = self.rest_ws.create_order(  fut, "Limit", 'sell', qty, prc, "GTX", "x-" + self.brokerKey + "-" + self.randomword(20) )
                                        
                                        if 'HOT' in fut:
                                            abc=123#print('vol new buy: ' + str(prc))
                                        #print(o)
                                        if i > 0:
                                            
                                            self.twosecsblock[fut]['asks'][i] = True
                                        t = self.threading.Thread(target=self.twosecsreseta, args=(fut, i))
                                        t.daemon = True
                                        t.start()
                                    elif float(self.rest_ws.positions ) < qty * prc * self.max_skew_mult * -1:
                                        abc=123#self.pprint(fut + ' not selling maxskew, pos: ' + str(float(self.rest_ws.positions[fut]['notional'])) + ' mod: ' + str(qty * prc *  self.max_skew_mult * -1))
                                    """
                                    if self.lao[fut] > self.MAX_LAYERS and i > self.MAX_LAYERS:
                                        t = self.threading.Thread(target=self.rest_ws.cancel_them, args=(self.ask_ords[fut][ i - 1 ]['id'], fut,))
                                        t.daemon = True
                                        t.start()
                                    """
                            
                            except Exception as e:
                                self.PrintException()
                                #self.logger.warn( 'Offer order failed: %s at %s'
                                #                    % ( qty, prc ))

                
            except:
                self.PrintException()
        proc = self.threading.Thread(target=self.place_orders, args=(fut,))
        abc=123#abc=123#self.pprint('5 proc')
        proc.start()
        proc.terminate() 
        self.sleep(5)

    
    def twosecsreseta( self, fut, i ):
        #self.sleep(2)
        self.twosecsblock[fut]['asks'][i] = False
    
    def twosecsresetb( self, fut, i ):
        #self.sleep(2)
        self.twosecsblock[fut]['bids'][i] = False
    