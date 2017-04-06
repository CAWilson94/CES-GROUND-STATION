#!/usr/bin/env python3

class MOT:
    """
    	Inteface / Abstract Class for all schedulers to implement. 

    	Each scheduler must implement the *find() method with the same inputs and outputs, 
    	so that the scheduler can be easily switched out for another one. 

    	Inputs: 
		missions   : a list of Mission models for which for which future passes need to be scheduled

		Outputs:
		passes[] : a list of NextPass models, which are in order of riseTime, and not conflicting.

    """

    def find(self, missions):
        # explicitly set it up so this can't be called directly
        raise NotImplementedError('Exception raised, MOT is supposed to be an interface class!')
