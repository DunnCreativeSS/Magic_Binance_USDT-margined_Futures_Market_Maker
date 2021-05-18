
var btc = 0;
api_key = 'xxx'
api_secret = 'xxx'

const ccxt = require('ccxt')
          
         ////console.log(ftx)

        client     = new ccxt.binance({
    'apiKey': api_key,
    'secret': api_secret,
    'timeout': 30000,
    'enableRateLimit': true,
            "options":{"defaultMarket":"margin"},
 })

        client1999     = new ccxt.binance({
    'apiKey': api_key,
    'secret': api_secret,
    'timeout': 30000,
    'enableRateLimit': true,
            "options":{"defaultMarket":"margin"},
 })

var client2 = new ccxt.deribit(

            {"apiKey": "",
            "secret": ""
 })
//client.urls['api'] = client.urls['test']
var usd2 = 0
var IM = 0
var orders = []
var LEV = 0
var olength = 0
var LEV_LIM = parseFloat(process.env.limit)
var startTime = new Date().getTime()
var oldstartTime = new Date().getTime() - 1000 * 60 * 60 * 24 / 3
var btcstart
var usdstart
var aprs = []
var yields = []
var btc4start
var usd4start
var usds = []
var thedone = true

var levs = []
var usd4s = []
var prices = []
var btc4s = []
var btcs = []
var btc2 = 0
var apr;
var usdcad = 1.32790;
var request = require("request")
async function getusdcad(){

	request.get('https://free.currconv.com/api/v7/convert?q=USD_CAD&compact=ultra&apiKey=56f9c260d80c736e4fc8', function(e, r, d){
		try{
			usdcad = JSON.parse(d)['USD_CAD']
		}
		catch(err){
			//console.log(err)
		}
	})
	
}
var takents = []
var r = 0
var markets = []
var usd4 = 0
var btc4 = 0
var ids = []
var vol = 0
var line
var tradesArr = []
var first = true;
var m;
var lines = []
var fee = 0
var btcusd;
var btcusdstart;
var positions = []
async function recursiveIncomes(thetime, thetime2, usdtold){
				//console.log(aprs.length)
					//console.log(usds.length)
console.log(thetime2)
	if (thetime == 9999999999999999999999){
	incomes = await client.fapiPrivateGetIncome({'limit': 1000, 'startTime': oldstartTime})
	
	incomes2 = await client1999.fapiPrivateGetIncome({'limit': 1000, 'startTime': oldstartTime})
	}
	else{
		incomes = await client.fapiPrivateGetIncome({'limit': 1000, 'endTime': thetime, 'startTime': 1597664686000})
	incomes2 = await client1999.fapiPrivateGetIncome({'limit': 1000, 'endTime': thetime, 'startTime': 1597664686000})
	
	}
	console.log(incomes.length)
	////////console.log(incomes)
	startbal = 0
	var newaprs = []
	var newusds = []

	var oldthetime2 = thetime2
	for(var inc in incomes2){
		if (incomes2[inc].asset == 'USDT'){
			if (incomes2[inc].time < thetime){
				thetime = incomes2[inc].time

			}
			if (incomes2[inc].time > thetime2){
				oldthetime2 = thetime2
				thetime2 = incomes2[inc].time
			}
			if (incomes2[inc].incomeType != 'TRANSFER' && incomes[inc].incomeType !='CROSS_COLLATERAL_TRANSFER'){
usdtold += parseFloat(incomes2[inc].income) * 1
}
else {
	console.log(incomes2[inc].incomeType)
}
		}
	}
	for(var inc in incomes){
		if (incomes[inc].asset == 'USDT'){
			if (incomes[inc].time < thetime){
				thetime = incomes[inc].time

			}
			if (incomes[inc].time > thetime2){
				oldthetime2 = thetime2
				thetime2 = incomes[inc].time
			}
			if (incomes[inc].incomeType != 'TRANSFER' && incomes[inc].incomeType !='CROSS_COLLATERAL_TRANSFER'){
usdtold += parseFloat(incomes[inc].income) * 1
}
else {
	console.log(incomes[inc].incomeType)
}
		}
	}
if (incomes.length == 1000){
	return(recursiveIncomes(thetime, thetime2, usdtold))
}
else{
	return([thetime, usdtold, thetime2])
}
}
async function testing123(){
	
}
testing123()
setInterval(function(){
	testing123()
}, 5 * 60 * 1000)
setInterval(async function(){
	try{
	if (thedone == true){
thedone = false
	ethusd = await client.fetchTicker('ETH/USDT')
	ethusd = ethusd['last']
	btcusd = await client.fetchTicker('BTC/USDT')
	////////console.log(btcusd)
btcusd = btcusd['last']

	////////console.log(btcusd)
ethbtc = btcusd/ethusd

	
console.log(markets.length)
	              for (var market in markets) {
        if (markets[market].type == 'spot') {
            var trades = await client.fetchMyTrades(markets[market].market, undefined, 10)

            
            for (var t in trades) {
                if (!takents.includes(trades[t].timestamp)){
                	takents.push(trades[t].timestamp)
                
                if(trades[t].side == 'sell'){
                lines.push({'color':
                        '#FF0000', // Red
                        'width':1,
                        'value': parseFloat(trades[t].timestamp) // Position, you'll have to translate this to the values on your x axis
                                    })
                }
                else {
                lines.push({'color':
                        '#00FF00', // Red
                        'width':1,
                        'value': parseFloat(trades[t].timestamp) // Position, you'll have to translate this to the values on your x axis
})
                }
}
}
}
}
console.log(lines)
	//////////////console.log(trades.length)

//////////////console.log(account)
//account         = await client.fetchBalance()
//////////////console.log(account)
//////////console.log(account)
////////console.log(btc)
 
btc = 0
////////console.log(btc)
 
while (thedone == false){
var bal = await client.fetchBalance({'type': 'margin'})
 //bal3 = await client1999.fetchBalance()
 LEV = 0

// //console.log(bal2)
 btc3 = 0
 	//btc3 += parseFloat(bal2.info.totalMarginBalance)


 	balances = {}
                //bal = exchange.fetchBalance()
                        var net_worth = 0
                        try{  
                for (var b in bal){
                    if (b == 'total'){
                        for (var coin in bal[b]){
                         balances[coin] = bal[b][coin]
                                    if (balances[coin] > 0 && coin != 'USDT'){
                                    	 price = await client.fetchTicker(coin + "/USDT")
                                    	 price = price['info']['askPrice']
                                    	 price = parseFloat(price)
                                    	 var gogogo = true
                                    	 for (market in markets){
                                    	 	if (markets[market].market == coin + '/USDT'){
	gogogo = false
}

                                    	 }
                                    	 if (gogogo){
                                    	 markets.push({'type': 'spot', 'market': coin + '/USDT'})
                                    	 }
                                    	 balances[coin] = parseFloat(balances[coin])
                                    net_worth += balances[coin] *price
                        }
                    } 
                    }
                }
                thedone = true
            }
        catch(err){
                    	if ('TypeError' in err.toString()){
                    	}
                    	else{
console.log(err)
}
        }
    }
        console.log(parseFloat(balances['USDT']))
                        net_worth += parseFloat(balances['USDT'])
btc3 = net_worth
 	////console.log(bal2.info.result[c].usdValue / btcusd)
  
  
   //btc3=     parseFloat(bal = bal2.info.result[ 'USDT' ] ['total'])

//////////////console.log(account)

//btc3 = parseFloat(account2 [ 'info' ] ['totalMarginBalance'])
////////////console.log(btc)

btc2 = btc  /  btcusd + btc3  /  btcusd

usd2 = parseFloat(net_worth)
//console.log(btc2)

btc4 = btc /  btcusd
usd4 = btc4

////console.log(bal2)
////console.log(bal2['info'])
IM = LEV / 2 
       ////console.log('lev')
       ////console.log(LEV)	
//////////console.log(btc2)

bal = await client.fetchBalance({'type': 'margin'})
//console.log(bal)
b1 = parseFloat(bal['info']['totalNetAssetOfBtc'])
b2 = parseFloat(bal['info']['totalAssetOfBtc'])
usd = b1
if (b2 > b1){
	usd =  b2
}
btcusdt = await client.fetchTicker('BTC/USDT')
mid = (btcusdt['bid'] + btcusdt['ask'] ) / 2
usd2 = usd * mid
console.log('usd2 ' + usd2)
if (btc2 != 0){
	if (first)
{
	btc4start = btc2
	usd4start = usd2
btcstart = btc2
first = false;
usdstart = usd2
btcusdstart = btcusd
////////console.log(btcstart)
}

prices.push([new Date().getTime(), -1 * (1-(btcusd / btcusdstart)) * 100])
	levs.push( [new Date().getTime(), LEV / LEV_LIM * 100])

//console.log(usd2)
//console.log(usdcad)
//console.log(usd2 * 1)

var d = new Date().getTime()
	usds.push( [new Date().getTime(), usd2 * 1])
				var d2 = usds[0][0]
				//console.log(d2)
				var diff = d - d2;

				var s = diff / 1000
				var m = s / 60
				var h = m / 60
				var d = h / 24
				//console.log(d)
				var y = d / 365


				apr = (usds[usds.length-1][1] -usds[0][1]) / y // (usds[usds.length-1][1] - 0.01348379) / y
				//console.log('')
				
				//console.log(apr)

if ((apr > 0 || apr <= 0)){
				
				aprs.push( [new Date().getTime(), apr / 365])
				yields.push( [new Date().getTime(), (apr / 365) / (usd2 * 1)])
}
r++
					//if ( r > 2){
						r = 0

			/*
		} else{
			usds[usds.length-1][1] = usd2
aprs[aprs.length-1][1] = apr / 365
yields[yields.length-1][1] = (apr / 365) / (usd2 * 1)

		}
*/

				//aprs.push([new Date().getTime(), apr])
					//aprs.push( [new Date().getTime(), apr / 365])
btcs.push( [new Date().getTime(), -1 * (1-(btc2 / btcstart)) * 100])
	usd4s.push( [new Date().getTime(), -1 * (1-(usd4 / usd4start)) * 100])

btc4s.push( [new Date().getTime(), -1 * (1-(btc4 / btc4start)) * 100])

topost = {'theurl': theurl, 'amounts': 0, 'fees': 0, 'startTime': startTime, 'apikey': process.env.binancekey, 'usd': usd2, 'btc': btc2, 'btcstart': btc4start, 'usdstart': usd4start, 'funding': true}
                if (!first){
             //  request.post("http://jare.cloud:8080/subscribers", {json:topost}, function(e,r,d){
               
               	////console.log(d)
               //+})
               	} 
               }
           }
} catch(err){}
//////////////console.log(btc)
}, 5000)
var theurl = process.env.theurl


const express = require('express');
var cors = require('cors');
var app = express();
app.use(cors());
var bodyParser = require('body-parser')
app.use(bodyParser.json()); // to support JSON-encoded bodies
app.use(bodyParser.urlencoded({ // to support URL-encoded bodies
    extended: true
}));
app.set('view engine', 'ejs');
app.listen(process.env.PORT || 8080, function() {});
subscribers = {}
setInterval(async function(){
subscribers = {}

}, 10 * 60 * 1000)
app.post('/subscribers', cors(), (req, res) => {
let apikey = req.body.apikey
let apikey2 = req.body.apikey2
let usdstrat = false
if (apikey2 != undefined){
if (apikey2.length < 2){
usdstrat = false
}
else {
usdstrat = true

}
}

let btcsub = req.body.btc
let btcstartsub = req.body.btcstart
let fees = parseFloat(req.body.fees) * btcusd
let amounts = parseFloat(req.body.amounts)
let usdsub = req.body.usd
let usdstartsub = req.body.usdstart
let startTime = req.body.startTime
if (subscribers[apikey] == undefined && parseFloat(btcstartsub) != 0 && parseFloat(usdstartsub) != 0){
subscribers[apikey] = {'usdstrat': usdstrat, 'amounts': amounts, 'fees': fees, 'btc': btcsub, 'btcstart': btcstartsub, 'usd': usdsub, 'usdstart': usdstartsub, 'pnlbtc': [startTime, 0], 'pnlusd': [startTime,0]}
////console.log(apikey)
}
else{
	if (parseFloat(btcstartsub) != 0 && parseFloat(usdstartsub) != 0){
	subscribers[apikey].amounts = amounts
	subscribers[apikey].usdstrat = usdstrat
	subscribers[apikey].fees = fees
	subscribers[apikey].btc = btcsub
	subscribers[apikey].btcstart = btcstartsub
	subscribers[apikey].usd = usdsub
	subscribers[apikey].usdstart = usdstartsub

subscribers[apikey].pnlbtc.push({'pnl': [startTime, -1 * (1-(btcsub / btcstartsub)) * 100], 'usdstrat': usdstrat})
subscribers[apikey].pnlusd.push({'pnl': [ startTime,-1 * (1-(usdsub / usdstartsub)) * 100], 'usdstrat': usdstrat})
}
	}
	//////console.log(subscribers)
	//////console.log(apikey + ' recent pnl btc: ' + subscribers[apikey].pnlbtc[subscribers[apikey].pnlbtc.length-1])

	//////console.log(apikey + ' recent pnl usd: ' + subscribers[apikey].pnlusd[subscribers[apikey].pnlusd.length-1])
	res.send('ok')

	})


app.get('/update', cors(), (req, res) => {

    res.json({
usds:usds,
    	aprs:aprs,
    	yields:yields,
    	lines:lines
    })
    	console.log(usd2)

})

app.get('/', (req, res) => {
        res.render('indexFunding.ejs', {
    	usds: usds,
    	aprs: aprs,
    	lines:lines,
    	yields: yields,
        theurl: theurl
        })

});
