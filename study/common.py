// @version=4

study(title='Common', precision=2, overlay=true)


// -------------- INPUTS -------------- //
// RSI
rsi_period = input(14, title='RSI - Periods', minval=1)
// STOCHASTIC
periodK = input(20, title='Stoch K', minval=1)
periodD = input(3, title='Stoch D', minval=1)
stoch_smoothK = input(3, title='Stoch Smooth', minval=1)
// STOCHASTIC RSI
smoothK = input(3, 'Stoch RSI - Smooth K', minval=1)
smoothD = input(3, 'Stoch RSI - Smooth D', minval=1)
lengthRSI = input(14, 'Stoch RSI - Length', minval=1)
lengthStoch = input(14, "Stoch - Length", minval=1)
src = input(close, title='Stoch RSI - Source')
// MACD
fast_length = input(title='MACD - Fast Length', type=input.integer, defval=12)
slow_length = input(title='MACD - Slow Length', type=input.integer, defval=26)
macd_src = input(title='MACD - Source', type=input.source, defval=close)
signal_length = input(title='MACD - Signal Smoothing', type=input.integer, minval = 1, maxval = 50, defval = 9)
sma_source = input(title='MACD - Simple MA(Oscillator)', type=input.bool, defval=false)
sma_signal = input(title='MACD - Simple MA(Signal Line)', type=input.bool, defval=false)


// -------------- LOGIC -------------- //
// RSI
rsi = rsi(close, rsi_period)
// STOCHASTIC
stoch_k = sma(stoch(close, high, low, periodK), stoch_smoothK)
stoch_d = sma(stoch_k, periodD)
// STOCHASTIC RSI
rsi1 = rsi(src, lengthRSI)
k = sma(stoch(rsi1, rsi1, rsi1, lengthStoch), smoothK)
d = sma(k, smoothD)
// MACD
fast_ma = sma_source ? sma(macd_src, fast_length) : ema(macd_src, fast_length)
slow_ma = sma_source ? sma(macd_src, slow_length) : ema(macd_src, slow_length)
macd = fast_ma - slow_ma
signal = sma_signal ? sma(macd, signal_length) : ema(macd, signal_length)
hist = macd - signal


// -------------- RENDERING -------------- //
// RSI
plot(rsi, 'RSI')
// STOCHASTIC
plot(stoch_k, 'STOCH K', color=color.green)
plot(stoch_d, 'STOCH D', color=color.red)
// STOCHASTIC RSI
plot(k, 'STOCH RSI K', color=color.orange)
plot(d, 'STOCH RSI D', color=color.purple)

// fill(b1, b2, title = 'Background Bollinger', color=#198787, transp=95)
// plotshape(overbuy, 'Overbuy', style=shape.triangleup, location=location.abovebar, color=color.green, size=size.tiny)
// plotshape(oversell, 'Oversell', style=shape.triangledown, location=location.belowbar, color=color.red, size=size.tiny)
