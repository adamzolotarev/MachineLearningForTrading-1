import pandas as pd  		  	 		  		  		    	 		 		   		 		  
import matplotlib.pyplot as plt  		   	  			  	 		  		  		    	 		 		   		 		  
import numpy as np  		   	  			  	 		  		  		    	 		 		   		 		  
import datetime as dt  		   	  			  	 		  		  		    	 		 		   		 		  
from util import get_data, plot_data  	
from marketsimcode import compute_portvals

class TheoreticallyOptimalStrategy(object):
    def __init__(self):
        pass

    def testPolicy(self, symbol = "JPM", sd=dt.datetime(2008, 1, 1), ed=dt.datetime(2009, 1, 31), sv=100000):
         # get data
        dates = pd.date_range(sd, ed)  		   	  			  	 		  		  		    	 		 		   		 		  
        prices_all = get_data([symbol], dates)  # automatically adds SPY  		   	  			  	 		  		  		    	 		 		   		 		  
        prices_all.fillna(method ='ffill',inplace=True)  
        prices_all.fillna(method ='bfill',inplace=True) 
        prices = prices_all[[symbol]]
        prices_SPY = prices_all['SPY']

        commission = 0.0
        impact = 0.000
        holding = 0
        cash = sv

        df_trades = prices.copy()
        df_trades[symbol] = 0

        for i in range(0,prices.shape[0]-1):  
            price = prices.iloc[i,0]
            next_price = prices.iloc[i+1,0]
            price_diff = next_price - price

            if price_diff > 0:
                price = price*(1+impact)
                price_diff = next_price - price
                if holding == 0:
                    pot_gain = price_diff*1000 - commission
                    if pot_gain > 0:
                        cash = cash - price*1000 - commission
                        holding = 1000
                        df_trades.iloc[i,0] = 1000
                elif holding == -1000:
                    pot_gain = price_diff*2000 - commission
                    if pot_gain > 0:
                        cash = cash - price*2000 - commission 
                        holding = 1000 
                        df_trades.iloc[i,0] = 2000

            elif price_diff < 0:
                price = price*(1-impact)
                price_diff = price - next_price
                if holding == 0:
                    pot_gain = price_diff*1000 - commission
                    if pot_gain > 0:
                        cash = cash + price*1000 - commission
                        holding = -1000
                        df_trades.iloc[i,0] = -1000
                elif holding == 1000:
                    pot_gain = price_diff*2000 - commission
                    if pot_gain > 0:
                        cash = cash + price*2000 - commission 
                        holding = -1000 
                        df_trades.iloc[i,0] = -2000
        return df_trades

    def author():
        return 'tnguyen497'

if __name__ == "__main__":  		   	  			  	 		  		  		    	 		 		   		 		  
    ms = TheoreticallyOptimalStrategy() 	
    df_trades = ms.testPolicy(symbol = "JPM", sd=dt.datetime(2008, 1, 1), ed=dt.datetime(2009, 12, 31), sv=100000)
    optimal_portvals = compute_portvals(df_trades, start_val = 100000, commission=0.0, impact=0.0)
   
    # Create benchmark data
    df_trades_bm = df_trades.copy()
    df_trades_bm.iloc[:] = 0
    df_trades_bm.iloc[0] = 1000 # buy 1000 at the beginning and hold
    bm_portvals = compute_portvals(df_trades_bm, start_val = 100000, commission=0.0, impact=0.0)

    # Cummulative returns
    bm_cum_return = bm_portvals[-1]/bm_portvals[0] - 1
    op_cum_return = optimal_portvals[-1]/optimal_portvals[0] - 1

    # daily returns
    bm_daily_returns = bm_portvals/bm_portvals.shift(1) - 1
    bm_daily_returns = bm_daily_returns[1:]

    opt_daily_returns = optimal_portvals/optimal_portvals.shift(1) - 1
    opt_daily_returns = opt_daily_returns[1:]

    # normalized returns
    optimal_portvals_norm = optimal_portvals/optimal_portvals[0] - 1
    bm_portvals_norm = bm_portvals/bm_portvals[0] - 1

    # std daily return
    bm_std = bm_daily_returns.std()
    opt_std = opt_daily_returns.std()

    # mean daily return
    bm_mean = bm_daily_returns.mean()
    opt_mean = opt_daily_returns.mean()

    plt.figure(1)
    plt.plot(bm_portvals_norm,color="green")
    plt.plot(optimal_portvals_norm,color="red")
    plt.xlabel("Date")
    plt.xticks(rotation=30)
    plt.ylabel("Normalized porfolio value")
    plt.title("Normalized theoretically optimal vs benchmark porfolio")
    plt.legend(["Benchmark porfolio","Theoretically optimal porfolio"])

    print("Cummulative return benchmark: ", bm_cum_return)
    print("Cummulative return optimal: ", op_cum_return)
    print("Std benchmark: ", bm_std)
    print("Std optimal: ", opt_std)
    print("Mean benchmark: ", bm_mean)
    print("Mean optimal: ", opt_mean)

    plt.savefig("TheoreticallyOptimal.png")
