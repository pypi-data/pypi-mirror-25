import numpy as np

_open = None
_close = None
_high = None
_low = None
_volumes = None

def assignRates( open, high, low, close, volumes ):
	_open = None
	_close = None
	_high = None
	_low = None
	_volumes = None

def assignFinamRates( finamRates, flip = False ):
	_open = np.array( finamRates.loc[:,'<OPEN>'] )
	_close = np.array( finamRates.loc[:,'<CLOSE>'] )
	_high = np.array( finamRates.loc[:,'<HIGH>'] )
	_low = np.array( finamRates.loc[:,'<LOW>'] )
	_volumes = np.array( finamRates.loc[:,'<VOL>'] )
	if flip:
		np.flip( _open )
		np.flip( _high )
		np.flip( _low )
		np.flip( close )
		np.flip( _volumes )

# 
def _defineRates( op=[], hi=[], lo=[], cl=[], vo=[] ):
	global _open
	global _high
	global _low
	global _close
	global _volumes

	ret = ()
	if op is None:
		op = _open
		ret = ret + (op,)
	elif len(op) > 0:
		ret = ret + (op,)
	if hi is None:
		hi = _high
		ret = ret + (hi,)
	elif len(hi):
		ret = ret + (hi,)
	if lo is None:
		lo = _low
		ret = ret + (lo,)
	elif len(lo) > 0:
		ret = ret + (lo,)
	if cl is None:
		cl = _close
		ret = ret + (cl,)
	elif len(cl) > 0:
		ret = ret + (cl,)
	if vo is None:
		vo = _volumes
		ret = ret + (vo,)
	elif len(vo) > 0:
		ret = ret + (vo,)
	return ret
# end of _defineRates


# AD-indicator
def ad( period=1, shift=0, hi=None, lo=None, cl=None, vo=None, prev=None ):
	(hi, lo, cl, vo) = _defineRates( hi=hi, lo=lo, cl=cl, vo=vo )
	if hi is None or lo is None or cl is None or vo is None:
		return None

	adValue = None
	if prev is not None:
		if shift < len(cl):
			adValue = prev + ad1( hi[shift], lo[shift], cl[shift], vo[shift] ) 
	else:
		startIndex = shift + period - 1
		if startIndex < len(cl):
			prevAdValue = 0.0
			for i in range( startIndex, shift-1, -1 ):
				adValue = prevAdValue + ad1( hi[i], lo[i], cl[i], vo[i] ) 
				prevAdValue = adValue
	
	return adValue
# end of AD

def ad1( hi,lo,cl,vo ):
	highLessLow = hi - lo
	if highLessLow > 0.0:
		closeLessLow = cl - lo
		highLessClose = hi - cl
		return ( ( vo * ( closeLessLow - highLessClose ) ) / highLessLow )
	return 0
# end of ad1

# ADX-indicator
def adx( period=14, shift=0, hi=None, lo=None, cl=None, prev=None ):
	(hi, lo, cl) = _defineRates( hi=hi, lo=lo, cl=cl )
	if hi is None or lo is None or cl is None:
		return None

	if prev is not None:
		if shift+1 >= len(cl):
			return None

		smoothedTr = prev['TRsm']
		smoothedPlusDM = prev['+DMsm']
		smoothedMinusDM = prev['-DMsm']	
		tr = max( hi[shift] - lo[shift], abs( hi[shift] - cl[shift+1]), abs(lo[shift]-cl[shift+1]) )
		plusDM = 0.0
		minusDM = 0.0
		upMove = hi[shift] - hi[shift+1]
		downMove = lo[shift+1] - lo[shift]
		if upMove > downMove and upMove > 0.0:
			plusDM = upMove
		if downMove > upMove and downMove > 0.0:
			minusDM = downMove
		
		smoothedTr = smoothedTr - smoothedTr / period + tr
		if not( smoothedTr > 0.0 ):
			return None 
		smoothedPlusDM = smoothedPlusDM - smoothedPlusDM / period + plusDM
		smoothedMinusDM = smoothedMinusDM - smoothedMinusDM / period + minusDM

		plusDI = 100.0 * (smoothedPlusDM / smoothedTr)
		minusDI = 100.0 * (smoothedMinusDM / smoothedTr)
		sumDI = plusDI + minusDI
		if not( sumDI > 0.0 ):
			return None
		dx0 = 100.0 * ( abs( plusDI - minusDI ) / sumDI )
		adx = ( prev['adx'] * (period-1.0) + dx0 ) / period

	else:
		st = shift + period * 2 - 2
		if st+1 >= len(cl):
			return None

		plusDM = np.zeros( shape=period*2, dtype="float" )
		minusDM = np.zeros( shape=period*2, dtype="float" )
		tr = np.empty( shape=period*2, dtype='float')

		for i in range( st, shift-1, -1 ):
			upMove = hi[i] - hi[i+1]
			downMove = lo[i+1] - lo[i]

			index = i-shift
			if upMove > downMove and upMove > 0.0:
				plusDM[index] = upMove

			if downMove > upMove and downMove > 0.0:
				minusDM[index] = downMove
		
			tr[index] = max( hi[i] - lo[i], abs( hi[i] - cl[i+1]), abs(lo[i]-cl[i+1]) )

		# for i in range(st, shift-1,-1):
		# 	print str(i) + ": tr =" + str( tr[i-shift] ) + ", plusDM=" + str( plusDM[i-shift] ) + ", minusDM=" + str( minusDM[i-shift] )
		
		dx = np.empty( shape = period, dtype='float' )
		smoothedTr = None
		smoothedPlusDM = None
		smoothedMinusDM = None	
		for i in range( shift + period-1, shift-1, -1 ):
			index = i - shift
			if smoothedTr is None:
				smoothedTr = np.sum( tr[index:index+period] )
			else:
				smoothedTr = smoothedTr - smoothedTr / period + tr[index]
			if smoothedPlusDM is None:
				smoothedPlusDM = np.sum( plusDM[index:index+period] )
			else:
				smoothedPlusDM = smoothedPlusDM - smoothedPlusDM / period + plusDM[index]
			if smoothedMinusDM is None:
				smoothedMinusDM = np.sum( minusDM[index:index+period] )
			else:
				smoothedMinusDM = smoothedMinusDM - smoothedMinusDM / period + minusDM[index]

			if not( smoothedTr > 0.0 ):
				return None 
			plusDI = 100.0 * (smoothedPlusDM / smoothedTr)
			minusDI = 100.0 * (smoothedMinusDM / smoothedTr)
			sumDI = plusDI + minusDI
			if not( sumDI > 0.0 ):
				return None
			dx[index] = 100.0 * ( abs( plusDI - minusDI ) / ( plusDI + minusDI ) )

		adx = np.mean( dx )
		dx0 = dx[0]

	return( { 'adx': adx, 'dx': dx0, "+DI": plusDI, "-DI": minusDI, "+DMsm": smoothedPlusDM, "-DMsm": smoothedMinusDM, "TRsm": smoothedTr } )
# end of ADX	


# ATR - Average True Range
def atr( period=14, shift=0, hi=None, lo=None, cl=None, prev=None ):
	(hi, lo, cl) = _defineRates( hi=hi, lo=lo, cl=cl )
	if hi is None or lo is None or cl is None:
		return None

	trValue = None
	atrValue = None
	if prev is not None:
		if prev['atr'] is not None:
			if shift < len(cl):
				trValue = tr( hi, lo, cl, shift )
				atrValue = (prev['atr'] * (period-1) + trValue) / period	
	if atrValue is None:
		if shift + period - 1 < len(cl):
			trValues = np.empty( shape=period, dtype='float' )
			for i in range( shift+period-1, shift-1, -1 ):
				trValues[i-shift] = tr( hi, lo, cl, i )
			trValue = trValues[0]
			atrValue = np.mean( trValues )

	return { 'atr':atrValue, 'tr':trValue }
# end of atr


def tr( hi, lo, cl, shift ):
	trValue = None
	lenCl = len(cl)
	if shift + 1 < lenCl:
		trValue = max( hi[shift] - lo[shift], abs(hi[shift] - cl[shift+1]), abs(lo[shift] - cl[shift+1]) )
	elif shift < lenCl:
		trValue = hi[shift] - lo[shift]
	return trValue
#end of tr


# Bollinger Bands
def bollinger( period=20, shift=0, nStds = 2.0, rates=None ):
	(rates,) = _defineRates( cl=rates )
	if rates is None:
		return None

	en = shift + period
	if en > len(rates):
		return None

	bandMiddle = np.mean( rates[shift:en] )
	bandStd = np.std( rates[shift:en] )

	return( { 'middle':bandMiddle, 'std': bandStd, 'upper': bandMiddle + nStds * bandStd, 'lower': bandMiddle - nStds * bandStd } )
# end of bollinger


# CCI indicator
def cci( period=20, shift=0, hi=None, lo=None, cl=None, cciConst=0.015 ):
	(hi, lo, cl) = _defineRates( hi=hi, lo=lo, cl=cl )
	if hi is None or lo is None or cl is None:
		return None

	if shift + period - 1 >= len(cl):
		return None
		
	typicalPrices = np.empty( shape = period, dtype='float')
	for i in range( shift+period-1, shift-1, -1 ):
		typicalPrices[shift-i] = (hi[i] + lo[i] + cl[i]) / 3.0
	
	meanTypicalPrice = np.mean( typicalPrices )	

	sumDeviation = 0.0
	for i in range( shift+period-1, shift-1, -1 ):
		sumDeviation = sumDeviation + abs( meanTypicalPrice - typicalPrices[shift-i] )
	if not( sumDeviation > 0.0 ):
		return None
	meanDeviation = sumDeviation / period

	cciValue = (typicalPrices[0] - meanTypicalPrice) / (cciConst * meanDeviation)

	return { 'cci': cciValue, 'meanTypicalPrice': meanTypicalPrice, 'meanDeviation': meanDeviation }
# end of CCI


# EMA - Exponential Moving Average
def ema( period=10, shift=0, alpha=None, rates=None, prev=None, history=0 ):			
	global _close
	if rates is None:
		rates = _close
	if rates is None:
		return None

	if alpha is None:
		alpha = 2.0 / (period + 1.0)

	emaValue = None

	# Previously calculated ema is given 
	if prev is not None:
		if shift < len(rates):
			emaValue = (rates[shift] - prev) * alpha + prev
	else:
		if history == 0:
			end = shift + period - 1
			if end < len(rates):
				emaValue = np.mean( rates[shift:end+1] )
		else:
			end = shift + period + history - 1
			if end < len(rates):
				emaValue = np.mean( rates[ shift+history: end+1 ] )
				for i in range( shift+history-1, shift-1,-1 ):
					emaValue = (rates[i] - emaValue) * alpha + emaValue
	return emaValue
# end of ema


# MACD - Moving Average Convergence/Divergence Oscillator
def macd( periodFast=12, periodSlow=26, periodSignal=9, shift=0, rates=None ):
	global _close
	if rates is None:
		rates = _close
	if rates is None:
		return None

	st = shift + periodSlow + periodSignal - 1
	if st >= len(rates):
		return None
	
	fastLessSlow = np.empty( shape=periodSignal, dtype='float' )
	emaSlow = ema( period=periodSlow, shift=shift+periodSignal-1, rates=rates )
	emaFast = ema( period=periodFast, shift=shift+periodSignal-1, rates=rates )
	fastLessSlow[periodSignal-1] = emaFast - emaSlow
	for i in range( shift + periodSignal - 2, shift-1, -1 ):
		emaSlow = ema( period=periodSlow, shift=i, rates=rates, prev = emaSlow )
		emaFast = ema( period=periodFast, shift=i, rates=rates, prev = emaSlow )
		fastLessSlow[i-shift] = emaFast - emaSlow

	emaSignal = ema( period=periodSignal, rates=fastLessSlow )

	return( {'slow': emaSlow, 'fast': emaFast, 'signal': emaSignal } )
# end of macd


# SMMA - SMooothed Moving Average
def smma( period, shift=0, rates=None ):
	return ema( period=period, shift=shift, alpha = 1.0 / period, rates=rates )
# end of smma


# Stochastic (FSI) - Stochastic Oscillator
def stochastic( periodK=14, periodD=3, shift=0, hi=None, lo=None, cl=None ):
	(hi, lo, cl) = _defineRates( hi=hi, lo=lo, cl=cl )
	if hi is None or lo is None or cl is None:
		return None

	ratesLen = len(cl)
	if shift + periodK + periodD - 1 >= ratesLen:
		if shift + periodK - 1 >= ratesLen: # The 'K' value is also impossible to calculate?
			return None
		valueK = stochasticK( hi, lo, cl, shift, shift+periodK-1 ) # Calculating the 'K' value only
		if valueK is None:
			return None
		return( { 'K':valueK, 'D':None } )

	valuesK = np.empty( shape=periodD, dtype='float' )
	for i in range( periodD ):
		valueK = stochasticK( hi, lo, cl, shift+i, shift+i+periodK-1 )
		if valueK is None:
			return None
		valuesK[i] = valueK

	return( { 'K': valuesK[0], 'D': np.mean( valuesK ) } )
# end of stochastic

def stochasticK( hi, lo, cl, st, en ):
	minLow = lo[st]
	maxHigh = hi[st]
	for i in range( st+1, en+1 ):
		if lo[i] < minLow:
			minLow = lo[i]
		if hi[i] > maxHigh:
			maxHigh = hi[i]
	difference = maxHigh - minLow
	if not ( difference > 0 ):
		return None

	return (cl[st] - minLow) * 100.0 / difference
# end of stochasticK

	
# ROC - Rate Of Change indicator
def roc( period=12, shift=0, rates=None ):
	(rates,) = _defineRates(cl=rates)
	if rates is None:
		return None

	nPeriodsAgoIndex = shift + period 
	if nPeriodsAgoIndex >= len(rates):
		return None
	if not( rates[nPeriodsAgoIndex] > 0 ):
		return None

	return ( rates[shift] - rates[nPeriodsAgoIndex] ) * 100.0 / rates[nPeriodsAgoIndex]
# end of roc


# RSI - Relative Strength Index
def rsi( period=14, shift=0, rates=None, prev = None ):
	(rates,) = _defineRates( cl=rates )
	if rates is None:
		return None

	averageGainPrev = None
	averageLossPrev = None
	if prev is not None:
		averageGainPrev = prev['averageGain']
		averageLossPrev = prev['averageLoss']

	if (averageGainPrev is not None) and (averageLossPrev is not None):
		if shift + 1 >= len(rates):
			return None
		difference = rates[shift] - rates[shift+1]
		currentGain = 0.0
		currentLoss = 0.0
		if difference > 0.0: 
			currentGain = difference
		if difference < 0.0:
			currentLoss = -difference
		averageGain = (averageGainPrev * (period-1.0) + currentGain) / period 
		averageLoss = (averageLossPrev * (period-1.0) + currentLoss) / period 
	else:
		st = shift + period - 1
		if st + 1 >= len(rates):
			return None 
		upSum = 0.0
		downSum = 0.0
		for i in range( st, shift-1, -1 ):
			difference = rates[i] - rates[i+1]
			if difference > 0:
				upSum += difference
			elif difference < 0:
				downSum += -difference
		averageGain = upSum / period
		averageLoss = downSum / period

	if not( averageLoss > 0.0 ):
		rsiValue = 100.0
		rs = "HUGE!"
	else:
		rs = averageGain / averageLoss
		rsiValue = 100.0 - 100.0 / ( 1.0 + rs )

	return( { 'rsi':rsiValue, 'rs':rs, 'averageGain': averageGain, 'averageLoss': averageLoss } )
# end of rsi


# SMA - Simple Moving Average
def sma( period=10, shift=0, rates=None ):
	(rates,) = _defineRates( cl=rates )
	if rates is None:
		return None
	
	endIndex = shift + period
	if endIndex > len(rates):
		return None

	return np.mean( rates[shift:endIndex] )	
# end of sma


# Simulates trade
def simulateTrade( shift=0, hi=None, lo=None, tp=None, sl=None, tpSlides=False, slSlides=False, side=1, price=None, type=0 ):
	profit = None
	closedAt = -1	

	( hi, lo ) = _defineRates( hi=hi, lo=lo )
	if hi is None or lo is None:
		return None

	hiMax = np.max(hi)
	loMin = np.min(lo)
	if tp is None:
		tp = (hiMax - loMin)*100.0
	if sl is None:
		sl = (hiMax - loMin)*100.0

	if price is None:
		price = lo[shift] + (hi[shift] - lo[shift]) / 2.0

	hiLessLo = np.subtract( hi, lo )
	hiLessLoMean = np.mean( hiLessLo )

	closePrice = None

	if side == 1:
		tpPrice = price + tp
		slPrice = price - sl
	else:
		tpPrice = price - tp 
		slPrice = price + sl

	for i in range( shift, -1, -1 ):
		if side == 1:
			if hi[i] >= tpPrice:
				profit = tpPrice - price
				closedAt = i
				closePrice = tpPrice
				break
			if lo[i] <= slPrice:
				profit = slPrice - price
				closedAt = i
				closePrice = slPrice
				break
			if tpSlides == True:
				if lo[i] + tp < tpPrice:
					tpPrice = lo[i] + tp
			if slSlides:
				if hi[i] - sl > slPrice:
					slPrice = hi[i] - sl
		else:
			if hi[i] >= slPrice:
				profit = price - slPrice
				closedAt = i
				closePrice = slPrice				
				break
			if lo[i] <= tpPrice:
				profit = price - tpPrice
				closedAt = i
				closePrice = tpPrice				
				break
			if tpSlides:
				if hi[i] - tp > tpPrice:
					tpPrice = hi[i] - tp
			if slSlides:
				if lo[i] + sl < slPrice:
					slPrice = lo[i] + sl

	return { 'profit': profit, 'closedAt':closedAt, 'closePrice':closePrice }
# end of simulateTrade

def normalize( x, meanX=None, stdX=None, normInterval=[0,-1] ):
	if meanX is None:
		if normInterval[1] == -1:
			meanX = np.mean(x)
		else:
			meanX = np.mean( x[ normInterval[0]:normInterval[1] ] )			
	if stdX is None:
		if normInterval[1] == -1:
			stdX = np.std(x)
		else:
			stdX = np.std( x[ normInterval[0]:normInterval[1] ] )			
	if not( stdX > 0.0 ):
		return None, None, None
	lenX = len(x) 
	for i in range( lenX ):
		x[i] = (x[i] - meanX) / stdX
	return lenX, meanX, stdX
# end of normalize


def readFinam( fileName ):
	readError = False
	fileOpened = False
	
	linesRead = 0
	linesSkipped = 0

	from datetime import datetime 

	op = []
	hi = []
	lo = []
	cl = []
	vol = []
	dtm = []

	try:
		fileHandle = open(fileName, "r")
		fileOpened = True

		firstLine = True
		for line in fileHandle:

			if firstLine:
				firstLine = False
				linesSkipped += 1
				continue

			lineSplitted = line.split( "," )
			if len(lineSplitted) < 9:
				linesSkipped += 1
				continue

			strDate = lineSplitted[2]
			strTime = lineSplitted[3]
			dtm.append( datetime.strptime(strDate + " " + strTime, '%Y%m%d %H%M%S') )

			op.append( float( lineSplitted[4] ) )
			hi.append( float( lineSplitted[5] ) )
			lo.append( float( lineSplitted[6] ) )
			cl.append( float( lineSplitted[7] ) )
			vol.append( float( lineSplitted[8].rstrip() ) )

			linesRead += 1	
	except IOError:
		readError = True
	
	if fileOpened:
		fileHandle.close()

	if readError:
		return( None )

	op = np.array( op[::-1], dtype='float' )
	hi = np.array( hi[::-1], dtype='float' )
	lo = np.array( lo[::-1], dtype='float' )
	cl = np.array( cl[::-1], dtype='float' )
	vol = np.array( vol[::-1], dtype='float' )
	dtm = dtm[::-1]

	return { 'op':op, 'hi':hi, 'lo':lo, 'cl':cl, 'vol':vol, 'dtm':dtm, 'length':linesRead, 'skipped':linesSkipped }
# end of readFinam