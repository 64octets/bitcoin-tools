
Bitcoin Tools
=============

Group of python scripts for analyzing Bitcoin.

**Prerequisites:** 

- Python 2.7, NumPy, SciPy, Matplotlib, Pandas.
- We assume that you have downloaded some bitcoin historical prices, e.g., 
from Mt.Gox Bitcoin Exchange, into a csv file `data/mtgoxUSD.csv`.
You can download these data from: http://api.bitcoincharts.com/v1/csv/

bitcoin.py
----------

Script for loading and analyzing bitcoin historical time-series.

**Example:**

    # Read raw bitcoin price history from a csv file
    mtgox_raw = read_bitcoin_csv('data/mtgoxUSD.csv')
    # Get bitcoin OHLC data frame with 5min frequency
    mtgox_ohlc = get_bitcoin_ohlc(mtgox_raw, '5min')
    # Sample output
    mtgox_ohlc['2013-01-01':].head()

**Output:**

                             open      high       low     close     amount
    date
    2013-01-01 00:00:00  13.51001  13.51001  13.51001  13.51001  36.874308
    2013-01-01 00:05:00  13.55999  13.55999  13.51001  13.51001   0.010000
    2013-01-01 00:10:00  13.51001  13.56000  13.51001  13.51001   0.010000
    2013-01-01 00:15:00  13.51001  13.51001  13.51001  13.51001   1.610000
    2013-01-01 00:20:00  13.51001  13.51002  13.51000  13.51000   0.041716

trading.py
----------

Script for backtesting simple trading strategies.

We make the following simplifying assumptions:

- At any time during trading all our resources are allocated either in BTC 
or in USD. Therefore, we consider only *long positions*, during which all our 
resources are allocated in BTC.
- We use BTC/USD as our *benchmark*. In other words, a trading strategy
beats the benchmark if and only if it is better than mere holding of BTC.

Class `LongPositions` is used for bookkeeping our trades. It can compute
the resulting profit and profit time-series.

Class `TradingStrategyMA` is a simple trading strategy based on two
moving averages - one with a short period and one with a long period.

**Example:**

    # Read raw bitcoin price history from a csv file
    mtgox_raw = read_bitcoin_csv('data/mtgoxUSD.csv')
    # Get bitcoin OHLC data frame with 1h frequency
    mtgox = get_bitcoin_ohlc(mtgox_raw, '1h')
    # Select test time interval
    test_from_date = '2013-01-01'
    test_to_date = '2013-10-01'
    mtgox_test = mtgox[
        (mtgox.index >= test_from_date) &
        (mtgox.index < test_to_date)]
    # Initial balance
    balance = 1000
    # Initialize a trading strategy
    trading = TradingStrategyMA(30, 50)
    # Compute long positions
    long_positions = trading.compute(mtgox_test.close)
    # Compute resulting profit
    profit = long_positions.profit(balance)
    # Compare resulting profit with BTC/USD benchmark
    print 'Test benchmark: %.2f' % \
        (balance * mtgox_test.close[-1] / mtgox_test.close[0])
    print 'Test profit %.2f' % profit

**Output:**

    Test benchmark: 10464.34
    Test profit 17674.91

LICENSE
=======

The Bitcoin Tools project is licensed to you under MIT.X11:

Copyright (c) 2013 Peter Cerno.

Permission is hereby granted, free of charge, to any person obtaining
a copy of this software and associated documentation files (the
"Software"), to deal in the Software without restriction, including
without limitation the rights to use, copy, modify, merge, publish,
distribute, sublicense, and/or sell copies of the Software, and to
permit persons to whom the Software is furnished to do so, subject to
the following conditions:

The above copyright notice and this permission notice shall be
included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE
LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION
WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.