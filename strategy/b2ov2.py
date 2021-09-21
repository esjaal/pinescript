// @version=4

// Timeframe: 30m (48 bars)
// Crypto: Multi-pair
// Pairs: AAVE, ADA, AVAX, BNB, BTC, DOT, EGLD, EOS, 
//   ETH, FIL, FTM, FTT, GRT, LINK, LTC, LUNA, MATIC, MOVR
//   RAY, RSR, SAND, SDN, SOL, UOS, XLM, XRP, XTZ, ZEC
// Average benefits: 518.93%
// Back testing period: 2021-2022
// Usage: 3commas Bot

strategy(title='b2ov2', overlay=true, 
     initial_capital=100, default_qty_type=strategy.percent_of_equity,
     default_qty_value=100, currency='USD', commission_value=0,
     commission_type=strategy.commission.percent)

start = timestamp(2021, 01, 01, 00, 00, 00)
end = timestamp(2022, 01, 01, 00, 00, 00)
period = time >= start and time <= end
openTrades = strategy.opentrades > 0

// Trigger alert for 20% decrease on 24h
decrease = input(20, title='Moving down %', minval=5)
bars = input(48, title='Bars number', minval=2)
benefits = input(5, title='Take Profit (%)', minval=1)
formattedDecrease = - (decrease/100)
formattedBenefits = (benefits/100) + 1

highest = highest(close, bars)
lowest = lowest(close, bars)
percChange = ((lowest - highest) / highest) <= formattedDecrease

buySignal = percChange and not openTrades
sellSignal = close > close[1] * formattedBenefits and openTrades

if period
    strategy.entry('buy', strategy.long, when=buySignal)
    strategy.close('buy', when=sellSignal)
