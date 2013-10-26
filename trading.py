#!/usr/bin/env python
# Author: Peter Cerno

"""
Script for backtesting simple trading strategies.
"""

import pandas as pd
from matplotlib.dates import date2num
from bitcoin import read_bitcoin_csv, get_bitcoin_ohlc, plot_candlestick


class LongPositions(object):
    """
    Class representing long trading positions.
    """
    def __init__(self):
        self.positions = []
        self.actual_state = 0
        self.actual_position = None
    
    def open_signal(self, date, price):
        if self.actual_state == 0:
            # Enter a new long position
            self.actual_state = 1
            self.actual_position = {
                'start_date': date,
                'start_price': price}
    
    def close_signal(self, date, price):
        if self.actual_state == 1:
            # Close existing long position
            self.actual_state = 0
            self.actual_position['end_date'] = date
            self.actual_position['end_price'] = price
            self.positions.append(self.actual_position)
    
    def profit(self, balance, fee_percent = 0.01, fee_fixed = 0.):
        for position in self.positions:
            balance -= max(fee_percent * balance, fee_fixed)
            balance *= position['end_price'] / position['start_price']
        return balance
    
    def profit_series(self, series, balance, fee_percent = 0.01, fee_fixed = 0.):
        profit = series.copy()
        profit[:] = balance
        last_date = series.index[0]
        last_balance = balance
        for position in self.positions:
            profit[last_date:position['start_date']] = last_balance
            last_balance -= max(fee_percent * last_balance, fee_fixed)
            profit[position['start_date']:position['end_date']] =\
                series[position['start_date']:position['end_date']] * \
                last_balance / series.ix[position['start_date']]
            last_date = position['end_date']
            last_balance = profit.ix[last_date]
        profit[last_date:] = last_balance
        return profit


class TradingStrategyMA(object):
    """
    Trading strategy based on simple moving average.
    """
    def __init__(self, period_short=10, period_long=20):
        self.period_short = period_short
        self.period_long = period_long

    def compute(self, series):
        """
        Compute long trading positions.
        """
        long_positions = LongPositions()
        ma_short = pd.rolling_mean(series, self.period_short).dropna()
        ma_long = pd.rolling_mean(series, self.period_long).dropna()
        for date in ma_long.index:
            if ma_short[date] > ma_long[date]:
                long_positions.open_signal(date, series[date])
            elif ma_short[date] < 0.95*ma_long[date]:
                long_positions.close_signal(date, series[date])
        long_positions.close_signal(date, series[date])
        return long_positions

if __name__ == '__main__':
    # Read raw bitcoin price history from a csv file
    mtgox_raw = read_bitcoin_csv('data/mtgoxUSD.csv')
    # Get bitcoin OHLC data frame with 1h frequency
    mtgox = get_bitcoin_ohlc(mtgox_raw, '1h')
    # Select train time interval
    train_from_date = '2012-01-01'
    train_to_date = '2013-01-01'
    mtgox_train = mtgox[
        (mtgox.index >= train_from_date) &
        (mtgox.index < train_to_date)]
    # Select test time interval
    test_from_date = '2013-01-01'
    test_to_date = '2013-10-01'
    mtgox_test = mtgox[
        (mtgox.index >= test_from_date) &
        (mtgox.index < test_to_date)]
    # Initial balance
    balance = 1000
    # Find the best trading parameters
    best_profit = 0
    best_params = None
    for period_short in [10, 20, 30, 40, 50]:
        for period_long in [period_short + delta for delta in [10, 20, 30, 40, 50]]:
            trading = TradingStrategyMA(period_short, period_long)
            long_positions = trading.compute(mtgox_train.close)
            profit = long_positions.profit(balance)
            if profit > best_profit:
                best_profit = profit
                best_params = {
                    'period_short': period_short,
                    'period_long': period_long}
    # Print training result
    print 'Training benchmark: %.2f' % \
        (balance * mtgox_train.close[-1] / mtgox_train.close[0])
    print 'Best training profit: %.2f' % best_profit
    print 'Best training parameters: ' + str(best_params)
    trading = TradingStrategyMA(
        best_params['period_short'], 
        best_params['period_long'])
    # Test
    long_positions = trading.compute(mtgox_test.close)
    profit = long_positions.profit(balance)
    print 'Test benchmark: %.2f' % \
        (balance * mtgox_test.close[-1] / mtgox_test.close[0])
    print 'Test profit %.2f' % profit
    # Plot test profit series
    (ax0, ax1) = plot_candlestick(mtgox_test, candle_width=1./24., freq='1M')
    profit_series = long_positions.profit_series(mtgox_test.close, mtgox_test.close[0])
    ma_short = pd.rolling_mean(mtgox_test.close, best_params['period_short']).dropna()
    ma_long = pd.rolling_mean(mtgox_test.close, best_params['period_long']).dropna()
    ax0.plot(date2num(ma_short.index), ma_short.values, 'y')
    ax0.plot(date2num(ma_long.index), ma_long.values, 'b')
    ax0.plot(date2num(profit_series.index), profit_series.values, 'g')