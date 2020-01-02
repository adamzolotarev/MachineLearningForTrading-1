"""MC2-P1: Market simulator.  		   	  			  	 		  		  		    	 		 		   		 		  
  		   	  			  	 		  		  		    	 		 		   		 		  
Copyright 2018, Georgia Institute of Technology (Georgia Tech)  		   	  			  	 		  		  		    	 		 		   		 		  
Atlanta, Georgia 30332  		   	  			  	 		  		  		    	 		 		   		 		  
All Rights Reserved  		   	  			  	 		  		  		    	 		 		   		 		  
  		   	  			  	 		  		  		    	 		 		   		 		  
Template code for CS 4646/7646  		   	  			  	 		  		  		    	 		 		   		 		  
  		   	  			  	 		  		  		    	 		 		   		 		  
Georgia Tech asserts copyright ownership of this template and all derivative  		   	  			  	 		  		  		    	 		 		   		 		  
works, including solutions to the projects assigned in this course. Students  		   	  			  	 		  		  		    	 		 		   		 		  
and other users of this template code are advised not to share it with others  		   	  			  	 		  		  		    	 		 		   		 		  
or to make it available on publicly viewable websites including repositories  		   	  			  	 		  		  		    	 		 		   		 		  
such as github and gitlab.  This copyright statement should not be removed  		   	  			  	 		  		  		    	 		 		   		 		  
or edited.  		   	  			  	 		  		  		    	 		 		   		 		  
  		   	  			  	 		  		  		    	 		 		   		 		  
We do grant permission to share solutions privately with non-students such  		   	  			  	 		  		  		    	 		 		   		 		  
as potential employers. However, sharing with other current or future  		   	  			  	 		  		  		    	 		 		   		 		  
students of CS 7646 is prohibited and subject to being investigated as a  		   	  			  	 		  		  		    	 		 		   		 		  
GT honor code violation.  		   	  			  	 		  		  		    	 		 		   		 		  
  		   	  			  	 		  		  		    	 		 		   		 		  
-----do not edit anything above this line---  		   	  			  	 		  		  		    	 		 		   		 		  
  		   	  			  	 		  		  		    	 		 		   		 		  
Student Name: Tucker Balch (replace with your name)  		   	  			  	 		  		  		    	 		 		   		 		  
GT User ID: tb34 (replace with your User ID)  		   	  			  	 		  		  		    	 		 		   		 		  
GT ID: 900897987 (replace with your GT ID)  		   	  			  	 		  		  		    	 		 		   		 		  
"""  		   	  			  	 		  		  		    	 		 		   		 		  
  		   	  			  	 		  		  		    	 		 		   		 		  
import pandas as pd  		   	  			  	 		  		  		    	 		 		   		 		  
import numpy as np  		   	  			  	 		  		  		    	 		 		   		 		  
import datetime as dt  		   	  			  	 		  		  		    	 		 		   		 		  
import os  		   	  			  	 		  		  		    	 		 		   		 		  
from util import get_data, plot_data  		   	  			  	 		  		  		    	 		 		   		 		  
  		   	  			  	 		  		  		    	 		 		   		 		  
def compute_portvals(df_input, start_val = 100000, commission=9.95, impact=0.005):  		   	  			  	 		  		  		    	 		 		   		 		  

 #   df_input = df_input[df_input != 0 ]
 #   df_input.dropna(inplace=True)
  #  print(df_input)
    cols = df_input.columns.tolist()
    sym = cols[0]
    syms=[sym]

    df_input.sort_index(inplace=True)
    start_date = df_input.index.min()
    end_date = df_input.index.max() 		   	  			  	 		  		  		    	 		 		   		 		  
    prices = get_data(syms, pd.date_range(start_date, end_date))  		   	  			  	 		  		  		    	 		 		   		 		  
    prices = prices[syms]  # remove SPY  		 
    prices.fillna(method ='ffill',inplace=True)  
    prices.fillna(method ='bfill',inplace=True)   
    prices['Cash']= 1
 
    trades = pd.DataFrame(columns=syms+['Cash'],index=pd.date_range(start_date, end_date))	
    trades.fillna(0.0,inplace=True)
    trades.sort_index(inplace=True)
  #  print(prices)
    for index, row in df_input.iterrows():  
       
        shares = row[sym]
        price = prices.ix[index][sym]
      #  print(shares)
      #  print(index)
        if shares > 0:
           # print('buy')
            shares = abs(shares)
            trades.ix[index][sym] +=  shares
            trades.ix[index]['Cash'] -=  (shares*price*(1+impact) + commission)         
           # print(trades.ix[index])
        elif shares < 0:
            shares = abs(shares)
            trades.ix[index][sym] -=  shares
            trades.ix[index]['Cash'] +=  (shares*price*(1-impact) - commission) 
          #  print(trades.ix[index])
   # print(trades)
    holdings =  trades.copy()
    for i in range(1,len(holdings)):
        holdings.iloc[i] = holdings.iloc[i] + holdings.iloc[i-1] 
 #  print(holdings)
    values = holdings.multiply(prices)
    values.dropna(inplace=True)
    values['Cash'] += start_val
    portvals = values.sum(axis=1)
  #  print(portvals)
  #  rv = pd.DataFrame(index=portvals.index, data=portvals.values)  		   	  			  	 		  		  		    	 		 		   		 		  
  		   	  			  	 		  		  		    	 		 		   		 		  
  #  return rv  		   	  			  	 		  		  		    	 		 		   		 		  
    return portvals  		   	  			  	 		  		  		    	 		 		   		 		  

def author():
    return 'tnguyen497'
      		   	  			  	 		  		  		    	 		 		   		 		  
def test_code():  		   	  			  	 		  		  		    	 		 		   		 		  
    # this is a helper function you can use to test your code  		   	  			  	 		  		  		    	 		 		   		 		  
    # note that during autograding his function will not be called.  		   	  			  	 		  		  		    	 		 		   		 		  
    # Define input parameters  		
    sd=dt.datetime(2008, 1, 2)
    ed=dt.datetime(2009, 1, 31)   	  	

    df_trades = pd.DataFrame(columns=['JPM'],index=pd.date_range(sd, ed))	
    df_trades['JPM'] = 0
    df_trades.iloc[0,0] = 1000
   # print(df_trades)
    result = compute_portvals(df_trades, start_val = 1000000, commission=9.95, impact=0.005)
    print(result)
   # of = "./orders/orders2.csv"  		   	  			  	 		  		  		    	 		 		   		 		  
   # sv = 1000000  		   	  			  	 		  		  		    	 		 		   		 		  

    '''	   	  			  	 		  		  		    	 		 		   		 		  
    # Process orders  		   	  			  	 		  		  		    	 		 		   		 		  
    portvals = compute_portvals(orders_file = of, start_val = sv)  		   	  			  	 		  		  		    	 		 		   		 		  
    if isinstance(portvals, pd.DataFrame):  		   	  			  	 		  		  		    	 		 		   		 		  
        portvals = portvals[portvals.columns[0]] # just get the first column  		   	  			  	 		  		  		    	 		 		   		 		  
    else:  		   	  			  	 		  		  		    	 		 		   		 		  
        "warning, code did not return a DataFrame"  		   	  			  	 		  		  		    	 		 		   		 		  
  		   	  			  	 		  		  		    	 		 		   		 		  
    # Get portfolio stats  		   	  			  	 		  		  		    	 		 		   		 		  
    # Here we just fake the data. you should use your code from previous assignments.  		   	  			  	 		  		  		    	 		 		   		 		  
    start_date = portvals.index.min() #datetime(2008,1,1)  		   	  			  	 		  		  		    	 		 		   		 		  
    end_date = portvals.index.max() #dt.datetime(2008,6,1)  		   	  			  	 		  		  		    	 		 		   		 		  
    cum_ret, avg_daily_ret, std_daily_ret, sharpe_ratio = [0.2,0.01,0.02,1.5]  		   	  			  	 		  		  		    	 		 		   		 		  
    cum_ret_SPY, avg_daily_ret_SPY, std_daily_ret_SPY, sharpe_ratio_SPY = [0.2,0.01,0.02,1.5]  		   	  			  	 		  		  		    	 		 		   		 		  

    # FUND SHARPE RATIO
  #  df = portvals/portvals.iloc[0]	
    df = (portvals/portvals.shift(1))  - 1 # find daily returns
    df = df.iloc[1:] # remove first row
    df_mean = df.mean()
    df_std = df.std()
    sharpe_ratio = np.sqrt(252)*df_mean/df_std

    # FUND CUMMULATIVE RETURN
    cum_ret = portvals[-1]/portvals[0] - 1


    # STD OF FUND
    daily_returns = (portvals/portvals.shift(1))  - 1
    daily_returns = daily_returns[1:]
    std_daily_ret = daily_returns.std()
    avg_daily_ret = daily_returns.mean()

    # Compare portfolio against $SPX  		   	  			  	 		  		  		    	 		 		   		 		  
    print(f"Date Range: {start_date} to {end_date}")  		   	  			  	 		  		  		    	 		 		   		 		  
    print()  		   	  			  	 		  		  		    	 		 		   		 		  
    print(f"Sharpe Ratio of Fund: {sharpe_ratio}")  		   	  			  	 		  		  		    	 		 		   		 		  
    print(f"Sharpe Ratio of SPY : {sharpe_ratio_SPY}")  		   	  			  	 		  		  		    	 		 		   		 		  
    print()  		   	  			  	 		  		  		    	 		 		   		 		  
    print(f"Cumulative Return of Fund: {cum_ret}")  		   	  			  	 		  		  		    	 		 		   		 		  
    print(f"Cumulative Return of SPY : {cum_ret_SPY}")  		   	  			  	 		  		  		    	 		 		   		 		  
    print()  		   	  			  	 		  		  		    	 		 		   		 		  
    print(f"Standard Deviation of Fund: {std_daily_ret}")  		   	  			  	 		  		  		    	 		 		   		 		  
    print(f"Standard Deviation of SPY : {std_daily_ret_SPY}")  		   	  			  	 		  		  		    	 		 		   		 		  
    print()  		   	  			  	 		  		  		    	 		 		   		 		  
    print(f"Average Daily Return of Fund: {avg_daily_ret}")  		   	  			  	 		  		  		    	 		 		   		 		  
    print(f"Average Daily Return of SPY : {avg_daily_ret_SPY}")  		   	  			  	 		  		  		    	 		 		   		 		  
    print()  		   	  			  	 		  		  		    	 		 		   		 		  
    print(f"Final Portfolio Value: {portvals[-1]}")  		   	  			  	 		  		  		    	 		 		   		 		  
  	'''   	  			  	 		  		  		    	 		 		   		 		  
if __name__ == "__main__":  		   	  			  	 		  		  		    	 		 		   		 		  
    test_code()  		   	  			  	 		  		  		    	 		 		   		 		  
