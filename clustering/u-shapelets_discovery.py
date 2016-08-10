'''
Created on 9 Aug 2016

@author: sennikta
'''

# TODO: continue testing on a small dataset

import os
from os import listdir
import numpy
import json
import random


#--------------------------------------------------------------------------------------------------------------------------------------------------------
#---------------- Define directories ---------------------- Define directories ---------------- Define directories --------------------------------------
#--------------------------------------------------------------------------------------------------------------------------------------------------------

base_dir = os.path.dirname(os.path.dirname(__file__))
data_dir = os.path.join(base_dir, 'data')
neighbors_dir = os.path.join(data_dir, 'neighbors')
seed_dir = os.path.join(data_dir, 'seed')
baseline_dir = os.path.join(data_dir, 'baseline')

# sax representation
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
gooogle_trends_sax_topic = os.path.join(google_trends_sax, 'topics')

# seed or baseline
scientists_file = os.path.join(seed_dir, 'seed_creation_date.json') 
test = os.path.join(sax_dir, 'test')

def load_simple_json(filename):
    print filename
    with open(filename, 'r') as f:
        return json.load(f)


def read_sax (filename):
    ts_list = []
    temp_list = []
    with open(filename) as f:
        temp_list = f.read().splitlines()
    temp_list = list(set(temp_list))
    for word in temp_list: 
        word = list(word.replace(',',''))
        #word = map(int,word)
        ts_list.append(word)
    return ts_list

def random_masking(sax_list):
    print 'in random masking function'
    R = 10
    maskedNum = 3
    candidate_dict = {}
    masked_list = []
    for i in range (0,R):
        stop_list = []
        mask_ind = random.sample(range(0, 8), 3)
        masked_dict = {}
        print 'started random masking'
        
        # apply mask to the list of time series
        for time_series in sax_list:
            masked_time_series = []
            for word in time_series:  
                masked_word = list(word)
                for l in sorted(mask_ind, reverse=True):
                    del masked_word[l]
                masked_word = int(''.join(masked_word))
                masked_time_series.append(masked_word)
            masked_time_series = set(masked_time_series)
            masked_list.append(masked_time_series)
        print 'random mask #', i, '=', mask_ind
        print 'masked time series', masked_time_series
        
        print 'counting frequency'
        for time_series in sax_list:
            for candidate in time_series:
                if  candidate not in stop_list:
                    masked_candidate = list(candidate)
                    sum = 0
                    sum_list = []
                    
                    for l in sorted(mask_ind, reverse=True):
                        del masked_candidate[l]
                    masked_candidate = int(''.join(masked_candidate))
                
                   # Critical point
                    for masked_time_series in masked_list:
                        #masked_time_series=set(masked_time_series)
                        if masked_candidate in masked_time_series:
                            sum+=1
                            print sum
                    
                    candidate_dict.update({str(candidate):sum_list.append(sum)})
                    
                    stop_list.append(candidate)
        print 'candidate dir:'
        print candidate_dict
        
        #print i
    #print candidate_dict
    return candidate_dict


dir = views_sax_sci
sax_list = []
scientist_dict = load_simple_json(scientists_file)

# FOR TESTING
scientist_list=['1.txt','2.txt','3.txt','4.txt','5.txt']
for scientist in scientist_list:
    filename = os.path.join(test + "\\"+scientist)
    ts_list=read_sax(filename)
    sax_list.append(ts_list)
print 'SAX list:', sax_list
candidate_dict = random_masking(sax_list)

# REAL CODE

# for scientist in scientist_dict:
#     scientist = scientist.rstrip().split('/')[-1]
#     filename = os.path.join(dir + '\\' + scientist + '.txt')
#     ts_list=read_sax(filename)
#     sax_list.append(ts_list)
# candidate_dict = random_masking(sax_list)
# 
# with open('candidate_list.json', 'w') as f:
#         json.dump(candidate_dict, f, indent=4, sort_keys=True)
