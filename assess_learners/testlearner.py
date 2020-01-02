"""  		   	  			  	 		  		  		    	 		 		   		 		  
Test a learner.  (c) 2015 Tucker Balch  		   	  			  	 		  		  		    	 		 		   		 		  
  		   	  			  	 		  		  		    	 		 		   		 		  
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
"""  		   	  			  	 		  		  		    	 		 		   		 		  
  		   	  			  	 		  		  		    	 		 		   		 		  
import numpy as np  		  
import pandas as pd 	  			  	 		  		  		    	 		 		   		 		  
import math  		   	  			  	 		  		  		    	 		 		   		 		  
import LinRegLearner as lrl  	
import DTLearner as dt	   	
import RTLearner as rt	   
import BagLearner as bl	  			  	 		  		  		    	 		 		   		 		  
import sys
import matplotlib.pyplot as plt
import time	 		   		 		  
  		   	  			  	 		  		  		    	 		 		   		 		  
if __name__=="__main__":		  		    	 		 		   		 		  
    if len(sys.argv) != 2:
        print("Usage: python testlearner.py <filename>")
        sys.exit(1)
    inf = open(sys.argv[1])

    if sys.argv[1] == 'Data/Istanbul.csv':
        data = np.genfromtxt(inf,delimiter=",")
        data = data[1:,1:]
        np.random.seed(100)
        np.random.shuffle(data)
    else:
        data = np.array([list(map(float,s.strip().split(','))) for s in inf.readlines()])  		   	  			  	 		  		  		    	 		 		   		 		  
  		   	  			  	 		  		  		    	 		 		   		 		  
    # compute how much of the data is training and testing  		   	  			  	 		  		  		    	 		 		   		 		  
    train_rows = int(0.6* data.shape[0])  		   	  			  	 		  		  		    	 		 		   		 		  
    test_rows = data.shape[0] - train_rows  		   	  			  	 		  		  		    	 		 		   		 		  
  		   	  			  	 		  		  		    	 		 		   		 		  
    # separate out training and testing data  		   	  			  	 		  		  		    	 		 		   		 		  
    trainX = data[:train_rows,0:-1]  		   	  			  	 		  		  		    	 		 		   		 		  
    trainY = data[:train_rows,-1]  		   	  			  	 		  		  		    	 		 		   		 		  
    testX = data[train_rows:,0:-1]  		   	  			  	 		  		  		    	 		 		   		 		  
    testY = data[train_rows:,-1]  		   	  			  	 		  		  		    	 		 		   		 		  

    '''  	 		  		  		    	 		 		   		 		  
    print(f"{testX.shape}")  		   	  			  	 		  		  		    	 		 		   		 		  
    print(f"{testY.shape}")  		   	  			  	 		  		  		    	 		 		   		 		  
  		   	  			  	 		  		  		    	 		 		   		 		  
    # create a learner and train it  		   	  			  	 		  		  		    	 		 		   		 		  
    learner = lrl.LinRegLearner(verbose = True) # create a LinRegLearner  		   	  			  	 		  		  		    	 		 		   		 		  
    learner.addEvidence(trainX, trainY) # train it  		   	  			  	 		  		  		    	 		 		   		 		  
    print(learner.author())  		   	  			  	 		  		  		    	 		 		   		 		  
  		   	  			  	 		  		  		    	 		 		   		 		  
    # evaluate in sample  		   	  			  	 		  		  		    	 		 		   		 		  
    predY = learner.query(trainX) # get the predictions  		   	  			  	 		  		  		    	 		 		   		 		  
    rmse = math.sqrt(((trainY - predY) ** 2).sum()/trainY.shape[0])  		   	  			  	 		  		  		    	 		 		   		 		  
   # print()  		   	  			  	 		  		  		    	 		 		   		 		  
    print("In sample results")  		   	  			  	 		  		  		    	 		 		   		 		  
    print(f"RMSE: {rmse}")  		   	  			  	 		  		  		    	 		 		   		 		  
    c = np.corrcoef(predY, y=trainY)  		   	  			  	 		  		  		    	 		 		   		 		  
    print(f"corr: {c[0,1]}")  		   	  			  	 		  		  		    	 		 		   		 		  
  		   	  			  	 		  		  		    	 		 		   		 		  
    # evaluate out of sample  		   	  			  	 		  		  		    	 		 		   		 		  
    predY = learner.query(testX) # get the predictions  		   	  			  	 		  		  		    	 		 		   		 		  
    rmse = math.sqrt(((testY - predY) ** 2).sum()/testY.shape[0])  		   	  			  	 		  		  		    	 		 		   		 		  
    print()  		   	  			  	 		  		  		    	 		 		   		 		  
    print("Out of sample results")  		   	  			  	 		  		  		    	 		 		   		 		  
    print(f"RMSE: {rmse}")  		   	  			  	 		  		  		    	 		 		   		 		  
    c = np.corrcoef(predY, y=testY)  		   	  			  	 		  		  		    	 		 		   		 		  
    print(f"corr: {c[0,1]}")  	
    '''

    # Q1 OVERFITTING AND LEAF SIZE WITH DTLEARNER
    leaf_size = [i for i in range(1,50,2)]
    train_error = []
    test_error = []
    for i in leaf_size:
      #  print(i)
        tree = dt.DTLearner(leaf_size=i)
        tree.addEvidence(trainX,trainY)
        train_predY = tree.query(trainX)
        test_predY = tree.query(testX)
        train_RMSE = math.sqrt(((trainY - train_predY) ** 2).sum()/trainY.shape[0])  
        test_RMSE = math.sqrt(((testY - test_predY) ** 2).sum()/testY.shape[0])  
        train_error.append(train_RMSE)
        test_error.append(test_RMSE)
   # print(train_error)
    error_data = pd.DataFrame({'In sample RMSE': train_error, 
                               'Out sample RMSE': test_error
                                }, index = leaf_size)

    error_data.plot()
    plt.title("RMSE for Decision Tree vs leaf size")
    plt.xlabel("Leaf size")
    plt.ylabel("RMSE")
    plt.savefig("Q1")
  #  plt.show()
    
    # Q2 Effect of bagging
    train_error = []
    test_error = []
    for i in leaf_size:
        tree = bl.BagLearner(learner = dt.DTLearner, kwargs={'leaf_size':i}, bags = 10)
        tree.addEvidence(trainX,trainY)
        train_predY = tree.query(trainX)
        test_predY = tree.query(testX)
        train_RMSE = math.sqrt(((trainY - train_predY) ** 2).sum()/trainY.shape[0])  
        test_RMSE = math.sqrt(((testY - test_predY) ** 2).sum()/testY.shape[0])  
        train_error.append(train_RMSE)
        test_error.append(test_RMSE)
    error_data = pd.DataFrame({'In sample RMSE': train_error, 
                               'Out sample RMSE': test_error
                                }, index = leaf_size)

    error_data.plot()
    plt.title("RMSE for Bagging learner vs leaf size")
    plt.xlabel("Leaf size")
    plt.ylabel("RMSE")    
    plt.savefig("Q2")

    
    # Q3: Classic vs Random decision trees	 
    # compare correlation 	 
    leaf_size = [i for i in range(1,50,2)]
    DT_test_error = []
    DT_train_time = []
    DT_query_time = []
    RT_test_error = []
    RT_train_time = []
    RT_query_time = []

    for i in leaf_size:
        # Decision Tree
        tree = dt.DTLearner(leaf_size=i)
        start = time.time()
        tree.addEvidence(trainX,trainY)
        train_lapse = 1000*(time.time() - start)
        start = time.time()
        test_predY = tree.query(testX)
        query_lapse = 1000*(time.time() - start)
        test_abs_err = abs(testY - test_predY).sum()/testY.shape[0]
        DT_test_error.append(test_abs_err)
        DT_train_time.append(train_lapse)
        DT_query_time.append(query_lapse)

        # Random Tree
        tree = rt.RTLearner(leaf_size=i)
        start = time.time()
        tree.addEvidence(trainX,trainY)
        train_lapse = 1000*(time.time() - start)
        start = time.time()
        test_predY = tree.query(testX)
        query_lapse = 1000*(time.time() - start)
        test_abs_err = abs(testY - test_predY).sum()/testY.shape[0]
        RT_test_error.append(test_abs_err)
        RT_train_time.append(train_lapse)
        RT_query_time.append(query_lapse)

    error_data = pd.DataFrame({'Decision Tree mean absolute error': DT_test_error, 
                               'Random Tree mean absolute error': RT_test_error
                                }, index = leaf_size)
 

    error_data.plot()
    plt.title("Mean absolute error for Decision Trees vs Random Trees")
    plt.xlabel("Leaf size")
    plt.ylabel("Mean Absolute Error")   
    plt.savefig("Q3a")


    train_time_data = pd.DataFrame({'Decision Trees training time': DT_train_time, 
                               'Random Trees training time': RT_train_time
                                }, index = leaf_size) 
    train_time_data.plot()
    plt.title("Training time for Decision Trees vs Random Trees")
    plt.xlabel("Leaf size")
    plt.ylabel("Training time (ms)")   
    plt.savefig("Q3b") 


    query_time_data = pd.DataFrame({'Decision Trees training time': DT_query_time, 
                               'Random Trees training time': RT_query_time
                                }, index = leaf_size) 
    query_time_data.plot()
    plt.title("Query time for Decision Trees vs Random Trees")
    plt.xlabel("Leaf size")
    plt.ylabel("Training time (ms)")   
    plt.savefig("Q3c") 
 

		    	 		 		   		 		  
