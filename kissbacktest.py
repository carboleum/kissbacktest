# coding: utf-8
import requests
import numpy as np
import pandas as pd
from bokeh.plotting import figure,show
from bokeh.layouts import column,row
from bokeh.models import DatetimeTickFormatter

import talib as ta

def kbt_init (pair,period):
    url = f'https://api.kraken.com/0/public/OHLC?pair={pair}&interval={period}'
    ohlc = requests.get(url).json()['result'][pair]
    columns = ['time','open','high','low','close','vwap','volume','count']
    df = pd.DataFrame(ohlc, columns=columns).astype(float)
    df = df.iloc[-1000:]
    return df

def kbt_compute (df):
    # signal
    if not 'signal' in df:
        df['sig_0'] = df.sig_in.astype(int) - df.sig_out.astype(int)
        df['sig_1'] = df.sig_0.where(df.sig_0!=0).ffill()
        df['signal'] = df.sig_1 > 0
    # Rendements
    df['close'] = df.close.replace(to_replace=0, method='ffill')
    df['r_0'] = df.close / df.close.shift()
    df['r_strat'] = np.where(df.signal.shift(), df.r_0, 1)
    df['r_fee'] = np.where(df.signal.shift() + df.signal == 1, 1-0.0025, 1)
    # Rendement cumulé
    df['R_net'] = (df.r_strat * df.r_fee).cumprod()
    return df
    
def kbt_graph (df, y_axis_type = "linear", full=False):

    lst = []
    df['time'] = pd.to_datetime(df.time, unit='s')
    
    f0 = figure(height = 300, width = 800, x_axis_type = 'datetime', y_axis_type = y_axis_type)
    f0.line(df.time,df.close)
    if 'slow' in df:
        f0.line(df.time,df.slow,color='red')
    if 'fast' in df:
        f0.line(df.time,df.fast,color='green')
    f0.triangle(df.time, df.close.where((df.signal == 1) & (df.signal.shift() == 0)), color='green', size=7)
    f0.inverted_triangle(df.time, df.close.where((df.signal == 0) & (df.signal.shift() == 1)), color='red', size=7)
    lst.append(f0)
    
    #p2 =  figure(height=100,width=800,x_range=f0.x_range, x_axis_type = 'datetime')
    #p2.line(df.time,df.RSI)
    
    #p3_0 = figure(height=100,width=800,x_range=f0.x_range, x_axis_type = 'datetime')
    #p3_0.line(df.time,df.trend)

    if full:
        if 'sig_in' in df:
            fig = figure(height=100,width=800,x_range=f0.x_range, x_axis_type = 'datetime')
            fig.line(df.time,df.sig_in,color='green')
            lst.append(fig)

        if 'sig_out' in df:
            fig = figure(height=100,width=800,x_range=f0.x_range, x_axis_type = 'datetime')
            fig.line(df.time,df.sig_out,color='red')
            lst.append(fig)
    
        if 'sig_0' in df:
            fig = figure(height=100,width=800,x_range=f0.x_range, x_axis_type = 'datetime')
            fig.line(df.time,df.sig_0)
            lst.append(fig)

    if 'sig_1' in df:
        fig = figure(height=100,width=800,x_range=f0.x_range, x_axis_type = 'datetime')
        fig.line(df.time,df.sig_1)
        lst.append(fig)
    
    fig = figure(height=100,width=800,x_range=f0.x_range, x_axis_type = 'datetime')
    fig.line(df.time,df.signal)
    lst.append(fig)

    if full:
        fig = figure(height=150,width=800,x_range=f0.x_range, x_axis_type = 'datetime')
        fig.line(df.time,df.r_0,color='lightgray')
        fig.line(df.time,df.r_strat)
        fig.line(df.time,df.r_fee,color='red')
        lst.append(fig)
    
    fig = figure(height = 300, width = 800, x_range = f0.x_range, x_axis_type = 'datetime', y_axis_type = y_axis_type)
    fig.line(df.time,df.r_0.cumprod(),color='lightgray')
    fig.line(df.time,df.r_strat.cumprod())
    fig.line(df.time,df.R_net,color='red')
    lst.append(fig)
     
    show(column(lst))
