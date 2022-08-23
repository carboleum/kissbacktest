# Kissbacktest

Keep It Simple and Stupid backtesting in Python

Explanation (in french and mathematical semantics) and example: 
follow this [link](https://carboleum.github.io/jekyll/2022/08/10/Introduction-au-backtesting.html)

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

## Load kissbacktest
```python
%load kissbacktest.py
```

## load data
```python
df = kbt_init('btceur',12*60) # 12h
```

## define signal from stategy

example:

$$
\begin{align}
    S_{in} &\equiv \bigl\( SMA_{14} > SMA_{200} \bigr\) \ \\&\  \bigl\( RSI_{14} > 60 \bigr\) \\
    S_{out} &\equiv \big\( RSI_{14} < 40 \big\)
\end{align}
$$

```python
df['RSI'] = ta.RSI(df.close, timeperiod=14)
df['long'] = ta.SMA(df.close, timeperiod=200)
df['short'] = ta.SMA(df.close,timeperiod=14)
df['sig_in'] = (df.RSI > 60) & (df.long < df.short)
df['sig_out'] = (df.RSI < 40)
```

## compute and trace graph

```python
df = kbt_compute (df)
kbt_graph(df)
```

[Result](./example-plot.html)
