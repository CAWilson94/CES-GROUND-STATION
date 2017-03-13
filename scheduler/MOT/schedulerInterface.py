#!/usr/bin/env python3

class MOT:
    """ Inteface / Abstract Class concept for readability. """

    def find(self):
        # explicitly set it up so this can't be called directly
        raise NotImplementedError('Exception raised, ImageFinder is supposed to be an interface / abstract class!')
