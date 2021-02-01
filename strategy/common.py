//@version=4

strategy(title='Common', overlay=true, initial_capital=1000, default_qty_type=strategy.percent_of_equity, default_qty_value=100, currency='EUR', commission_type=strategy.commission.percent, commission_value=0.26, pyramiding=10)

start = timestamp(2020, 01, 01, 00, 00, 00)
end = timestamp(2022, 01, 01, 00, 00, 00)
period = time >= start and time <= end
openTrades = strategy.opentrades > 0


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
lengthStoch = input(14, "Stoch RSI - Length", minval=1)
src = input(close, title='Stoch RSI - Source')
// MACD
fast_length = input(8, title='MACD - Fast Length', type=input.integer)
slow_length = input(21, title='MACD - Slow Length', type=input.integer)
macd_src = input(title='MACD - Source', type=input.source, defval=close)
signal_length = input(20, title='MACD - Signal Smoothing', type=input.integer, minval = 1, maxval = 50)
sma_source = input(title='MACD - Simple MA(Oscillator)', type=input.bool, defval=false)
sma_signal = input(title='MACD - Simple MA(Signal Line)', type=input.bool, defval=false)
// Williams %R
williams_length = input(title='Williams - Length', type=input.integer, defval=52)
williams_src = input(close, 'Williams - Source', type = input.source)
// OVERSELL - OVERBUY
stoch_k_oversell = input(25, title='Stoch K - Oversell', type=input.integer, minval=1)
stoch_rsi_k_oversell = input(25, title='Stoch RSI K - Oversell', type=input.integer, minval=1)
rsi_oversell = input(38, title='RSI - Oversell', type=input.integer, minval=1)
stoch_k_overbuy = input(75, title='Stoch K - Overbuy', type=input.integer, minval=1)
stoch_rsi_k_overbuy = input(75, title='Stoch RSI K - Overbuy', type=input.integer, minval=1)
rsi_overbuy = input(62, title='RSI - Overbuy', type=input.integer, minval=1)
williams_oversell = input(25, title='Williams - Oversell', type=input.integer, minval=1)
williams_overbuy = input(75, title='Williams - Overbuy', type=input.integer, minval=1)


// -------------- LOGIC -------------- //
// RSI
rsi = rsi(close, rsi_period)
// STOCHASTIC
stoch_k = sma(stoch(close, high, low, periodK), stoch_smoothK)
stoch_d = sma(stoch_k, periodD)
// STOCHASTIC RSI
rsi1 = rsi(src, lengthRSI)
stoch_rsi_k = sma(stoch(rsi1, rsi1, rsi1, lengthStoch), smoothK)
stoch_rsi_d = sma(stoch_rsi_k, smoothD)
// MACD
// fast_ma = sma_source ? sma(macd_src, fast_length) : ema(macd_src, fast_length)
// slow_ma = sma_source ? sma(macd_src, slow_length) : ema(macd_src, slow_length)
// macd = fast_ma - slow_ma
// signal = sma_signal ? sma(macd, signal_length) : ema(macd, signal_length)
// hist = macd - signal
// Williams %R
_pr(williams_length) =>
	max = highest(williams_length)
	min = lowest(williams_length)
	100 * (williams_src - max) / (max - min)
percentR = _pr(williams_length)


// -------------- STRATEGY -------------- //
crossOver = crossover(stoch_rsi_k, stoch_rsi_d)
crossUnder = crossunder(stoch_rsi_k, stoch_rsi_d)

buyCounter = 0
if period and not openTrades
    if stoch_k < stoch_k_oversell and stoch_rsi_k < stoch_rsi_k_oversell
        buyCounter := buyCounter + 2
    if rsi < rsi_oversell
        buyCounter := buyCounter + 1
    if crossOver
        buyCounter := buyCounter + 1
    if percentR < williams_overbuy
        buyCounter := buyCounter + 1
buySignal = buyCounter > 3

sellCounter = 0
if period and openTrades
    if stoch_k > stoch_k_overbuy and stoch_rsi_k > stoch_rsi_k_overbuy
        sellCounter := sellCounter + 2
    if rsi > rsi_overbuy
        sellCounter := sellCounter + 1
    if crossUnder
        sellCounter := sellCounter + 1
    if percentR > williams_oversell
        sellCounter := sellCounter + 1
sellSignal = sellCounter > 3

strategy.order('buy', true, 1, when = buySignal, comment='buy coef: ' + tostring(buyCounter))
strategy.order('sell', false, 1, when = sellSignal, comment='sell coef: ' + tostring(sellCounter))
