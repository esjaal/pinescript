// @version=4

study(title='RSI/Bollinger/DEMA500', precision=2, overlay=true)


// ----------- Inputs
rsiOversell = input(30, minval=0, maxval=100, title='RSI oversell')
rsiOverbuy = input(70, minval=0, maxval=100, title='RSI overbuy')

priceDemaGapTolerance = input(60, minval=0, maxval=100, title='Price & DEMA gap tolerance')

emaSrc = input(close, title='EMA Source')
demaPeriod = input(500, minval=1, maxval=500, title='DEMA period')

bollLength = input(20, minval=1, title='Bollinger Length')
bollSrc = input(close, title='Bollinger Source')


// ----------- Bollinger
basis = sma(bollSrc, bollLength)
dev = 2.0 * stdev(bollSrc, bollLength)
upper = basis + dev // lower point of bollinger
lower = basis - dev // higher point of bollinger


// ----------- RSI
rsi = rsi(close, 9)


// ----------- DEMA
e1 = ema(emaSrc, demaPeriod)
e2 = ema(e1, demaPeriod)
dema = 2 * e1 - e2


// ----------- Logic
priceDemaGap = close - dema // units
gap = (priceDemaGap / 100) * priceDemaGapTolerance
authorized = dema + gap

overbuy = rsi > rsiOverbuy and high > upper and low > authorized
oversell = rsi < rsiOversell and low < lower and high < authorized


// ----------- Rendering
plot(dema, 'ema')

b1 = plot(upper, 'Upper Bollinger', color=color.teal, offset=0)
b2 = plot(lower, 'Lower Bollinger', color=color.teal, offset=0)
fill(b1, b2, title = 'Background Bollinger', color=#198787, transp=95)

plotshape(overbuy, 'Overbuy', style=shape.triangleup, location=location.abovebar, color=color.green, size=size.tiny)
plotshape(oversell, 'Oversell', style=shape.triangledown, location=location.belowbar, color=color.red, size=size.tiny)
