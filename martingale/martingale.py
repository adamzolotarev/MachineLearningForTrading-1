"""Assess a betting strategy.  		   	  			  	 		  		  		    	 		 		   		 		  
  		   	  			  	 		  		  		    	 		 		   		 		  
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
import pandas as pd  		
import matplotlib.pyplot as plt   	  			  	 		  		  		    	 		 		   		 		  
def author():  		   	  			  	 		  		  		    	 		 		   		 		  
        return 'tnguyen497' # replace tb34 with your Georgia Tech username.  		   	  			  	 		  		  		    	 		 		   		 		  
  		   	  			  	 		  		  		    	 		 		   		 		  
def gtid():  		   	  			  	 		  		  		    	 		 		   		 		  
	return 903456497 # replace with your GT ID number  		   	  			  	 		  		  		    	 		 		   		 		  
  		   	  			  	 		  		  		    	 		 		   		 		  
def get_spin_result(win_prob):  		   	  			  	 		  		  		    	 		 		   		 		  
	result = False  		   	  			  	 		  		  		    	 		 		   		 		  
	if np.random.random() <= win_prob:  		   	  			  	 		  		  		    	 		 		   		 		  
		result = True  		   	  			  	 		  		  		    	 		 		   		 		  
	return result  		   	  			  	 		  		  		    	 		 		   		 		  

def run_simulation(max_bet=1000):
	win_prob = 0.474
	bet_record = np.full([max_bet,1],np.nan)
	bet_record[0,0] = 0 #starting winnings 	   	  			  	 		  		  		    	 		 		   		 		  
	episode_winnings = 0
	bet_amount = 1
	i = 1
	while episode_winnings < 80:
		if get_spin_result(win_prob):
			episode_winnings += bet_amount
			bet_amount = 1
		else:
			episode_winnings -= bet_amount
			bet_amount *= 2
		bet_record[i,0] = episode_winnings
		i += 1
		if i == max_bet:
			break
	if i < max_bet:
		bet_record[i:,0] = episode_winnings
	return bet_record	

def run_real_simulation(max_bet=1000):
	win_prob = 0.474
	i = 1
	bank_roll = 256
	bet_record = np.full([max_bet,1],np.nan)	
	bet_record[0,0] = 0 #starting winnings  	  			  	 		  		  		    	 		 		   		 		  
	episode_winnings = 0
	bet_amount = 1
	while episode_winnings < 80:
		if get_spin_result(win_prob):
			episode_winnings += bet_amount
			bet_amount = 1
		else:
			episode_winnings -= bet_amount
			bet_amount *= 2
		bet_record[i,0] = episode_winnings
		i += 1
		if i == max_bet:
			break
		if episode_winnings <= -bank_roll:
			break

		# if will go below allowed bankroll, adjust bet amount
		if (episode_winnings - bet_amount) < -bank_roll:
				bet_amount = episode_winnings + bank_roll

	if i < max_bet:
		bet_record[i:,0] = episode_winnings
	return bet_record	

def test_code():  		   	  			  	 		  		  		    	 		 		   		 		  
	win_prob = 0.474 # set appropriately to the probability of a win  		   	  			  	 		  		  		    	 		 		   		 		  
	np.random.seed(gtid()) # do this only once  		   	  			  	 		  		  		    	 		 		   		 		  
	print(get_spin_result(win_prob)) # test the roulette spin  		   	  			  	 		  		  		    	 		 		   		 		  
  		   	  			  	 		  		  		    	 		 		   		 		  
	# add your code here to implement the experiments  


# EXPERIMENT 1
	# Figure 1 10 runs
	bet_runs = run_simulation()
	for i in range(0,10): #run 9 simulations
		winnings = run_simulation()
		bet_runs = np.hstack([bet_runs, winnings])

	plt.figure(1)
	plt.plot(bet_runs)
	plt.ylim(-256,100)
	plt.xlim(0,300)
	plt.ylabel('winning $')
	plt.xlabel('bet')
	plt.title('Figure 1: 10 runs')
	plt.savefig('Figure 1')
	#plt.show()
	plt.close()

	#print ("figure 2")
	#Figure 2 1k runs
	bet_runs = run_simulation()
	for i in range(0,1000): #run 999 simulations
		winnings = run_simulation()
		bet_runs = np.hstack([bet_runs, winnings])
	
	mean_winnings = bet_runs.mean(axis=1)
	#print(bet_runs)
	std_winnings = bet_runs.std(axis=1)
	std_winnings_high = mean_winnings + std_winnings
	std_winnings_low = mean_winnings - std_winnings
	#print(mean_winnings.shape)
	plt.figure(2)
	plt.plot(std_winnings_low)
	plt.plot(std_winnings_high)
	plt.plot(mean_winnings)
#	plt.axhline(y=std_winnings_high, color='b', linestyle='-')
#	plt.axhline(y=std_winnings_low, color='r', linestyle='-')
	plt.ylim(-256,100)
	plt.xlim(0,300)
	plt.ylabel('winning $')
	plt.xlabel('bet')
	plt.title('Figure 2: Mean winnings and std. deviation')
	plt.legend(['Mean winnings - std. deviation', 'Mean winnings + std. deviation', 'Mean winnings'])
	plt.savefig('Figure 2')
	#plt.show()
	#plt.show()
	plt.close()

	# Figure 3: 1k runs and median
	median_winnings = np.median(bet_runs,axis=1)
	std_winnings_high = median_winnings + std_winnings
	std_winnings_low = median_winnings - std_winnings
	
	plt.figure(3)
	plt.plot(std_winnings_low)
	plt.plot(std_winnings_high)
	plt.plot(median_winnings)
	#plt.axhline(y=std_winnings_high, color='b', linestyle='-')
	#plt.axhline(y=std_winnings_low, color='r', linestyle='-')
	plt.ylim(-256,100)
	plt.xlim(0,300)
	plt.ylabel('winning $')
	plt.xlabel('bet')
	plt.title('Figure 3: Median winnings and std. deviation')
	plt.legend(['Median winnings - std. deviation', 'Median winnings + std. deviation', 'Median winnings'])
	plt.savefig('Figure 3')
	plt.close()
	#plt.show()
	# 	

	# EXPERIMENT 2
	# Realistic runs
	#Figure 2 10k runs
	bet_runs = run_real_simulation()
	for i in range(0,1000): #run 999 simulations
		winnings = run_real_simulation()
		bet_runs = np.hstack([bet_runs, winnings])
	
	mean_winnings = bet_runs.mean(axis=1)
	std_winnings = bet_runs.std(axis=1)
	std_winnings_high = mean_winnings + std_winnings
	std_winnings_low = mean_winnings - std_winnings
	#print(mean_winnings.shape)
	plt.figure(5)
	plt.plot(std_winnings_low)
	plt.plot(std_winnings_high)
	plt.plot(mean_winnings)
	plt.ylim(-256,100)
	plt.xlim(0,300)
	plt.ylabel('winning $')
	plt.xlabel('bet')
	plt.title('Figure 4: Mean winnings realistic and std. deviation')
	plt.legend(['Mean winnings - std. deviation', 'Mean winnings + std. deviation', 'Mean winnings'])
	plt.savefig('Figure 4')
	plt.close()
	#plt.show()


	# Figure 5: 10k runs and median
	median_winnings = np.median(bet_runs,axis=1)
	std_winnings_high = median_winnings + std_winnings
	std_winnings_low = median_winnings - std_winnings
	plt.figure(5)
	plt.plot(std_winnings_low)
	plt.plot(std_winnings_high)
	plt.plot(median_winnings)
	plt.ylim(-256,100)
	plt.xlim(0,300)
	plt.ylabel('winning $')
	plt.xlabel('bet')
	plt.title('Figure 5: Median winnings realistic and std. deviation')
	plt.legend(['Median winnings - std. deviation', 'Median winnings + std. deviation', 'Median winnings'])
	plt.savefig('Figure 5')
	plt.close()
	#print(median_winnings)
	#plt.show()
	last_run = bet_runs[-1,:]
	#print(last_run)
	win_count = (last_run == 80).sum()
	print(win_count)
	print(win_count/1000)
	print("Expected value: ", last_run.mean())

if __name__ == "__main__":  		   	  			  	 		  		  		    	 		 		   		 		  
    test_code()  		   	  			  	 		  		  		    	 		 		   		 		  
