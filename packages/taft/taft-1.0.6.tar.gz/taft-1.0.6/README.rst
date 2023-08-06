TAFT: Technical Analysis tools For Trading
==========================================

version 1.0.2

    **Important notice**: Quotes and volumes (numpy-arrays given as
    arguments to the functions listed below) are required to be indexed
    so that the most **old** value has the **biggest** index while the
    most **new** one has index **0**.

Indicators
----------

AD-indicator
~~~~~~~~~~~~

::

    def ad( period=1, shift=0, hi=None, lo=None, cl=None, vo=None, prev=None )

::

    period (int) - the period of the indicator, default: 1
    shift (int) - the shift inside the data arrays (hi,lo,l,vo) to calculate the indicator at, default: 0
    hi (numpy array, float) - HIGH rates
    lo (numpy array, float) - LOW rates
    cl (numpy array, float) - CLOSE rates
    vo (numpy array, float) - volumes
    prev (float) - the value previously returned by the function, default: None 

    Returns (float) - the value of the indicator, 'None' if failed

`See the sample code here <samples/test-ad.py>`__

ADX-indicator
~~~~~~~~~~~~~

::

    def adx( period=14, shift=0, hi=None, lo=None, cl=None, prev=None )

::

    period (int) - the period of the indicator, default: 14
    shift (int) - the shift inside the data arrays (hi,lo,cl) to calculate the indicator for, default: 0
    hi (numpy array, float) - HIGH rates
    lo (numpy array, float) - LOW rates
    cl (numpy array, float) - CLOSE rates
    prev (dict) - previously returned by the function, default: None 

    Returns (dict) - { 'adx': the ADX value, 'dx': the DX value, "+DI": the "+DI" value, "-DI": the "-DI value, 
    "+DMsm": the smoothed "+DM" value, "-DMsm": the smoothed "-DM" value, "TRsm": the smoothed 'true-range' value }, 'None' if failed

`See the sample code here <samples/test-adx.py>`__

ATR - Average True Range
~~~~~~~~~~~~~~~~~~~~~~~~

::

        def atr( period=14, shift=0, hi=None, lo=None, cl=None, prev=None ):

::

    period (int) - the period of the indicator, default: 14
    shift (int) - the shift inside the data arrays (hi,lo,cl) to calculate the indicator for, default: 0
    hi (numpy array, float) - HIGH rates
    lo (numpy array, float) - LOW rates
    cl (numpy array, float) - CLOSE rates
    prev (float) - the value previously returned by the function, default: None 

    Returns (dict) - { 'atr': the average true-range value, 'tr' - the last rue-range value }, 'None' if failed

`See the sample code here <samples/test-atr.py>`__

Bollinger Bands
~~~~~~~~~~~~~~~

::

    def bollinger( period=20, shift=0, nStds = 2.0, rates=None ):

::

    period (int) - the period of the indicator, default: 20
    shift (int) - the shift inside the 'rates' array to calculate the indicator for, default: 0
    nStds (float) - the number of standard deviations to calculate 'upper' and 'lower' values of the indicator, default:2
    rates (numpy array, float) - rates

    Returns (dict) - { 'middle': the 'middle' value of the bollinger, 'upper': the upper value of the bollinger, 
    'lower' - the lower value of the bollinger, 'std': the standard deviation value ), 'None' if failed

`See the sample code here <samples/test-bollinger.py>`__

CCI Commodity Channel Index indicator
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

::

    def cci( period=20, shift=0, hi=None, lo=None, cl=None, cciConst=0.015 ):

::

    period (int) - the period of the indicator, default: 20
    shift (int) - the shift inside the data arrays (hi,lo,cl) to calculate the indicator for, default: 0
    hi (numpy array, float) - HIGH rates
    lo (numpy array, float) - LOW rates
    cl (numpy array, float) - CLOSE rates
    cciConst (float) - the constant used in the indicator formula, default: 0.015 

    Returns (dict) - { 'cci': the value of the indicator, 'meanTypicalPrice': the mean 'typical price', 
    'meanDeviation': the mean deviation of typical price against the mean value }, 'None' if failed

`See the sample code here <samples/test-cci.py>`__

EMA - Exponential Moving Average
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

::

    def ema( period=10, shift=0, alpha=None, rates=None, prev=None ):           

::

    period (int) - the period  of the indicator, default: 10
    shift (int) - the shift inside the 'rates' array to calculate the indicator for, default: 0 (the last received rate)
    alpha (float) - the smoothing factor, default: 2.0 / (period + 1.0)
    rates (numpy array, float) - HIGH rates
    prev (float) - the value previously returned by the function

    Returns (float) - the EMA value, 'None' if failed

`See the sample code here <samples/test-ma.py>`__

Stochastic-oscillator
~~~~~~~~~~~~~~~~~~~~~

::

    def stochastic( periodK=14, periodD=3, shift=0, hi=None, lo=None, cl=None ):

::

    periodK (int) - the period  of the 'fast' stochastic line, default: 14
    periodD (int) - the period  of the 'slow' stochastic line, default: 3
    shift (int) - the shift inside the data arrays (hi,lo,cl) to calculate the indicator for, default: 0
    hi (numpy array, float) - HIGH rates
    lo (numpy array, float) - LOW rates
    cl (numpy array, float) - CLOSE rates

    Returns: the 'K' ('fast) stochastic value, 'D': the 'D' ('slow') tochastic value, 'None' if failed.

`See the sample code here <samples/test-stochastic.py>`__

ROC - The Rate Of Change indicator
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

::

    def roc( period=12, shift=0, rates=None ):

::

    period (int) - the period of the indicator, default: 12
    shift (int) - the shift inside the 'rates' array to calculate the indicator for, default: 0 (the last received rate)
    rates (numpy array, float) - the rates

    Returns (float) - the rate of change (ROC) value, 'None' if failed

RSI - Relative Strength Index
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

::

    def rsi( period=14, shift=0, rates=None, prev=None ):

::

    period (int) - the period of the indicator, default: 14
    shift (int) - the shift inside the 'rates' array to calculate the indicator for, default: 0 (the last received rate)
    rates (numpy array, float) - the rates
    prev (dict) - the value previously returned by the function

    Returns (dict) - { 'rsi':the RSI value, 'rs': the Relative Strength value, 
    'averageGain': the 'average gain' value, 'averageLoss': the 'average loss' value }, 'None' if failed

`See the sample code here <samples/test-rsi.py>`__

SMA - Simple Moving Average
~~~~~~~~~~~~~~~~~~~~~~~~~~~

::

    def sma( period=10, shift=0, rates=None ):

::

    period (int) - the period of the indicator, default: 10
    shift (int) - the shift inside the 'rates' array to calculate the indicator for, default: 0 (the last received rate)
    rates (numpy array, float) - the rates

    Returns (float) - the SMA value, 'None' if failed 

Simulation and Analysis
-----------------------

simulateTrade
~~~~~~~~~~~~~

    Simulates trade - opening and closing a position. 
::

    def simulateTrade( shift=0, hi=None, lo=None, tp=None, sl=None, tpSlides=False, slSlides=False, side=1, price=None, type=0 ): 
::

    shift (int) - the shift inside the 'rates' arrays (hi,lo,cl), i.e. the index at which the trade is 'opened' 
    hi (numpy array, float) - HIGH rates 
    lo (numpy array, float) - LOW rates 
    tp (float) - the 'take profit' value, if 'None' a huge value of (max(hi)-min(lo))*100.0 is used
    sl (float) - the 'stop loss' value, if 'None' a huge value of (max(hi)-min(lo))*100.0 is used
    tpSlides (boolean) - if 'True' a sliding take profit is used 
    slSlides (boolean) - if 'True' a sliding stop loss is used 
    side (int) - the value of '1' simulates open LONG, the value of '-1' simulates open short 
    price (float) - the 'current' (initial) price, if 'None' the value of 'current price' is the mean between lo[shift] and hi[shift]

    Returns (dict): { 
        'profit' (float): the profit in points;
        'closedAt' (int): the index value (inside the 'hi' and 'lo' arrays) where the trade was 'closed', 
            '-1' if neigther stop loss nor take profit has been reached till the end of the arrays;
        'closePrice' (float): close price
    }

Utilities
---------

normalize
~~~~~~~~~

    Normalizes the values of an array with the following formula: x[i] = (x[i] - <mean-of-x>) / <standard-deviation-of-x> 

::
    def normalize( x ): 

::
    x (numpy array, float) - the array to be normalized

    Returns: nothing

readFinam
~~~~~~~~~

Loads rates from Finam file 

::
    
    def readFinam( fileName ): 

::
    
    fileName (string) - the name of the file with Finam rates.
    
    Returns (dict): {
        'op' (numpy-array, float): open rates, '0' index takes the latest rate
        'hi' (numpy-array, float): high rates, '0' index takes the latest rate
        'lo' (numpy-array, float): low rates, '0' index takes the latest rate
        'cl' (numpy-array, float): close rates, '0' index takes the latest rate
        'vol' (numpy-array, float): volumes, '0' index takes the volume of the latest period
        'dtm' (list, datetime): date&time, '0' index takes the date and time of the latest period
    }

