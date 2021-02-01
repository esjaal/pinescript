//@version=4

strategy(title='Initial', overlay=true, initial_capital=1000, default_qty_type=strategy.percent_of_equity, default_qty_value=100, currency='EUR', commission_type=strategy.commission.percent, commission_value=0.26, pyramiding=10)

start = timestamp(2020, 01, 01, 00, 00, 00)
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
    strategy.order('buy', true, 1, when = buySignal)
    strategy.order('sell', false, 1, when = sellSignal)
