'''
Created on 8 Sep 2016

@author: sennikta
'''

# Implementation of Mann-Kendall Test For Monotonic Trend

import numpy as np  
from scipy.stats import norm, mstats
import os
from os import listdir

base_dir = os.path.dirname(os.path.dirname(__file__))
data_dir = os.path.join(base_dir, 'data')
seed_dir = os.path.join(data_dir, 'seed')
baseline_dir = os.path.join(data_dir, 'baseline')
general_dir = os.path.join(data_dir, 'general')

# Change address for each dataset: views, edits, google_trends
dir = os.path.join(data_dir, 'edits_normed_by_main_page')
#views_baseline_dir = os.path.join(views_dir, 'baseline')
#views_seed_dir = os.path.join(views_dir, 'seed')
dir_seed = os.path.join(dir, 'seed')
scientist_dir = os.path.join(dir_seed, 'topics')
scientist_cut_dir = os.path.join(dir_seed, 'topics_after_creation')

scientists_file = os.path.join(general_dir, 'seed_topics_list.txt')

def running_mean(x, N):
    
    cumsum = np.cumsum(np.insert(x, 0, 0)) 
    return (cumsum[N:] - cumsum[:-N]) / N 

def read_ts (dir):
    ts_dict = {}
    files_list = listdir(dir)
#    with open(scientists_file) as f:
#        name_list = f.read().splitlines()
#        for filename in name_list:
    for filename in files_list:
        name = filename
#            filename = filename + '.txt'
#            if filename in files_list:
        ts_list = []
        temp_list = []
        try:
            with open(dir+'\\'+filename) as f:
                temp_list = f.read().split(',')
            temp_list = list(temp_list)
            if temp_list!=['']:
                temp_list = map(float, temp_list)
        except IOError:
            print "IOError ", filename
            continue
        if temp_list!=[]:
            ts_dict.update({name:temp_list})
        else: 
            print "empty: ", filename
    #else:
    #    print filename
    return ts_dict

def mk_test(x, alpha = 0.05):  
    """   
    Input:
        x:   a vector of data
        alpha: significance level (0.05 default)

    Output:
        trend: tells the trend (increasing, decreasing or no trend)
        h: True (if trend is present) or False (if trend is absence)
        p: p value of the significance test
        z: normalized test statistics 
    """
    
    n = len(x)

    #  Determine the sign of allpossible differences
    # S - the number of positive differences minus the number of negative differences
    s = 0

    for k in range(n-1):
        for j in range(k+1,n):
            s += np.sign(x[j] - x[k])

    # calculate the unique data
    unique_x = np.unique(x)
    g = len(unique_x)

    # calculate the var(s)
    if n == g: # there is no tie
        var_s = (n*(n-1)*(2*n+5))/18
    else: # there are some ties in data
        tp = np.zeros(unique_x.shape)
        for i in range(len(unique_x)):
            tp[i] = sum(unique_x[i] == x)
        var_s = (n*(n-1)*(2*n+5) + np.sum(tp*(tp-1)*(2*tp+5)))/18

    if s>0:
        z = (s - 1)/np.sqrt(var_s)
    elif s == 0:
            z = 0
    elif s<0:
        z = (s + 1)/np.sqrt(var_s)

    # calculate the p_value
    p = 2*(1-norm.cdf(abs(z))) # two tail test
    h = abs(z) > norm.ppf(1-alpha/2) 

    if (z<0) and h:
        trend = 'decreasing'
    elif (z>0) and h:
        trend = 'increasing'
    else:
        trend = 'no trend'

    return trend, h, p, z

x = [1,2,3,4,5,6,7,8,9,10]
trend,h,p,z = mk_test(x,0.05) 
print trend

decreasing_trend = 0
increasing_trend = 0
stable_trend = 0

ts_dict=read_ts(scientist_cut_dir)
count = 0
for name, ts in ts_dict.iteritems():
    print count
    count += 1
    #rm=running_mean(ts_dict[name],90)
    trend,h,p,z = mk_test(ts_dict[name], 0.05)
    if trend == 'decreasing':
        decreasing_trend +=1
    if trend == 'increasing':
        increasing_trend +=1
    if trend == 'no trend':
        stable_trend +=1

print len(ts_dict)
print "decreasing ", decreasing_trend
print "increasing ", increasing_trend
print "stable ", stable_trend