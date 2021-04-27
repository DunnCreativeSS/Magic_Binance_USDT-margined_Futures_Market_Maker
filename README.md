# Magic_Binance_USDT-margined_Futures_Market_Maker by Jarett Dunn


# Chat


https://discord.gg/YtstUhA6PF


# Important Note


This software makes no assurances or implication of profit. Past transaction history is no assurance or implication of future returns. This product is in a very active alpha stage, and may not run as expected. You may lose all of your funds, as this algo trades at leverage (that you can increase or decrease) - risk only what you can afford to lose, and always do your own research & due diligence.


# Secondly Important Note


Please do create a brand-new Binance account without using any referral codes, so that my Binance Broker API key can generate me some revenues (only when you exit at TP/SL, which you can set).


# Thirdly Important Note


To enter the Binance Futures Market Making Program, kindly send an email to their team after reviewing the documentation (and you may achieve a few week's trial of usdt-m and coin-m market making rebates if you're lucky...):  https://www.binance.com/en/support/faq/b65fefd0fee84893ad946dc6f707dedc


# Changelog

 
## Publicity v1.0


I won the recent BNB giveaway for spot + futures using this market maker. I traded more than 2 BTC in <2 hours with a balance of about $40. I even turned a 1.5% returns on equity trading BTCUSD futures.


https://medium.com/@jarettdunn/binance-hacked-two-trading-competitions-my-share-of-40k-and-10k-bnb-prize-in-jare-cloud-c9dca20f0ac6

Binance WAS running a competition as we speak for 50k BNB — 40k for spot/margin, 10k for futures — if you trade more than 1 BTC in notional value in either bucket! Be prepared for the next competition with my private market making repository for Binance futures and margin! IOTX Binance trading competition just concluded with another $90 000 to be won!


https://imgur.com/b97oLP9


https://drive.google.com/file/d/198dAxfEfmPxxe696t7wnsN3ijBLods4h/view?usp=sharing


Lucky for me I already have a Binance futures market maker — and with a wee bit of edits to the code, it ran fine on margin 5x, too! I ran the futures on 100x and orders of 0.002 BTC and it won the futures contest in ~1hr.


Check g543 for the total. Woo!


I was +0.5% for most of my bot run on futures, ended at -1% on equity.


I was down about 21% — of my whopping $46 — on margin.


Win Binance trading competitions! I won my share of 10k BNB for futures trading and 40k BNB for spot/margin trading 1+ BTC in <3 hours in this recent Binance giveaway: https://www.binance.com/en/support/articles/360040070651


## Enter 2.0


I've been hired to build an algo that achieves and maintains Futures Market Making Program requirements, while also earning some $ from the fee rebate along with the realized PnL (from the spread). I retain the IP for this algo as part of the agreement.


It's been nearly fully built and tested on USDT-m, here are the 10k recent trades over the last 0.44 days: https://drive.google.com/file/d/12l9thx8Bvbbek8X4vPEoQqXcvGxPEX2B/view?usp=sharing


The last 24hr's worth of iterations were specific to hitting cumulative min. order sizes on the books, while optimizing the list of instruments to trade vs the weight of the instrument and 24hr liquidity. According to the above sheet, we're doing about 21 000 times our $566 equity in volume projected / month - while sustaining growth of equity in uPnL and rPnL.


The algo has been built with a configurable Take Profit and Stop Loss, expressed in % such as the ROI on the futures interface. The algo only ever enters a market making order as post-only, and therein would drive me no revenues - but the TP/SL orders execute at market.


# Setup


1. Clone or download repo
2. cd into dir
3. pip3 install ccxt
4. cp conf.json.ex conf.json
5. Edit conf.json! (TP and SL are multipled by lev, so 3x lev and 5% TP would exit positions when they achieve an ROI of 15%)
6. python3 market_maker.py
7. fun and profit!


https://hackernoon.com/porting-a-bot-to-binance-futures-market-making-competition-6v6a31qh


# Further Dev


Next up is this same approach to coin-margined futures - with more than 10x the fee rebate / maker trade!

