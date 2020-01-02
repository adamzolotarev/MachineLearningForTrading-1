	   	  			  	 		  		  		    	 		 		   		 		  
  		   	  			  	 		  		  		    	 		 		   		 		  
import numpy as np  	
import pandas as pd	   	  		  	 		  		  		    	 		 		   		 		  
import DTLearner as dt  

class BoostLearner(object):  		   	  			  	 		  		  		    	 		 		   		 		  
  		   	  			  	 		  		  		    	 		 		   		 		  
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

        bag_size = dataY.shape[0]
        weights = [1.0/bag_size]*bag_size
        ix_range = [i for i in range(0,bag_size)]
        a_tree = self.LearnerClass(**self.custom_args)
        X = dataX
        Y = dataY
        a_tree.addEvidence(X,Y)
        Y_predict = a_tree.query(X)
        Y_error = Y_predict - Y
        Y_error = np.absolute(Y_error)
        weights = Y_error/np.sum(Y_error)
        
        for i in range(self.bag_count):
            a_tree = self.LearnerClass(**self.custom_args)
            rand_ix = np.random.choice(a=ix_range,size = bag_size, replace = True, p= weights)
            X = dataX[rand_ix]
            Y = dataY[rand_ix]
            a_tree.addEvidence(X,Y)
            Y_predict = a_tree.query(X)
            Y_error = Y_predict - Y
           # print(Y_error)
            Y_error = np.absolute(Y_error)
            weights = Y_error/np.sum(Y_error)
            print("error: ", 1000*(np.mean(Y_error)))
            self.Boost = a_tree


       # print(self.DTree)
       # print(dataX) 		   	  			  	 		  		  		    	 		 		   		 		  
  		   	  			  	 		  		  		    	 		 		   		 		  
        # slap on 1s column so linear regression finds a constant term  		   	  			  	 		  		  		    	 		 		   		 		  
      #  newdataX = np.ones([dataX.shape[0],dataX.shape[1]+1])  		   	  			  	 		  		  		    	 		 		   		 		  
       # newdataX[:,0:dataX.shape[1]]=dataX  		   	  			  	 		  		  		    	 		 		   		 		  
  		   	  			  	 		  		  		    	 		 		   		 		  
        # build and save the model  		   	  			  	 		  		  		    	 		 		   		 		  
       # self.model_coefs, residuals, rank, s = np.linalg.lstsq(newdataX, dataY, rcond=None)  		   	  			  	 		  		  		    	 		 		   		 		  

   

    def query(self,points):  		   	  			  	 		  		  		    	 		 		   		 		  
        """  		   	  			  	 		  		  		    	 		 		   		 		  
        @summary: Estimate a set of test points given the model we built.  		   	  			  	 		  		  		    	 		 		   		 		  
        @param points: should be a numpy array with each row corresponding to a specific query.  		   	  			  	 		  		  		    	 		 		   		 		  
        @returns the estimated values according to the saved model.  		   	  			  	 		  		  		    	 		 		   		 		  
        """  	
        #print("aa")
        #print (self.Forest)
        Y= self.Boost.query(points)
        
        Y = np.array(Y)
        #print(Y)
        return Y   	
         #[self.make_prediction(0, self.DTree[0], x) for x in points ]
        #return (self.model_coefs[:-1] * points).sum(axis = 1) + self.model_coefs[-1]  		   	  			  	 		  		  		    	 		 		   		 		  
  		   	  			  	 		  		  		    	 		 		   		 		  
if __name__=="__main__":  		   	  			  	 		  		  		    	 		 		   		 		  
    print("Decision Tree ******")  		   	  			  	 		  		  		    	 		 		   		 		  
    Y = np.array([1,2,3,4,5,6])
    X = np.array([[-0,-2],
                 [5,-4],
                 [4,-6],
                [17,-8],
                [17,-10],
                [8,-12]])

    learner = BoostLearner(learner = dt.DTLearner, kwargs ={"leaf_size": 3}, bags= 1, boost = False, verbose = False)
    learner.addEvidence(X,Y)
    X_test = np.array([[0,-2],[5,-4]])
    Y = learner.query(X)
    print(Y)
