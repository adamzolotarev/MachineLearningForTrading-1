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
    # Strategy Learner
    strategy_learner = sl.StrategyLearner(verbose = False, impact = 0.005)
    strategy_learner.addEvidence(symbol='JPM', 
            sd=dt.datetime(2008,1,1), 
            ed=dt.datetime(2009,12,31),
            sv = 100000
        )
    df_trades = strategy_learner.testPolicy(symbol='JPM', 
            sd=dt.datetime(2008,1,1),
            ed=dt.datetime(2009,12,31),
            sv = 100000
        )
    sl_portvals = compute_portvals(df_trades, start_val = 100000, commission=0.0, impact=0.005)

    # Manual Learner
    manual_learner = ms.ManualStrategyClass() 
    df_trades = manual_learner.testPolicy(symbol = "JPM", 
            sd=dt.datetime(2008, 1, 1), 
            ed=dt.datetime(2009, 12, 31), 
            sv=100000)
    ms_portvals = compute_portvals(df_trades, start_val = 100000, commission=0.0, impact=0.005)

    # Cummulative returns
    sl_cum_return = sl_portvals[-1]/sl_portvals[0] - 1
    ms_cum_return = ms_portvals[-1]/ms_portvals[0] - 1

    # daily returns
    sl_daily_returns = sl_portvals/sl_portvals.shift(1) - 1
    sl_daily_returns = sl_daily_returns[1:]

    ms_daily_returns = ms_portvals/ms_portvals.shift(1) - 1
    ms_daily_returns = ms_daily_returns[1:]

    # normalized returns
    sl_portvals_norm = sl_portvals/sl_portvals[0] - 1
    ms_portvals_norm = ms_portvals/ms_portvals[0] - 1

    # std daily return
    sl_std = sl_daily_returns.std()
    ms_std = ms_daily_returns.std()


    # mean daily return
    sl_mean = sl_daily_returns.mean()
    ms_mean = ms_daily_returns.mean()

    plt.figure(1)
    plt.plot(sl_portvals_norm,color="blue")
    plt.plot(ms_portvals_norm,color="green")

    plt.xlabel("Date")
    plt.xticks(rotation=30)
    plt.ylabel("Normalized porfolio value")
    plt.title("Experiment 1: Strategy Learner vs Manual Strategy")
    plt.legend(["Strategy Learner porfolio", "Manual Strategy Porfolio"])
    print("")
    print("Cummulative return strategy learner: ", sl_cum_return)
    print("Cummulative return manual strategy: ", ms_cum_return)
    print("Std strategy learner: ", sl_std)
    print("Std manual strategy: ", ms_std)
    print("Mean strategy learner: ", sl_mean)
    print("Mean manual strategy: ", ms_mean)
    print("")
   # plt.show()
    plt.savefig("Experiment1.png")

def author():
    return 'tnguyen497'

if __name__ == '__main__':
    main()