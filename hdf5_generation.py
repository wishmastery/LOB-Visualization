import numpy as np
import pandas as pd
from pandas import HDFStore, DataFrame

store = pd.HDFStore('store.h5')

num_levels = 10
column_names = [['ask'+str(i+1)+'p','ask'+str(i+1)+'q','bid'+str(i+1)+'p','bid'+str(i+1)+'q'] for i in range(num_levels)]
column_names = [names for levels in column_names for names in levels]
df = pd.read_csv('orderbook.csv', names = column_names, dtype=int)
price_names = [['ask'+str(i+1)+'p','bid'+str(i+1)+'p'] for i in range(num_levels)]
price_names = [names for levels in price_names for names in levels]
df_prices = df[price_names]
quantity_names = [['ask'+str(i+1)+'q','bid'+str(i+1)+'q'] for i in range(num_levels)]
quantity_names = [names for levels in quantity_names for names in levels]
df_quantity = df[quantity_names]
df_prices.to_hdf('store.h5', 'prices', append=True)
df_quantity.to_hdf('store.h5', 'quantity', append=True)
