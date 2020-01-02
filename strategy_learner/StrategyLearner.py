"""  		   	  			  	 		  		  		    	 		 		   		 		  
Template for implementing StrategyLearner  (c) 2016 Tucker Balch  		   	  			  	 		  		  		    	 		 		   		 		  
  		   	  			  	 		  		  		    	 		 		   		 		  
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
  		   	  			  	 		  		  		    	 		 		   		 		  
Student Name: Tri Nguyen (replace with your name)  		   	  			  	 		  		  		    	 		 		   		 		  
GT User ID: tnguyen497 (replace with your User ID)  		   	  			  	 		  		  		    	 		 		   		 		  
GT ID: 903456497 (replace with your GT ID)  		   	  			  	 		  		  		    	 		 		   		 		  
"""  		   	  			  	 		  		  		    	 		 		   		 		  
  		   	  			  	 		  		  		    	 		 		   		 		  
import datetime as dt  		   	  			  	 		  		  		    	 		 		   		 		  
import pandas as pd  		   	  			  	 		  		  		    	 		 		   		 		  
import util as ut  		   	  			  	 		  		  		    	 		 		   		 		  
import random as rand	
import indicators as idc	  
import math	 	
import QLearner as ql	  
import marketsimcode as ms		  		    	 		 		   		 		  
  		   	  			  	 		  		  		    	 		 		   		 		  
class StrategyLearner(object):  		   	  			  	 		  		  		    	 		 		   		 		  
  		   	  			  	 		  		  		    	 		 		   		 		  
    # constructor  		   	  			  	 		  		  		    	 		 		   		 		  
    def __init__(self, verbose = False, impact=0.0):  		   	  			  	 		  		  		    	 		 		   		 		  
        self.verbose = verbose  		   	  			  	 		  		  		    	 		 		   		 		  
        self.impact = impact  	
        self.threshold_mmt = [] # Momentum thresholds
        self.threshold_smar = [] # Simple moving average ratio
        self.threshold_bbp = []	# Bollinger band percentage

        self.learner = ql.QLearner(num_states=1000,\
            num_actions = 3, \
            alpha = 0.2, \
            gamma = 0.9, \
            rar = 0.5, \
            radr = 0.99, \
            dyna = 0, \
            verbose=False)  	  			  	 		  		  		    	 		 		   		 		  

    # Turn the three indicator values into an integer
    def serialize(self,indicators):
        state = 0
        threshold_i = 0
        for i in range(0,len(self.threshold_mmt)):
            if indicators[0] <= self.threshold_mmt[i]:
                state += i*100
                break
        for i in range(0,len(self.threshold_smar)):
            if indicators[1] <= self.threshold_smar[i]:
                state += i*10
                break
        for i in range(0,len(self.threshold_bbp)):
            if indicators[2] <= self.threshold_bbp[i]:
                state += i   
                break          
        return state		  	

    # this method should create a QLearner, and train it for trading  		   	  			  	 		  		  		    	 		 		   		 		  
    def addEvidence(self, symbol = "JPM", \
        sd=dt.datetime(2008,1,1), \
        ed=dt.datetime(2009,12,31), \
        sv = 100000):  		   	  			  	 		  		  		    	 		 		   		 		  
  		   	  			  	 		  		  		    	 		 		   		 		   	  
        rand.seed(5)  		
        LOOKBACK = 10	
        randomrate = 0.0
		  		   	  			  	 		  		  		    	 		 		   		 		  
        # Getting data 		   	  			  	 		  		  		    	 		 		   		 		  
        syms=[symbol]  		   	  			  	 		  		  		    	 		 		   		 		  
        dates = pd.date_range(sd, ed)  		   	  			  	 		  		  		    	 		 		   		 		  
        prices_all = ut.get_data(syms, dates)  # automatically adds SPY  		   	  			  	 		  		  		    	 		 		   		 		  
        prices = prices_all[syms]  # only portfolio symbols 
        prices.fillna(method ='ffill',inplace=True)  
        prices.fillna(method ='bfill',inplace=True)   		   	  			  	 		  		  		    	 		 		   		 		  
        prices_SPY = prices_all['SPY']  # only SPY, for comparison later  		   	  			  	 		  		  		    	 		 		   		 		  	

        # Make indicators df
        X = prices.copy()
        X.drop([symbol],axis=1,inplace=True)   	  	
        X['mmt'] = idc.get_momentum(prices)	
        X['smar'] = idc.get_sma_r(prices)
        X['bbp'] = idc.get_bbp(prices)

        # Get thresholds for 3 indicators
        # Momentum
        sorted_vals = X['mmt'].sort_values()
        sorted_vals = sorted_vals.dropna()
        stepsize = math.floor(sorted_vals.shape[0]/10)
        for i in range(0,10):
            self.threshold_mmt.append(sorted_vals[(i+1)*stepsize])

        # Simple moving average ratio
        sorted_vals = X['smar'].sort_values()
        sorted_vals = sorted_vals.dropna()
        stepsize = math.floor(sorted_vals.shape[0]/10)
        for i in range(0,10):
            self.threshold_smar.append(sorted_vals[(i+1)*stepsize])

        # Bollinger band percentage
        sorted_vals = X['bbp'].sort_values()
        sorted_vals = sorted_vals.dropna()
        stepsize = math.floor(sorted_vals.shape[0]/10)
        for i in range(0,10):
            self.threshold_bbp.append(sorted_vals[(i+1)*stepsize])

        # Get initial state
        indicators = X.iloc[LOOKBACK - 1]
        s = self.serialize(indicators)
        a = self.learner.querysetstate(s)
        df_len = prices.shape[0]

        run_i = 0
        run_results = []
        MAX_RUNS = 50

        while run_i < MAX_RUNS:
            if len(run_results) > 10: # Check for convergence
                if (round(run_results[-1],4) == round(run_results[-2],4)): break
            run_i += 1
            holding = 0
            df_trades = prices.copy()
            df_trades[symbol] = 0

            for i in range(LOOKBACK, df_len - 1):
                s = self.serialize(X.iloc[i])
                price = prices.iloc[i,0]
                next_price = prices.iloc[i+1,0]

                if rand.uniform(0.0, 1.0) <= randomrate: # going rogue  		   	  			  	 		  		  		    	 		 		   		 		  
                    a = rand.randint(0,2) # choose the random direction  	
                
                # Calculate reward
                r = 0
                if a == 2: # LONG
                    if holding == 0:
                        holding = 1000
                        df_trades.iloc[i,0] = 1000
                        r = - self.impact*(price+next_price)*1000
                    elif holding == -1000:
                        holding = 1000 
                        df_trades.iloc[i,0] = 2000
                        r = - self.impact*(price+next_price)*2000
                    else:
                        pass
                
                elif a == 1: # do nothing
                    pass

                elif a == 0: # SHORT
                    if holding == 0:
                        holding = -1000
                        df_trades.iloc[i,0] = -1000
                        r = - self.impact*(price+next_price)*1000

                    elif holding == 1000:
                        holding = -1000 
                        df_trades.iloc[i,0] = -2000
                        r = - self.impact*(price+next_price)*2000
                    else:
                        pass

                else:
                    raise Exception("ERROR: INVALID ACTION")

                r += (next_price - price)*holding
                a = self.learner.query(s,r)

            por_vals = ms.compute_portvals(df_trades, start_val = sv, commission=0.0, impact=self.impact)
            cum_ret = por_vals[-1]/por_vals[0] - 1
            run_results.append(cum_ret)	   	  			  	 		  		  		    	 		 		   		 		  
  		   	  			  	 		  		  		    	 		 		   		 		  
    # this method should use the existing policy and test it against new data  		   	  			  	 		  		  		    	 		 		   		 		  
    def testPolicy(self, symbol = "JPM", \
        sd=dt.datetime(2010,1,1), \
        ed=dt.datetime(2011,12,31), \
        sv = 100000):  	

        rand.seed(5)  	
        LOOKBACK = 10

        # example usage of the old backward compatible util function  		   	  			  	 		  		  		    	 		 		   		 		  
        syms=[symbol]  		   	  			  	 		  		  		    	 		 		   		 		  
        dates = pd.date_range(sd, ed)  		   	  			  	 		  		  		    	 		 		   		 		  
        prices_all = ut.get_data(syms, dates)  # automatically adds SPY  		   	  			  	 		  		  		    	 		 		   		 		  
        prices = prices_all[syms]  # only portfolio symbols  		   	  			  	 		  		  		    	 		 		   		 		  
        prices.fillna(method ='ffill',inplace=True)  
        prices.fillna(method ='bfill',inplace=True) 
        prices_SPY = prices_all['SPY']  # only SPY, for comparison later  		   	  			  	 		  		  		    	 		 		   		 		  
        if self.verbose: print(prices)  	

        # Make indicators df
        X = prices.copy()
        X.drop([symbol],axis=1,inplace=True)   	  	
        X['mmt'] = idc.get_momentum(prices)	
        X['smar'] = idc.get_sma_r(prices)
        X['bbp'] = idc.get_bbp(prices)

        df_trades = prices.copy()
        df_trades[symbol] = 0
        holding = 0

        # Get initial state
        indicators = X.iloc[LOOKBACK - 1]
        s = self.serialize(indicators)
        a = self.learner.querysetstate(s)
        df_len = prices.shape[0]

        for i in range(LOOKBACK, df_len - 1):
            s = self.serialize(X.iloc[i])
            
            if a == 2: # LONG
                if holding == 0:
                        holding = 1000
                        df_trades.iloc[i,0] = 1000       
                elif holding == -1000:   
                    holding = 1000
                    df_trades.iloc[i,0] = 2000
            elif a == 1:
                pass
            elif a == 0: # SHORT
                if holding == 0:
                    holding = -1000
                    df_trades.iloc[i,0] = -1000
                elif holding == 1000:
                    holding = -1000 
                    df_trades.iloc[i,0] = -2000
            else:
                raise Exception("ERROR: INVALID ACTION")
            a = self.learner.querysetstate(s)

       # por_vals = ms.compute_portvals(df_trades, start_val = sv, commission=0.0, impact=self.impact)
       # cum_ret = por_vals[-1]/por_vals[0] - 1
        return df_trades
	   	  			  	 		  		  		    	 		 		   		 		  
        if self.verbose: print(type(trades)) # it better be a DataFrame!  		   	  			  	 		  		  		    	 		 		   		 		  
        if self.verbose: print(trades)  		   	  			  	 		  		  		    	 		 		   		 		  
        if self.verbose: print(prices_all)  		   	  			  	 		  		  		    	 		 		   		 		  

    def author(self):
        return 'tnguyen497'
  		   	  			  	 		  		  		    	 		 		   		 		  
if __name__=="__main__":  		   	  			  	 		  		  		    	 		 		   		 		  
    print("One does not simply think up a strategy")  	 		  		  		    	 		 		   		 		  
