'''
Created on 2 Aug 2016

@author: sennikta
'''

#TODO solve problem woth map_to_string the same results
#TODO play around with the normalization - each ts separately, or all together

# Input:
#    data              is the raw time series. 
#    N                 is the length of sliding window (use the length of the raw time series
#                      instead if you don't want to have sliding windows)
#    n                 is the number of symbols in the low dimensional approximation of the sub sequence. (Size of the word to produce)
#    alphabet_size     is the number of discrete symbols. 2 <= alphabet_size <= 20, although 
#                      alphabet_size = 2 is a special "useless" case.
# 
# Output:
#    symbolic_data:    matrix of symbolic data (no-repetition).  If consecutive subsequences
#                      have the same string, then only the first occurrence is recorded, with
#                      a pointer to its location stored in "pointers"
#    pointers:         location of the first occurrences of the strings
# 
#  The variable "win_size" is assigned to N/n, this is the number of data points on the raw 
#  time series that will be mapped to a single symbol, and can be imagined as the 
#  "compression rate".
#
# The symbolic data is returned in "symbolic_data", with pointers to the subsequences  

import json
import os
import numpy
import csv
from itertools import islice
import pandas as pd
import datetime
import time

#--------------------------------------------------------------------------------------------------------------------------------------------------------
#---------------- Define directories ---------------------- Define directories ---------------- Define directories --------------------------------------
#--------------------------------------------------------------------------------------------------------------------------------------------------------

base_dir = os.path.dirname(os.path.dirname(__file__))
data_dir = os.path.join(base_dir, 'data')
neighbors_dir = os.path.join(data_dir, 'neighbors')
seed_dir = os.path.join(data_dir, 'seed')
baseline_dir = os.path.join(data_dir, 'baseline')

# seed or baseline
scientists_file =  os.path.join(seed_dir, 'seed_creation_date.json') 

# for topics change seed/baseline
topic_file =  os.path.join(neighbors_dir, 'baseline_neighbors_list_clean_en.json') 

# views, edits or google trends
views_dir = os.path.join(data_dir, 'views')
edits_dir = os.path.join(data_dir, 'edits')
google_trends_dir = os.path.join(data_dir, 'google')

# scientists or topics
views_sci = os.path.join(views_dir, 'scientists')
edits_sci = os.path.join(edits_dir, 'scientists')
gooogle_trends_sci = os.path.join(google_trends_dir, 'scientists')

views_topic = os.path.join(views_dir, 'topics')
edits_topic = os.path.join(edits_dir, 'topics')
gooogle_trends_topic = os.path.join(google_trends_dir, 'topics')

# for output
sax_dir = os.path.join(data_dir, 'sax_representation')
views_sax = os.path.join(sax_dir, 'views')
edits_sax = os.path.join(sax_dir, 'edits')
google_trends_sax = os.path.join(sax_dir, 'google_trends')

# scientists or topics
views_sax_sci = os.path.join(views_sax, 'scientists')
edits_sax_sci = os.path.join(edits_sax, 'scientists')
gooogle_trends_sax_sci = os.path.join(google_trends_sax, 'scientists')

views_sax_topic = os.path.join(views_sax, 'topics')
edits_sax_topic = os.path.join(edits_sax, 'topics')
gooogle_trends_sax_topicc = os.path.join(google_trends_sax, 'topics')

def load_simple_json(filename):
    print filename
    with open(filename, 'r') as f:
        return json.load(f)
    
def map_to_string(PAA, alphabet_size):
    string = numpy.zeros(shape=(1,len(PAA)))
    switcher = {
                2:[0],
                3:[-0.43, 0.43],
                4:[-0.67, 0, 0.67],
                5:[-0.84, -0.25, 0.25, 0.84],
                6:[-0.97, -0.43, 0, 0.43, 0.97],
                7:[-1.07, -0.57, -0.18, 0.18, 0.57, 1.07],
                8:[-1.15, -0.67, -0.32, 0, 0.32, 0.67, 1.15],
                9:[-1.22, -0.76, -0.43, -0.14, 0.14, 0.43, 0.76, 1.22],
                10:[-1.28, -0.84, -0.52, -0.25, 0, 0.25, 0.52, 0.84, 1.28]
                }
    for i in range(0, len(PAA)):
        cut_points = [s for s in switcher.get(alphabet_size) if s<=PAA[i]]
        print cut_points
        string[0][i] = sum(cut_points)
    
    return string

def series_to_sax(data, N, n, alphabet_size):
    if alphabet_size > 20:
        print 'Currently alphabet_size cannot be larger than 20.  Please update the breakpoint table if you wish to do so'
        return
    # win_size is the number of data points on the raw time series that will be mapped to a single symbol
    win_size = int(N/n)      
    symbolic_data = numpy.zeros(shape=(1,n))
    PAA = []
    PAA = numpy.array(PAA)
    # Scan across the time series extract sub sequences, and converting them to strings.
    for i in range (0, (len(data) - N)):
    
        #Remove the current subsection
        sub_section = data[i:i+N]
        
        #Z normalize it
        sub_section = (sub_section - numpy.mean(sub_section))/numpy.std(sub_section)
    
        # take care of the special case where there is no dimensionality reduction
        if N == n:
            PAA = sub_section
       
        # convert to PAA
        else:
            #N is not dividable by n
            if float(N)/n!=round(N/n):
                temp = numpy.zeros(shape=(n,N))
                for j in range(0,n):
                    temp[j,:] = sub_section
                expanded_sub_section = numpy.reshape(temp,(1, N*n))
                PAA = numpy.mean(numpy.reshape(expanded_sub_section, (N, n)), 0)
            # N is dividable by n
            else:                                  
                PAA =numpy.mean(numpy.reshape(sub_section, (win_size,n)), 0)
        current_string = map_to_string(PAA,alphabet_size)
    #print PAA.shape
    return

def get_series_from_txt(scientist, dir):
    scientist_series = []
    scientist = scientist.rstrip().split('/')[-1]
    filename = os.path.join(dir + '\\' + scientist + '.txt')
    try:
        f = open(filename)
        for line in f:
            time_list = map(float, line.split(','))
            year = int(time_list.pop(0))
            if  year>2004 and year<2016:
                scientist_series += time_list 
        f.close()
    except IOError:
        return []
        #    print scientist
    return scientist_series

scientist_dict = load_simple_json(scientists_file)
for scientist in scientist_dict:
    scientist_series = get_series_from_txt(scientist, views_sci)
    series_to_sax(scientist_series, 90, 8, 10)
    break