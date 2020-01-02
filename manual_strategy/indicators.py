import pandas as pd  		   	  			  	 		  		  		    	 		 		   		 		  
import matplotlib.pyplot as plt  		   	  			  	 		  		  		    	 		 		   		 		  
import numpy as np  		   	  			  	 		  		  		    	 		 		   		 		  
import datetime as dt  		   	  			  	 		  		  		    	 		 		   		 		  
from util import get_data, plot_data  	

def get_momentum(df,lookback = 10):
    mmt = df/df.shift(lookback-1) - 1
    return mmt

def get_sma(df,lookback = 10):
    sma = df.rolling(window=lookback,min_periods=lookback).mean()
    return sma

def get_volatility(df, lookback = 10):
    rolling_std = df.rolling(window=lookback,min_periods=lookback).std()
    return rolling_std

def get_sma_r(df,lookback = 10):
    sma = get_sma(df)
    sma_ratio = df/sma
    return sma_ratio

def get_bb_upper(df,loopback=10):
    sma = get_sma(df)
    rolling_std = get_volatility(df)
    boll_upper = sma + 2*rolling_std
    return boll_upper    

def get_bb_lower(df,loopback=10):
    sma = get_sma(df)
    rolling_std = get_volatility(df)
    boll_lower = sma - 2*rolling_std
    return boll_lower   

def get_bbp(df, lookback = 10):
    sma = get_sma(df)
    rolling_std = get_volatility(df)
    boll_upper = get_bb_upper(df)
    boll_lower = get_bb_lower(df)
    bbp = (df - boll_lower)/(boll_upper-boll_lower)
    return bbp

def author():
    return 'tnguyen497'

if __name__ == "__main__":  

    # Get original data		   	  			  	 		  		  		    	 		 		   		 		  
    sd = dt.datetime(2008,1,1)  		   	  			  	 		  		  		    	 		 		   		 		  
    ed = dt.datetime(2009,12,31)  		 	   	  			  	 		  		  		    	 		 		   		 		  
    syms = ['JPM']
    dates = pd.date_range(sd, ed)  		   	  			  	 		  		  		    	 		 		   		 		  
    prices_all = get_data(syms, dates)	   	  			  	 		  		  		    	 		 		   		 		  
    prices_all.fillna(method ='ffill',inplace=True)  
    prices_all.fillna(method ='bfill',inplace=True)

    # normalise prices
    prices_all = prices_all/prices_all.iloc[0]
    prices = prices_all[syms]  # only portfolio symbols  		   	  			  	 		  		  		    	 		 		   		 		  
    prices_SPY = prices_all['SPY'] 

    # Momentum
    sma = get_sma(prices)
    mmt = get_momentum(prices)
    smr = get_sma_r(prices)

    bbp = get_bbp(prices)
    bb_upper = get_bb_upper(prices)
    bb_lower = get_bb_lower(prices)

    volatility = get_volatility(prices)

    # Momentum chart
    plt.figure(1)
    plt.plot(prices)
    plt.plot(mmt)
    plt.xlabel('Date')
    plt.xticks(rotation=30)
    plt.title('Normalized price and momentum')
    plt.legend(['Normalised prices','Momentum'])  
    plt.savefig("Indicator - Momemtum")

    # PLOT SMA
    plt.figure(2)
    plt.plot(prices)
    plt.plot(sma)
    plt.plot(smr)
    plt.xlabel('Date')
    plt.title('Normalized price and simple-moving-average')
    plt.legend(['Normalised prices','10-day SMA', 'price/SMA ratio'])  
    plt.savefig("Indicator - SMA")

    # PLOT BOLLINGER BAND
    plt.figure(3)
    plt.plot(prices)
    plt.plot(bbp)
    plt.plot(sma)
    plt.plot(bb_lower)
    plt.plot(bb_upper)
    plt.xlabel('Date')
    plt.xticks(rotation=30)
    plt.title('Normalized price and bollinger band indicator')
    plt.legend(['Normalised prices','Bollinger Band Percentage'])  
    plt.savefig("Indicator - Bollinger Bands")

    '''
    # PLOT VOLATILITY
    plt.figure(4)
    plt.plot(prices)
    plt.plot(volatility)
    plt.xlabel('Date')
    plt.xticks(rotation=30)
    plt.title('Normalized price volatility indicator')
    plt.legend(['Normalised prices','Volatility'])  
    plt.show()
    '''