# Kissbacktet

## Load kissbacktest
```python
%load kissbacktest.py
```

## load data
```python
df = kbt_init('btceur',12*60) # 12h
```

## define signal from stategy

$$
\begin{align}
    S_in \equiv \bigl\( SMA_{14} > SMA_{200} \bigr\) \& bigl\( RSI_{14} > 60 \bigr\)
    S_out \equiv \big\( RSI_{14} < 40 \big\)
\end{align}
$$

```python
df['RSI'] = ta.RSI(df.close, timeperiod=14)
df['long'] = ta.SMA(df.close, timeperiod=200)
df['short'] = ta.SMA(df.close,timeperiod=14)
df['sig_in'] = (df.RSI > 60) & (df.long < df.short)
df['sig_out'] = (df.RSI < 40)
```

## compute and trace kbt_graph

```python
df = kbt_compute (df)
kbt_graph(df)
```
