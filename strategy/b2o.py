//@version=4

// Timeframe: 1h
// Pair: BTC/BUSD
// Fees: Binance Exchange

strategy(title='b2o', overlay=true, initial_capital=1000, default_qty_type=strategy.percent_of_equity, default_qty_value=100, currency='EUR', commission_type=strategy.commission.percent, commission_value=0)

start = timestamp(2021, 01, 01, 00, 00, 00)
end = timestamp(2022, 01, 01, 00, 00, 00)
period = time >= start and time <= end
openTrades = strategy.opentrades > 0

lostPercentage = input(92, title='Buy Signal', minval=1)
gainPercentage = input(1.05, title='Sell Signal', minval=1)

diff = (close * 100) / close[1]
// plot(diff, title = 'diff', color=color.red, linewidth = 2)

buySignal = diff < lostPercentage and not openTrades
sellSignal = close > close[1] * gainPercentage and openTrades

if period
    strategy.entry('buy', strategy.long, when=buySignal)
    strategy.close('buy', when=sellSignal)
