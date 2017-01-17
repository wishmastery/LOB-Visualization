#!/usr/bin/python
# plot.py

import numpy as np
import matplotlib
import sys
import matplotlib.pyplot as plt
import matplotlib.colors as clrs
import matplotlib.cm as cm
import pandas as pd
from pandas import HDFStore, DataFrame

plt.style.use('ggplot')
fig, ax = plt.subplots()
store = pd.HDFStore('store.h5')
df_price = store.prices
df_quantity = store.quantity
data_length = len(df_price.index)
num_of_bars = 200
num_of_levels = int(len(df_price.columns)/2)

canvas = np.zeros((100, 200))
cmap=cm.jet
cmap.set_under("White")
p = ax.imshow(canvas, cmap = cmap, interpolation='nearest', vmin = 0.01)

def reorder(df):
    column_names = df.columns.tolist()
    ask = column_names[::2]
    bid = column_names[::-2]
    column_names = bid+ask
    df = df[column_names]
    return df

def plot_im(df_price, df_quantity):
    global p
    assert len(df_price.index) == len(df_quantity.index), 'Data length of prices and quantity does not match'
    if len(df_price.index) > num_of_bars: df_price = df_price[:num_of_bars]
    if len(df_quantity.index) > num_of_bars: df_quantity = df_quantity[:num_of_bars]
    min_price = df_price['bid'+str(num_of_levels)+'p'].min()
    max_price = df_price['ask'+str(num_of_levels)+'p'].max()
    num_of_ticks = int(1+(max_price - min_price) / 100)
    # print(min_price, max_price, num_of_ticks)
    df_price = (df_price-min_price)/100
    df_price = df_price.astype(int)
    canvas = np.zeros((num_of_bars, num_of_ticks*3))

    column_names = df_quantity.columns.tolist()
    start_index = df_price.index[0]
    print(start_index)
    for index, row in df_price.iterrows():
        for j, price_level in enumerate(row):
            canvas[index-start_index][3*price_level] = df_quantity[column_names[j]][index-start_index]
            canvas[index-start_index][3*price_level+1] = df_quantity[column_names[j]][index-start_index]
            canvas[index-start_index][3*price_level+2] = df_quantity[column_names[j]][index-start_index]
    canvas = np.transpose(canvas)
    canvas = np.flipud(canvas)
    p.set_data(canvas)
    # print(df_price)
    # print(df_quantity)

df_price = reorder(df_price)
df_quantity = reorder(df_quantity)
plot_start_point = 0

while plot_start_point + num_of_bars < data_length:
    plot_im(df_price[plot_start_point:plot_start_point+num_of_bars], df_quantity[plot_start_point:plot_start_point+num_of_bars])
    plot_start_point += 1


