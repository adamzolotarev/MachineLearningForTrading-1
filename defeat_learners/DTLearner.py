import numpy as np  	
import pandas as pd	   	  			  	 		  		  		    	 		 		   		 		  
  		   	  			  	 		  		  		    	 		 		   		 		  
class DTLearner(object):  		   	  			  	 		  		  		    	 		 		   		 		  
  		   	  			  	 		  		  		    	 		 		   		 		  
    def __init__(self, leaf_size = 1, verbose = False):  		   	  			  	 		  		  		    	 		 		   		 		  
        self.leaf_size = leaf_size 

    def author(self):  		   	  			  	 		  		  		    	 		 		   		 		  
        return 'tnguyen497' # replace tb34 with your Georgia Tech username  		   	  			  	 		  		  		    	 		 		   		 		  

    def build_tree(self,X,Y):
        if X.shape[0]==1:
            return np.array([[-1,Y[0],np.nan, np.nan]])
        Y_same_value = np.sum((Y == Y[0]))
        if (Y_same_value == Y.shape[0]):
            return np.array([[-1,Y[0],np.nan, np.nan]])
        if (Y.shape[0] <= self.leaf_size): # or (self.depth >= self.max_depth):
            return np.array([[-1, np.mean(Y), np.nan, np.nan]])

        # Determine best feature based on correlation
        corrs = [abs(np.corrcoef(X[:,i],Y)[0,1]) if np.std(X[:,i]) != 0 else 0 for i in range(X.shape[1]) ]
     #   factor = 0
        factor = np.nanargmax(corrs)
        
        splitVal = np.median(X[:,factor])
        X_left = X[X[:,factor] <= splitVal]
        Y_left = Y[X[:,factor] <= splitVal]

        if X_left.shape[0] == Y.shape[0] or X_left.shape[0] == 0:
            return np.array([[-1,np.mean(Y),np.nan,np.nan]])

        X_right = X[X[:,factor] > splitVal]
        Y_right = Y[X[:,factor] > splitVal]

        left_tree = self.build_tree(X_left,Y_left)

        right_tree = self.build_tree(X_right,Y_right)
        root = [factor,splitVal,1,left_tree.shape[0]+1]
        tree = np.vstack((root,left_tree,right_tree))

        return tree

    def addEvidence(self,dataX,dataY):  		   	  			  	 		  		  		    	 		 		   		 		  
        """  		   	  			  	 		  		  		    	 		 		   		 		  
        @summary: Add training data to learner  		   	  			  	 		  		  		    	 		 		   		 		  
        @param dataX: X values of data to add  		   	  			  	 		  		  		    	 		 		   		 		  
        @param dataY: the Y training values  		   	  			  	 		  		  		    	 		 		   		 		  
        """
        self.DTree = self.build_tree(dataX,dataY)
       # print(self.DTree)
    def make_prediction(self,node_ix,node,x):
        factor = int(node[0])
      #  print("current in ", node_ix)
      #  print("factor ", int(factor))
      #  print("splitval ", node[1])
      #  print("x factor ", x[factor])

        if factor == -1:
            return node[1]
        if x[factor] <= node[1]:
        #    print("left ")
            new_ix = int(node_ix + node[2])
            return self.make_prediction( new_ix,self.DTree[new_ix], x)
        else:
        #    print("right ")
            new_ix = int(node_ix + node[3])
            return self.make_prediction(new_ix, self.DTree[new_ix], x)

    def query(self,points):  		   	  			  	 		  		  		    	 		 		   		 		  
        """  		   	  			  	 		  		  		    	 		 		   		 		  
        @summary: Estimate a set of test points given the model we built.  		   	  			  	 		  		  		    	 		 		   		 		  
        @param points: should be a numpy array with each row corresponding to a specific query.  		   	  			  	 		  		  		    	 		 		   		 		  
        @returns the estimated values according to the saved model.  		   	  			  	 		  		  		    	 		 		   		 		  
        """  		   	
        return np.array([self.make_prediction(0, self.DTree[0], x) for x in points ])

