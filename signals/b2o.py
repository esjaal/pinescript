//@version=4

// Timeframe: 30m
// Pair: BTC/BUSD
// Fees: Binance Exchange

strategy(title='b2o - 3commas', overlay=true, initial_capital=100, default_qty_type=strategy.percent_of_equity, default_qty_value=100, currency='EUR', commission_type=strategy.commission.percent, commission_value=0, pyramiding=9999)

start = timestamp(2021, 01, 01, 00, 00, 00)
lostPercentage = input(98, title='Buy Signal', minval=1)

diff = (close * 100) / close[1]

buySignal = diff < lostPercentage and time >= start
strategy.entry('buy', strategy.long, when=buySignal)
