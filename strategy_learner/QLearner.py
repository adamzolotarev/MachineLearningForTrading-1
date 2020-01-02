"""  		   	  			  	 		  		  		    	 		 		   		 		  
Template for implementing QLearner  (c) 2015 Tucker Balch  		   	  			  	 		  		  		    	 		 		   		 		  
  		   	  			  	 		  		  		    	 		 		   		 		  
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
  		   	  			  	 		  		  		    	 		 		   		 		  
import numpy as np  		   	  			  	 		  		  		    	 		 		   		 		  
import random as rand  		   	  		
import time	  	 		  		  		    	 		 		   		 		  
  		   	  			  	 		  		  		    	 		 		   		 		  
class QLearner(object):  		   	  			  	 		  		  		    	 		 		   		 		  
  		   	  			  	 		  		  		    	 		 		   		 		  
    def __init__(self, \
        num_states=100, \
        num_actions = 4, \
        alpha = 0.2, \
        gamma = 0.9, \
        rar = 0.5, \
        radr = 0.99, \
        dyna = 0, \
        verbose = False):  		   	  			  	 		  		  		    	 		 		   		 		  
  		   	  			  	 		  		  		    	 		 		   		 		  
        self.verbose = verbose  		   	  			  	 		  		  		    	 		 		   		 		  
        self.num_actions = num_actions  		
        self.num_states = num_states   	  			  	 		  		  		    	 		 		   		 		  
        self.s = 0  		   	  			  	 		  		  		    	 		 		   		 		  
        self.a = 0  	
        self.q = np.zeros([num_states,num_actions])	 
        self.alpha = alpha
        self.gamma = gamma
        self.rar = rar
        self.radr = 0.99
        self.dyna = dyna  	  	

        if dyna > 0:
            self.Tc = np.zeros([num_states,num_states,num_actions])	+ 0.0001
            self.R = np.zeros([num_states,num_actions])

  		   	  			  	 		  		  		    	 		 		   		 		  
    def querysetstate(self, s):  		   	  			  	 		  		  		    	 		 		   		 		  
        """  		   	  			  	 		  		  		    	 		 		   		 		  
        @summary: Update the state without updating the Q-table  		   	  			  	 		  		  		    	 		 		   		 		  
        @param s: The new state  		   	  			  	 		  		  		    	 		 		   		 		  
        @returns: The selected action  		   	  			  	 		  		  		    	 		 		   		 		  
        """  		   	  			  	 		  		  		    	 		 		   		 		  
        self.s = s  
        pos_actions = self.q[s]
        action = np.argmax(pos_actions)	
        if (rand.uniform(0.0, 1.0) <= self.rar) or (pos_actions.sum() == 0):
            action = rand.randint(0, self.num_actions-1)  	
        self.a = action	   	  			  	 		  	
        self.rar = self.rar*self.radr 		  		    	 		 		   		 		  
        if self.verbose: print(f"s = {s}, a = {action}")  		   	  			  	 		  		  		    	 		 		   		 		  
        return action  		   	  			  	 		  		  		    	 		 		   		 		  
  		   	  			  	 		  		  		    	 		 		   		 		  
    def query(self,s_prime,r):  		   	  			  	 		  		  		    	 		 		   		 		  
        """  		   	  			  	 		  		  		    	 		 		   		 		  
        @summary: Update the Q table and return an action  		   	  			  	 		  		  		    	 		 		   		 		  
        @param s_prime: The new state  		   	  			  	 		  		  		    	 		 		   		 		  
        @param r: The ne state  		   	  			  	 		  		  		    	 		 		   		 		  
        @returns: The selected action  		   	  			  	 		  		  		    	 		 		   		 		  
        """  		   	  

        alpha = self.alpha
        gamma = self.gamma
        s = self.s
        a = self.a

       # start_time = time.time()     

        # DYNA STARTS
        # Update Model T, R
        if self.dyna > 0:
            self.Tc[s, s_prime, a] += 1
            self.R[s,a] = (1-alpha)*self.R[s,a] + alpha*r
          
        # Hallucinate
        start_time = time.time()
        for i in range(0,self.dyna):
            s_d = rand.randint(0,self.num_states - 1)
            a_d = rand.randint(0,self.num_actions - 1)
            next_states = self.Tc[s_d,:,a_d]
            if (next_states.sum() == 0.0001*self.num_states):
                continue              
            s_prime_d = np.argmax(next_states)
            r_d = self.R[s_d,a_d]
            pos_actions = self.q[s_prime_d] 
            max_future_reward = pos_actions.max()
            future_reward = alpha*(r_d + gamma*max_future_reward)
            self.q[s_d,a_d] = (1-alpha)*self.q[s_d,a_d] + future_reward
           # self.rar = self.rar*self.radr
           # 
        #lapse = time.time() - start_time
       # print('hallu time ', lapse)
        # DYNA ENDS
        
        pos_actions = self.q[s_prime]        
        max_future_reward = pos_actions.max()
        future_reward = alpha*(r + gamma*max_future_reward)
        self.q[s,a] = (1-alpha)*self.q[s,a] + future_reward

        action = self.querysetstate(s_prime)		   	  			  	 		  		  		    	 		 		   		 		  
        if self.verbose: print(f"s = {s_prime}, a = {action}, r={r}")  		 		  		  		    	 		 		   		 		  
        return action  		   	  			  	 		  		  		    	 		 		   		 		  

    def author(self):
        return 'tnguyen497'
        # v1

if __name__=="__main__":  		   	  			  	 		  		  		    	 		 		   		 		  
    print("Remember Q from Star Trek? Well, this isn't him")  		   	  			  	 		  		  		    	 		 		   		 		  
