#!/usr/bin/env python
# Author: Peter Cerno

"""
Script for loading and analyzing bitcoin historical time-series.
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.dates import num2date
from matplotlib.dates import date2num
from matplotlib.finance import candlestick_ochl


def read_bitcoin_csv(bitcoin_csv_file_name):
    """
    Read raw bitcoin price history from a csv file with the following format:
    unixtime, price, amount
    Bitcoin price history source:
    http://www.bitcoincharts.com/
    http://api.bitcoincharts.com/v1/csv/
    """
    # Read bitcoin csv file
    frame = pd.read_csv(bitcoin_csv_file_name, header=None)
    frame.columns = ['date', 'price', 'amount']
    frame['date'] = pd.to_datetime(frame['date'], unit='s')
    frame.set_index(frame['date'], inplace=True)
    frame = frame[['price', 'amount']]
    return frame

def remove_bitcoin_date_duplicates(frame):
    """
    Remove bitcoin date duplicates by using (weighted) aggregation.
    @param frame: raw bitcoin price history.
    """
    # Aggregate duplicate dates
    frame['price'] = frame['price'] * frame['amount']
    frame = frame.groupby(level=0).sum()
    frame['price'] = np.round(frame['price'] / frame['amount'], 5)
    return frame

def get_bitcoin_ohlc(frame, freq='1D'):
    """
    Compute bitcoin OHLC data frame with the given frequency.
    @param frame: raw bitcoin price history.
    @param freq: target OHLC frequency.
    """
    ohlc = frame['price'].resample(freq, how='ohlc')
    close = frame['price'].resample(freq, how='last', fill_method='ffill')
    for column in ['open', 'high', 'low', 'close']:
        ohlc[column] = np.where(np.isnan(ohlc[column]), close, ohlc[column])
    ohlc['amount'] = frame['amount'].resample(freq, how='last')
    ohlc['amount'].fillna(0.0, inplace=True)
    return ohlc

def plot_candlestick(frame, ylabel='BTC/USD', candle_width=1.0, freq='1M'):
    """
    Plot candlestick graph.
    @param frame: bitcoin OHLC data frame to be plotted.
    @param ylabel: label on the y axis.
    @param candle_width: width of the candles in days.
    @param freq: frequency of the plotted x labels.
    """
    candlesticks = list(zip(
        date2num(frame.index._mpl_repr()),
        frame['open'],
        frame['close'],
        frame['high'],
        frame['low'],
        frame['amount']))
    # Figure
    ax0 = plt.subplot2grid((3,1), (0,0), rowspan=2)
    ax1 = plt.subplot2grid((3,1), (2,0), rowspan=1, sharex=ax0)
    plt.subplots_adjust(bottom=0.15)
    plt.setp(ax0.get_xticklabels(), visible=False)
    ax0.grid(True)
    ax0.set_ylabel(ylabel, size=20)
    # Candlestick
    candlestick_ochl(ax0, candlesticks, 
        width=0.5*candle_width, 
        colorup='g', colordown='r')
    # Get data from candlesticks for a bar plot
    dates = np.asarray([x[0] for x in candlesticks])
    volume = np.asarray([x[5] for x in candlesticks])
    # Make bar plots and color differently depending on up/down for the day
    pos = np.nonzero(frame['close'] - frame['open'] > 0)
    neg = np.nonzero(frame['open'] - frame['close'] > 0)
    ax1.grid(True)
    ax1.bar(dates[pos], volume[pos], color='g', width=candle_width, align='center')
    ax1.bar(dates[neg], volume[neg], color='r', width=candle_width, align='center')
    # Scale the x-axis tight
    ax1.set_xlim(min(dates),max(dates))
    ax1.set_ylabel('VOLUME', size=20)
    # Format the x-ticks with a human-readable date. 
    xt = [date2num(date) for date in pd.date_range(
            start=min(frame.index), 
            end=max(frame.index),
            freq=freq)]
    ax1.set_xticks(xt)
    xt_labels = [num2date(d).strftime('%Y-%m-%d\n%H:%M:%S') for d in xt]
    ax1.set_xticklabels(xt_labels,rotation=45, horizontalalignment='right')
    # Plot
    plt.show()
    return (ax0, ax1)


if __name__ == '__main__':
    # Read raw bitcoin price history from a csv file
    bitstamp_raw = read_bitcoin_csv('data/bitstampUSD.csv')
    # Get bitcoin OHLC data frame with 1h frequency
    bitstamp = get_bitcoin_ohlc(bitstamp_raw, '1h')
    # Select a specific time interval
    from_date = '2013-06-01'
    to_date = '2013-06-07'
    bitstamp = bitstamp[
        (bitstamp.index >= from_date) &
        (bitstamp.index < to_date)]
    # Plot candlestick graph
    plot_candlestick(bitstamp, candle_width=1./24., freq='1D')