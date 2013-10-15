#!/usr/bin/env python
# Author: Peter Cerno

"""
A simple script for loading and analyzing bitcoin historical time-series.
"""

import numpy as np
import pandas as pd

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
    """
    # Aggregate duplicate dates
    frame['price'] = frame['price'] * frame['amount']
    frame = frame.groupby(level=0).sum()
    frame['price'] = np.round(frame['price'] / frame['amount'], 5)
    return frame

def get_bitcoin_ohlc(frame, rule='5min'):
    """
    Compute bitcoin OHLC data frame with the given frequency.
    """
    ohlc = frame['price'].resample(rule, how='ohlc')
    close = frame['price'].resample(rule, how='last', fill_method='ffill')
    for column in ['open', 'high', 'low', 'close']:
        ohlc[column] = np.where(np.isnan(ohlc[column]), close, ohlc[column])
    ohlc['amount'] = frame['amount'].resample(rule, how='last')
    ohlc['amount'].fillna(0.0, inplace=True)
    return ohlc