# -*- coding: utf-8 -*-
"""
Created on Wed Oct 28 23:58:19 2015

@author: frankanayet
"""

import random
import numpy as np
from scipy import spatial as sp

def RandomMove(tourist):
    """
    simulates one random steps in either of four directions.
    tourist is a 2d array with coordinates of tourist
    returns a new toursit position.
    """
    steps = np.array([[0,1],[0,-1],[1,0],[-1,0]])
    stp_tmp = random.choice(steps)
    tourist = tourist + stp_tmp
    return tourist
    
def TouristSim(tourist,nSteps):
    """
    simulates the path of a single tourist
    tourist is a 2d array with coordinates of a tourist
    nSteps is integer number of steps taken by the tourist
    returns final tourist position
    """
    for s in range(nSteps):
        tourist = RandomMove(tourist)
    return tourist


def FullSim(nSteps,nSims,min_dist):
    """
    simulates a full experiment to determine probabilities
    nSteps is integer number of steps taken by the tourist
    nSims is integer number of simulations
    min_dist is minimum distance from the question
    returns probability that tourist is further than min_dist
    """
    ctr = 0    
    for sim in range(nSims):
        tourist = np.zeros([1,2])
        tourist_end = TouristSim(tourist,nSteps)
        if sp.distance.euclidean(origin,tourist_end) >= min_dist:
            ctr += 1
    prob = ctr/float(nSims)
    return prob

def FullSimEver(nSteps,nSims,min_dist):
    """
    simulates a full experiment to determine probabilities 
    of crossing minimum distance min_dist at some point
    tourist is a 2d array with coordinates of a tourist
    nSteps is integer number of steps taken by the tourist
    nSims is integer number of simulations
    min_dist is minimum distance from the question
    returns probability that tourist is further than min_dist
    and average steps to reach min_dist
    """
    ctr = 0 
    avg_steps = 0
    nSimsCorrection = 0
    for sim in range(nSims):
        tourist = np.zeros([1,2])
        test =  0
        steps = 0
        tmp_steps = 0
        while test == 0:
            tourist = RandomMove(tourist)
            if sp.distance.euclidean(origin,tourist) >= min_dist:
                ctr += 1
                tmp_steps = steps + 1
                test = 1
            if steps >= nSteps-1:
                test = 1
            steps += 1
        avg_steps = avg_steps + tmp_steps
        if tmp_steps == 0:
            nSimsCorrection += 1
    prob = ctr/float(nSims)
    avg_steps = avg_steps/float(nSims-nSimsCorrection)
    return prob, avg_steps

def FullSimEastWest(nSteps,east_dist, west_dist,nSims):
    """
    simulates a full experiment to determine probabilities 
    of being east of east_dist and then end west of west_dist
    tourist is a 2d array with coordinates of a tourist
    nSteps is integer number of steps taken by the tourist
    nSims is integer number of simulations
    returns probability that tourist was east of 1st and ends west of 1st
    """
    ctr = 0 
    for sim in range(nSims):
        tourist = np.zeros([1,2])
        east = 0
        west = 0
        for s in range(nSteps):
            tourist = RandomMove(tourist)
            if tourist[0,0] >= east_dist:
                east = 1
        if tourist[0,1] <= west_dist:
            west = 1
        if east == 1 and west == 1:
            ctr += 1
    prob = ctr/float(nSims)
    return prob
                
    
    
nSims = 99999
origin = np.zeros([1,2])

quest1 = FullSim(10,nSims,3)
print 'Question 1 is: %.10f' % quest1

quest2 = FullSim(60,nSims,10)
print 'Question 2 is: %.10f' % quest2

quest3, avg3 = FullSimEver(10,nSims,5)
print 'Question 3 is: %.10f' % quest3

quest4, avg4 = FullSimEver(60,nSims,10)
print 'Question 4 is: %.10f' % quest4

quest5 = FullSimEastWest(10,1,-1,nSims)
print 'Question 5 is: %.10f' % quest5

quest6 = FullSimEastWest(30,1,-1,nSims)
print 'Question 6 is: %.10f' % quest6

quest7, avg7 = FullSimEver(100,nSims,10)
print 'Question 7 is: %.10f' % avg7

quest8, avg8 = FullSimEver(1000,nSims,60)
print 'Question 8 is: %.10f' % avg8