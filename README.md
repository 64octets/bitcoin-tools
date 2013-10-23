
Bitcoin Tools
=============

Group of python scripts for analyzing Bitcoin.

**Prerequisites:** Python 2.7, NumPy, SciPy, Matplotlib, Pandas.

bitcoin.py
----------

A simple script for loading and analyzing bitcoin historical time-series.

Assume that we have downloaded some bitcoin historical prices, e.g., 
from Mt.Gox Bitcoin Exchange, into a csv file `data/mtgoxUSD.csv`.
You can download these data from: http://api.bitcoincharts.com/v1/csv/

**Example:**

    mtgox_raw = read_bitcoin_csv('data/mtgoxUSD.csv')
    mtgox_ohlc = get_bitcoin_ohlc(mtgox_raw, '5min')
    mtgox_ohlc['2013-01-01':].head()

**Output:**

                             open      high       low     close     amount
    date
    2013-01-01 00:00:00  13.51001  13.51001  13.51001  13.51001  36.874308
    2013-01-01 00:05:00  13.55999  13.55999  13.51001  13.51001   0.010000
    2013-01-01 00:10:00  13.51001  13.56000  13.51001  13.51001   0.010000
    2013-01-01 00:15:00  13.51001  13.51001  13.51001  13.51001   1.610000
    2013-01-01 00:20:00  13.51001  13.51002  13.51000  13.51000   0.041716

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