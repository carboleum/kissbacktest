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
    
def kbt_graph (df):
    df['time'] = pd.to_datetime(df['time'], unit='s')
    xformatter = DatetimeTickFormatter(hours="%H:%M", days="%d/%m", months="%m/%Y", years="%Y")
    
    p1 = figure(height=300,width=800)
    p1.xaxis[0].formatter = xformatter
    p1.line(df.time,df.close)
    if 'slow' in df:
        p1.line(df.time,df.slow,color='red')
    if 'fast' in df:
        p1.line(df.time,df.fast,color='green')
    #p2 =  figure(height=100,width=800,x_range=p1.x_range)
    #p2.xaxis[0].formatter = xformatter
    #p2.line(df.time,df.RSI)
    #p3_0 = figure(height=100,width=800,x_range=p1.x_range)
    #p3_0.xaxis[0].formatter = xformatter
    #p3_0.line(df.time,df.trend)
    p3_1 = figure(height=100,width=800,x_range=p1.x_range)
    p3_1.xaxis[0].formatter = xformatter
    p3_1.line(df.time,df.sig_in,color='green')
    p3_2 = figure(height=100,width=800,x_range=p1.x_range)
    p3_2.xaxis[0].formatter = xformatter
    p3_2.line(df.time,df.sig_out,color='red')
    p3_3 = figure(height=100,width=800,x_range=p1.x_range)
    p3_3.xaxis[0].formatter = xformatter
    p3_3.line(df.time,df.sig_0)
    p3_3_2 = figure(height=100,width=800,x_range=p1.x_range)
    p3_3_2.xaxis[0].formatter = xformatter
    p3_3_2.line(df.time,df.sig_1)
    p3_4 = figure(height=100,width=800,x_range=p1.x_range)
    p3_4.xaxis[0].formatter = xformatter
    p3_4.line(df.time,df.signal)
    p4 = figure(height=150,width=800,x_range=p1.x_range)
    p4.xaxis[0].formatter = xformatter
    p4.line(df.time,df.r_0,color='lightgray')
    p4.line(df.time,df.r_strat)
    p4.line(df.time,df.r_fee,color='red')
    p5 = figure(height=300,width=800,x_range=p1.x_range)
    p5.xaxis[0].formatter = xformatter
    p5.line(df.time,df.r_0.cumprod(),color='lightgray')
    p5.line(df.time,df.r_strat.cumprod())
    p5.line(df.time,df.R_net,color='red')
    layout = column(p1,p3_1,p3_2,p3_3,p3_3_2,p3_4,p4,p5)
    show(layout)
