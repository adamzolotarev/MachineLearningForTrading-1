import pandas as pd  		  	 		  		  		    	 		 		   		 		  
import matplotlib.pyplot as plt  		   	  			  	 		  		  		    	 		 		   		 		  
import numpy as np  		   	  			  	 		  		  		    	 		 		   		 		  
import datetime as dt  		   	  			  	 		  		  		    	 		 		   		 		  
from util import get_data, plot_data  	
from marketsimcode import compute_portvals
from indicators import get_sma_r, get_bbp, get_momentum

class ManualStrategyClass(object):
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

        lookback = 7
        momentum = get_momentum(prices, lookback=lookback)
        sma_r = get_sma_r(prices, lookback=lookback)
        bbp = get_bbp(prices,lookback=lookback)

        commission = 9.95
        impact = 0.005
        holding = 0
        cash = sv
       
        #print(bbp)
        df_trades = prices.copy()
        df_trades[symbol] = 0

        for i in range(lookback - 1,prices.shape[0]-1):  
            price = prices.iloc[i,0]
            # BUY
            if (bbp.iloc[i,0] <= 0.6 and sma_r.iloc[i,0] < 1) or \
                (sma_r.iloc[i,0] < 1 and momentum.iloc[i,0] > 0.1) or \
                (bbp.iloc[i,0] <= 0.6 and momentum.iloc[i,0] > 0.1):
                price = price*(1+impact)

                if holding == 0:
                    cash = cash - price*1000 - commission
                    holding = 1000
                    df_trades.iloc[i,0] = 1000
                elif holding == -1000:
                    cash = cash - price*2000 - commission 
                    holding = 1000 
                    df_trades.iloc[i,0] = 2000
                else:
                    pass

            # SELL
            elif (bbp.iloc[i,0] >= 0.8 and sma_r.iloc[i,0] > 1) or \
                (sma_r.iloc[i,0] > 1 and momentum.iloc[i,0] < 0) or \
                (bbp.iloc[i,0] >= 0.8 and momentum.iloc[i,0] < 0):
                price = price*(1-impact)

                if holding == 0:
                    cash = cash + price*1000 - commission
                    holding = -1000
                    df_trades.iloc[i,0] = -1000
                elif holding == 1000:
                    cash = cash + price*2000 - commission 
                    holding = -1000 
                    df_trades.iloc[i,0] = -2000
                else:
                    pass
            else:
                pass

        return df_trades

    def author():
        return 'tnguyen497'

if __name__ == "__main__":  	
    
    for i in [1,2]:	   	  			  	 		  		  		    	 		 		   		 		  
        ms = ManualStrategyClass() 	
        if i == 1:
            print("In-sample performance")
            run_name = 'In-sample'
            df_trades = ms.testPolicy(symbol = "JPM", sd=dt.datetime(2008, 1, 1), ed=dt.datetime(2009, 12, 31), sv=100000)
        elif i == 2:
            print("Out-sample performance")
            run_name = 'Out-sample'
            df_trades = ms.testPolicy(symbol = "JPM", sd=dt.datetime(2010, 1, 1), ed=dt.datetime(2011, 12, 31), sv=100000)

        optimal_portvals = compute_portvals(df_trades, start_val = 100000, commission=0.0, impact=0.0)
        
        # Get vertical lines
        short_points = df_trades[df_trades < 0]
        short_points = short_points.index.tolist()
       # print(short_points)

        df_trades_bm = df_trades.copy()
        df_trades_bm.iloc[:] = 0
        df_trades_bm.iloc[0] = 1000
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

        plt.figure(i)
        plt.plot(optimal_portvals_norm,color="red")
        plt.plot(bm_portvals_norm,color="green")
        for i in range(0,df_trades.shape[0]):
            if df_trades.iloc[i,0] < 0: # SHORT
                plt.axvline(df_trades.iloc[i].name, color='black')
            elif df_trades.iloc[i,0] > 0:
                plt.axvline(df_trades.iloc[i].name, color='blue')
        plt.xlabel("Date")
        plt.xticks(rotation=30)
        plt.ylabel("Normalized porfolio value")
        plt.title(run_name + " normalized rule-based manual vs benchmark porfolio")
        plt.legend(["Manual Strategy Porfolio", "Benchmark porfolio"])
        print("")
        print("Cummulative return benchmark: ", bm_cum_return)
        print("Cummulative return manual: ", op_cum_return)
        print("Std benchmark: ", bm_std)
        print("Std manual: ", opt_std)
        print("Mean benchmark: ", bm_mean)
        print("Mean manual: ", opt_mean)
        print("")
        plt.savefig( run_name + ".png")

    
