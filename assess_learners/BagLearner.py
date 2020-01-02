import numpy as np  	
import pandas as pd	   	  	
import DTLearner as dt	  	 		  		  		    	 		 		   		 		  
		   	  			  	 		  		  		    	 		 		   		 		  
class BagLearner(object):  		   	  			  	 		  		  		    	 		 		   		 		  
  		   	  			  	 		  		  		    	 		 		   		 		  
    def __init__(self, learner = dt.DTLearner, kwargs = {}, bags= 20, boost = False, verbose = False):  		   	  			  	 		  		  		    	 		 		   		 		  
        self.custom_args = kwargs
        self.LearnerClass = learner
        self.bag_count = bags
        self.boost = boost
        self.verbose = verbose
        self.Forest = []
	  			  	 		  		  		    	 		 		   		 		  
    def author(self):  		   	  			  	 		  		  		    	 		 		   		 		  
        return 'tnguyen497' # replace tb34 with your Georgia Tech username  		   	  			  	 		  		  		    	 		 		   		 		  

    def addEvidence(self,dataX,dataY):  		   	  			  	 		  		  		    	 		 		   		 		  
        """  		   	  			  	 		  		  		    	 		 		   		 		  
        @summary: Add training data to learner  		   	  			  	 		  		  		    	 		 		   		 		  
        @param dataX: X values of data to add  		   	  			  	 		  		  		    	 		 		   		 		  
        @param dataY: the Y training values  		   	  			  	 		  		  		    	 		 		   		 		  
        """
        bag_size = dataY.shape[0]
        for i in range(self.bag_count):
            a_tree = self.LearnerClass(**self.custom_args)
            rand_ix = np.random.randint(size=bag_size,low=0,high=dataY.shape[0])
            X = dataX[rand_ix]
            Y = dataY[rand_ix]
            a_tree.addEvidence(X,Y)
            self.Forest.append(a_tree)

    def query(self,points):  		   	  			  	 		  		  		    	 		 		   		 		  
        """  		   	  			  	 		  		  		    	 		 		   		 		  
        @summary: Estimate a set of test points given the model we built.  		   	  			  	 		  		  		    	 		 		   		 		  
        @param points: should be a numpy array with each row corresponding to a specific query.  		   	  			  	 		  		  		    	 		 		   		 		  
        @returns the estimated values according to the saved model.  		   	  			  	 		  		  		    	 		 		   		 		  
        """  	
        Y= [tree.query(points) for tree in self.Forest] 
        Y = np.array(Y)
        return np.array((np.mean(Y,axis=0)))	   	
  	  			  	 		  		  		    	 		 		   		 		  
if __name__=="__main__":  		   	  			  	 		  		  		    	 		 		   		 		  
    print("Decision Tree ******")  		   	  			  	 		  		  		    	 		 		   		 		  
    Y = np.array([1,2,3,4,5,6])
    X = np.array([[-0,-2],
                 [5,-4],
                 [4,-6],
                [17,-8],
                [17,-10],
                [8,-12]])

    learner = BagLearner(learner = rt.RTLearner, kwargs ={"leaf_size": 1}, bags= 10, boost = False, verbose = False)
    learner.addEvidence(X,Y)
    X_test = np.array([[0,-2],[5,-4]])
    Y = learner.query(X)
    print(Y)
