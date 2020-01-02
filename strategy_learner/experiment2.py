"""
Student Name: Tri Nguyen (replace with your name)  		   	  			  	 		  		  		    	 		 		   		 		  
GT User ID: tnguyen497 (replace with your User ID)  		   	  			  	 		  		  		    	 		 		   		 		  
GT ID: 903456497 (replace with your GT ID)  		   	  			  	 		  		  		    	 		 		   		 		  
"""  

import pandas as pd  		   	  			  	 		  		  		    	 		 		   		 		  
import matplotlib.pyplot as plt  		   	  			  	 		  		  		    	 		 		   		 		  
import numpy as np  
import StrategyLearner as sl
import ManualStrategy as ms
import datetime as dt  		   	  			  	 		  		  		    	 		 		   		 		  		   	  			  	 		  		  		    	 		 		   		 		    
from marketsimcode import compute_portvals 		  	 		  		  		    	 		 		   		 		  		   	  			  	 		  		  		    	 		 		   		 		     	  			  	 		  		  		    	 		 		   		 		  
from util import get_data, plot_data

def main():

    # NO IMPACT
    strategy_learner = sl.StrategyLearner(verbose = False, impact = 0.00)
    strategy_learner.addEvidence(symbol='JPM', 
            sd=dt.datetime(2008,1,1), 
            ed=dt.datetime(2009,12,31),
            sv = 100000)
    df_trades = strategy_learner.testPolicy(symbol='JPM', 
            sd=dt.datetime(2008,1,1),
            ed=dt.datetime(2009,12,31),
            sv = 100000)
    sl_portvals = compute_portvals(df_trades, start_val = 100000, commission=0.0, impact=0.00)

    # WITH SMALL IMPACT
    strategy_learner = sl.StrategyLearner(verbose = False, impact = 0.0005)
    strategy_learner.addEvidence(symbol='JPM', 
            sd=dt.datetime(2008,1,1), 
            ed=dt.datetime(2009,12,31),
            sv = 100000)
    df_trades_wi = strategy_learner.testPolicy(symbol='JPM', 
            sd=dt.datetime(2008,1,1),
            ed=dt.datetime(2009,12,31),
            sv = 100000)
    wi_portvals = compute_portvals(df_trades_wi, start_val = 100000, commission=0.0, impact=0.0005)

    # WITH LARGE IMPACT
    strategy_learner = sl.StrategyLearner(verbose = False, impact = 0.01)
    strategy_learner.addEvidence(symbol='JPM', 
            sd=dt.datetime(2008,1,1), 
            ed=dt.datetime(2009,12,31),
            sv = 100000)
    df_trades_wi_large = strategy_learner.testPolicy(symbol='JPM', 
            sd=dt.datetime(2008,1,1),
            ed=dt.datetime(2009,12,31),
            sv = 100000)
    wilarge_portvals = compute_portvals(df_trades_wi_large, start_val = 100000, commission=0.0, impact=0.01)

    # Cummulative returns
    sl_cum_return = sl_portvals[-1]/sl_portvals[0] - 1
    wi_cum_return = wi_portvals[-1]/wi_portvals[0] - 1
    wilarge_cum_return = wilarge_portvals[-1]/wilarge_portvals[0] - 1

    # daily returns
    sl_daily_returns = sl_portvals/sl_portvals.shift(1) - 1
    sl_daily_returns = sl_daily_returns[1:]

    wi_daily_returns = wi_portvals/wi_portvals.shift(1) - 1
    wi_daily_returns = wi_daily_returns[1:]

    wilarge_daily_returns = wilarge_portvals/wilarge_portvals.shift(1) - 1
    wilarge_daily_returns = wilarge_daily_returns[1:]

    # normalized returns
    sl_portvals_norm = sl_portvals/sl_portvals[0] - 1
    wi_portvals_norm = wi_portvals/wi_portvals[0] - 1
    wilarge_portvals_norm = wilarge_portvals/wilarge_portvals[0] - 1

    # std daily return
    sl_std = sl_daily_returns.std()
    wi_std = wi_daily_returns.std()
    wilarge_std = wilarge_daily_returns.std()

    # mean daily return
    sl_mean = sl_daily_returns.mean()
    wi_mean = wi_daily_returns.mean()
    wilarge_mean = wilarge_daily_returns.mean()

    plt.figure(1)
    plt.plot(sl_portvals_norm,color="blue")
    plt.plot(wi_portvals_norm,color="green")
    plt.plot(wilarge_portvals_norm,color="red")

    plt.xlabel("Date")
    plt.xticks(rotation=30)
    plt.ylabel("Normalized porfolio value")
    plt.title("Experiment 2: Changing impact value")
    plt.legend(["Impact = 0", "Impact = 0.0005", "Impact = 0.01"])
    print("")
    print("Cummulative return impact = 0.0: ", sl_cum_return)
    print("Cummulative return impact = 0.0005: ", wi_cum_return)
    print("Cummulative return impact = 0.01: ", wilarge_cum_return)
    print("Std impact = 0.0: ", sl_std)
    print("Std impact = 0.0005: ", wi_std)
    print("Std impact = 0.01: ", wilarge_std)
    print("Mean impact = 0.0: ", sl_mean)
    print("Mean impact = 0.0005: ", wi_mean)
    print("Mean impact = 0.01: ", wilarge_mean)
    print("")
    
    print("Trading events impact = 0.00: ", (df_trades!=0).sum()[0] )
    print("Trading events impact = 0.0005: ", (df_trades_wi!=0).sum()[0] )
    print("Trading events impact = 0.01: ", (df_trades_wi_large!=0).sum()[0] )
    plt.savefig("Experiment2.png")
  #  plt.savefig( run_name + ".png")

   # plt.figure(2)
   # plt.plot(df_trades[0:50],color='blue')
   # plt.plot(df_trades_wi[0:50],color='green')
   # plt.plot(df_trades_wi_large[0:50],color='red')
   # plt.show()

def author():
    return 'tnguyen497'

if __name__ == '__main__':
    main()