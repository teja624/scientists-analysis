'''
Created on Jul 16, 2016

@author: Tania
'''
import json
import os
from datetime import datetime
import numpy as np
import matplotlib.pyplot as plt
import urllib2

#TODO: show to hists in one plot (seed+baseline)

base_dir = os.path.dirname(os.path.dirname(__file__))
data_dir = os.path.join(base_dir, 'data')
baseline_dir = os.path.join(data_dir, 'baseline')
seed_dir = os.path.join(data_dir, 'seed')
neighbors_dir = os.path.join(data_dir, 'neighbors')
plots_dir = os.path.join(data_dir, 'plots')
plots_dir = os.path.join(plots_dir, 'timelag')

def load_simple_json(filename):
    with open(filename, 'r') as f:
        return json.load(f)

def days_between(d1, d2):
    d1 = datetime.strptime(d1, "%Y-%m-%d")
    d2 = datetime.strptime(d2, "%Y-%m-%d")
    return (d2 - d1).days

def weekly_aggregation(time_list):
    weekly_list = []
    for day in time_list:
        day = day/7
        weekly_list.append(day)
    return weekly_list

def monthly_aggregation(time_list):
    monthly_list = []
    for day in time_list:
        day = day/30
        monthly_list.append(day)
    return monthly_list


def plotting(array, name):
    plt.title("Time lag between the articles creation")
    plt.xlabel("Time lag (months)")
    plt.ylabel("Probability")
    plt.hist(array, bins=50, normed = True)
    #plt.show()
    plt.savefig(plots_dir+name)
    return

# Plot the frequency distribution
def plot_distribution(seed, baseline, name):
    seed, base_seed = np.histogram(seed, bins=50)
    baseline, base_baseline = np.histogram(baseline, bins=50)
    cumulative_seed = np.cumsum(seed)
    print cumulative_seed
    cumulative_seed = np.float32(cumulative_seed)/np.max(cumulative_seed)
    print cumulative_seed
    cumulative_baseline = np.cumsum(baseline)
    cumulative_baseline = np.float32(cumulative_baseline)/np.max(cumulative_baseline)
    plt.title("Time lag between the articles creation")
    plt.xlabel("Time lag (months)")
    plt.ylabel("Number of pages created")
    plt.plot(base_seed[:-1], cumulative_seed, c='blue', label = 'seed data')
    plt.plot(base_baseline[:-1], cumulative_baseline, c='green', label = 'baseline data')
    plt.plot([0,0], [0,max(cumulative_seed)], c='black', linestyle = 'dashed')
    #bins = range(-20, 20)
    #plt.xticks(bins, ["2^%s" % i for i in bins])
    #plt.hist(seed, normed = True, bins=bins, label = 'seed data',  cumulative = True, histtype = 'step')
   # plt.hist(baseline, normed = True, bins=bins, label = 'baseline data',  cumulative = True, histtype = 'step')
    plt.legend(loc='upper left')
  #  plt.show()
    plt.savefig(plots_dir+name)
    return


filename =  os.path.join(neighbors_dir, 'baseline_topic_creation_date.json')    
topic_dict_baseline = load_simple_json(filename)

filename =  os.path.join(baseline_dir, 'baseline_creation_date.json')    
scientist_dict_baseline = load_simple_json(filename)

filename =  os.path.join(neighbors_dir, 'baseline_neighbors_list_clean_en.json')    
main_dict_baseline = load_simple_json(filename)

filename =  os.path.join(neighbors_dir, 'seed_topic_creation_date.json')    
topic_dict_seed = load_simple_json(filename)

filename =  os.path.join(seed_dir, 'seed_creation_date.json')    
scientist_dict_seed = load_simple_json(filename)

filename =  os.path.join(neighbors_dir, 'seed_neighbors_list_clean_en.json')    
main_dict_seed = load_simple_json(filename)


timelag_dict = {}
time_list = []

def get_series(main_dict, scientist_dict, topic_dict):
    time_list = []
    for scientist, topic_list in main_dict.iteritems():     
        #scientist = scientist.encode("utf-8")
        #scientist = urllib2.unquote(scientist).decode("utf-8")
        #scientist = urllib.quote_plus(scientist.encode("utf-8"))
        print scientist
        if topic_list!=[]:
            scientist_date = scientist_dict.get(scientist).get('Page_created').rstrip().split('T')[0]
            for topic in topic_list:
                topic_date = topic_dict.get(topic).rstrip().split('T')[0]
                time_lag = days_between(scientist_date, topic_date)
                time_list.append(time_lag)
    return time_list

seed = get_series(main_dict_seed, scientist_dict_seed, topic_dict_seed)
baseline = get_series(main_dict_baseline, scientist_dict_baseline, topic_dict_baseline)
seed = monthly_aggregation(seed)
baseline = monthly_aggregation(baseline)


plot_distribution(seed, baseline, '/timelag_monthly_normed.jpg')
#plotting(baseline, '/timelag_monthly_(baseline_creation_date).pdf')
#plotting(seed, '/timelag_monthly_(seed_creation_date).pdf')

