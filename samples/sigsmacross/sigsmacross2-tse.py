
#!/usr/bin/env python
# -*- coding: utf-8; py-indent-offset:4 -*-
###############################################################################
#
# Copyright (C) 2016 Daniel Rodriguez
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
###############################################################################
from __future__ import (absolute_import, division, print_function,
                        unicode_literals)
import pandas
import backtrader.feeds as btfeeds
import argparse
from tehran_stocks import Stocks, db
from datetime import datetime
import backtrader as bt


class SmaCross(bt.SignalStrategy):
    def __init__(self):
        sma1 = bt.ind.SMA(period=10)
        sma2 = bt.ind.SMA(period=30)
        crossover = bt.ind.CrossOver(sma1, sma2)
        self.signal_add(bt.SIGNAL_LONG, crossover)


def tsedata():
    # Create a cerebro entity
    cerebro = bt.Cerebro(stdstats=False)

    # Add a strategy
    cerebro.addstrategy(bt.Strategy)

    stock_by_symbol = Stocks.query.filter_by(
        name='كگل').first()  # find by symbol(نماد)

    print('--------------------------------------------------')
    print(stock_by_symbol.df)
    print('--------------------------------------------------')

    tsedf = stock_by_symbol.df.drop(
        columns=['code', 'id', 'ticker', 'vol', 'per', 'open', 'dtyyyymmdd', 'last'])
    tsedf = tsedf.rename(columns={'date': 'Date', 'first': 'Open', 'high': 'High',
                                  'low': 'Low', 'close': 'Close', 'value': 'Volume', 'openint': 'OpenInterest'})
    tsedf = tsedf[['Date', 'Open', 'High', 'Low',
                   'Close', 'Volume', 'OpenInterest']]
    # tsedf['Date'] = pandas.to_datetime(tsedf['Date'].astype(str), format='%Y-%m-%d')
    data = bt.feeds.PandasData(dataname=tsedf, datetime='Date', nocase=True,)
    return data


cerebro = bt.Cerebro()
cerebro.addstrategy(SmaCross)

data0 = bt.feeds.YahooFinanceData(dataname='YHOO',
                                  fromdate=datetime(2011, 1, 1),
                                  todate=datetime(2012, 12, 31))

cerebro.adddata(tsedata())

cerebro.run()
cerebro.plot()
