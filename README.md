# Kissbacktest

_Keep It Simple and Stupid backtesting coded with Python_

To have explanations (in french but with mathematical semantics and graphic illustrations): 
[kissbacktest.md](kissbacktest.md)

## Install TALib

To take full advantage of all features (technical indicators), you have to install TALib.

```bash
sudo apt install -y build-essential wget
wget http://prdownloads.sourceforge.net/ta-lib/ta-lib-0.4.0-src.tar.gz
tar -xvf ta-lib-0.4.0-src.tar.gz
cd ta-lib
./configure --prefix=/usr
make
sudo make install
```

## Install Python Libraries

```bash
sudo pip3 install TA-Lib bokeh
```

## Load kissbacktest
```python
%load kissbacktest.py
```

## Download data

Request the latest 720 values from Kraken API:
```python
df = kbt_init('XXBTZEUR',1440) # 1d
```
or download [the .cvs file directly from Kraken.com](https://support.kraken.com/hc/en-us/articles/360047124832-Downloadable-historical-OHLCVT-Open-High-Low-Close-Volume-Trades-data) and read it:
```python
df = pd.read_csv('XXBTZEUR_14400.csv')
```

## Define signal from stategy

example:

$$
\begin{align}
    S_{in} &\equiv \bigl\( SMA_{14} > SMA_{200} \bigr\) \ \\&\  \bigl\( RSI_{14} > 60 \bigr\) \\
    S_{out} &\equiv \big\( RSI_{14} < 40 \big\)
\end{align}
$$

```python
df['RSI'] = ta.RSI(df.close, timeperiod=14)
df['slow'] = ta.SMA(df.close, timeperiod=200)
df['fast'] = ta.SMA(df.close,timeperiod=14)
df['sig_in'] = (df.RSI > 60) & (df.slow < df.fast)
df['sig_out'] = (df.RSI < 40)
```

## compute and trace graph

```python
df = kbt_compute (df)
kbt_graph(df)
```

<p align="center"><img src="img/20240813-1.png" /></p>

<p align="center"><img src="img/20240813-2.png" /></p>

<p align="center"><img src="img/20240813-3.png" /></p>

<p align="center"><img src="img/20240813-4.png" /></p>

<p align="center"><img src="img/20240813-5.png" /></p>

<p align="center"><img src="img/20240813-6.png" /></p>

<p align="center"><img src="img/20240813-7.png" /></p>

<p align="center"><img src="img/20240813-8.png" /></p>

