import numpy as np  	 	  	
import LinRegLearner as lrl	
import BagLearner as bl  		  		    	 		 		   		 		  		  	 		  		  		    	 		 		   		 		  
class InsaneLearner(object):  		   	  			  	 		  		  		    	 		 		   		 		   			  	 		  		  		    	 		 		   		 		  
    def __init__(self, verbose = False):  		   	  			  	 		  		  		    	 		 		   		 		  
        self.Learners = []  			  	 		  		  		    	 		 		   		 		  
    def author(self):  		   	  			  	 		  		  		    	 		 		   		 		  
        return 'tnguyen497' # replace tb34 with your Georgia Tech username  		   	  			  	 		  		  		    	 		 		   		 		  
    def addEvidence(self,dataX,dataY):  
        for i in range(20):
            learner = bl.BagLearner(learner = lrl.LinRegLearner, kwargs = {}, bags= 20, boost=False, verbose=False )
            learner.addEvidence(dataX,dataY)
            self.Learners.append(learner)	   	  			  	 		  		  		    	 		 		   		 		  
    def query(self,points):  		  	        		  	 		  		  		    	 		 		   		 		  
        Y= np.array([learner.query(points) for learner in self.Learners])
        return np.array((np.mean(Y,axis=0)))