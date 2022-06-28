#DBS_utils.py

from datetime import date
from pdfminer.high_level import extract_text

from tqdm import tqdm

import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

import pandas as pd
import seaborn as sns

import re

import os
import sys

import time



def get_company_names(list_dir):
    companies = []
    for i in list_dir:
        if len(i.split('.'))==1:
            companies.append(i)
    return companies


def get_text_dicts(list_dir):
    text_dicts = []
    for i in list_dir:
        if len(i.split('.npz'))==2:
            text_dicts.append(i)
    return text_dicts

def get_keyword_result_dfs(list_dir):
    keyword_result_dfs = []
    for i in list_dir:
        if len(i.split('.npz'))==2:
            keyword_result_dfs.append(i)
    return keyword_result_dfs


def count_re_matches(re_string, string):
    return len(re.findall(re_string, string))

def count_re_matches_diff(re_string, string):
    return len(set(re.findall(re_string, string)))



def make_text_dictionary(companies, PWD, relative_location, build_on_date='2022-02-22', output_file=False):
    
    #I dont wanna do this whole thing again... every time i add more data...
    # perhaps make an output file rather than the excessive printing
    #if output_file:
    #	with open 
    if build_on_date != None:
        file = np.load(relative_location+f'text_from_shareholder_decks_{build_on_date}.npz', allow_pickle=True)
        dictionary = file[file.files[0]].item()

    else:
        dictionary = {}

    errors = []
    for company in tqdm(companies):
        if company == 'companies':
            pass
        else:
            report_filenames = os.listdir(PWD+relative_location+company)
            if company in dictionary.keys():
                pass
            else:
                dictionary[company] = {}
            for report_filename in report_filenames:
                if report_filename[:-4] in dictionary[company].keys():
                    errors.append('already in dataset: '+ relative_location+company+'/'+report_filename)
                elif report_filename[-4:] == '.pdf':
                    try:
                        #print(relative_location+company+'/'+report_filename)
                        text = extract_text(relative_location+company+'/'+report_filename)
                        dictionary[company][report_filename[:-4]] = {'text':text}
                    except:
                        errors.append('ERROR:  '+ relative_location+company+'/'+report_filename)
                else:
                    errors.append('not a pdf  '+ relative_location+company+'/'+report_filename)
    
    print('ERRORS:\n',errors)
    date_today = str(date.today())
    np.savez(relative_location+f'text_from_shareholder_decks_{date_today}.npz', dictionary)


def get_yearMonth(string):
    splitted = string.split('_')
    year = int(splitted[1])
    month = (int(splitted[2][-1]))*3

    time_stamp = date(year,month,1)
    return time_stamp

def new_keyword_find_dict_df():
	for company in tqdm(companies):
	    reports = text_dict[company].keys()
	    for report in reports:
	        string = text_dict[company][report]['text']
	        for cat in keyword_dict.keys():
	            count = 0
	            for index in keyword_dict[cat].keys():
	                (text, lemmas, stems) =     (keyword_dict[cat][index]['text'], 
	                                            keyword_dict[cat][index]['lemmas'], 
	                                            keyword_dict[cat][index]['stems'])
	                found = False
	                while found == False:
	                    for i in [text, lemmas, stems]:
	                        if type(i) == list:
	                            i = ' '.join(i)
	                        finding = count_re_matches(i, string)
	                        if finding != 0:
	                            count += finding
	                            found=True
	                            break
	                    break
	                        
	            #print(company,report,cat,count)
	            text_dict[company][report][cat] = count

	df = pd.concat({k: pd.DataFrame(v).T for k, v in text_dict.items()}, axis=0).drop(columns=['text'])
	df.reset_index(inplace=True)

	df=df[:-1] # cuz the last one is currently bad

	df['level_2'] = df['level_1'].apply(get_yearMonth)
	df.rename({'level_2': 'period', 'level_0':'company'}, axis=1, inplace=True)

	df = df.groupby(by=['period', 'company']).sum()
	df.to_csv('../data/results_dataframe_{}.csv'.format(date_today))



def get_locations_of_keywords(text_file,
                             category ='DBS'):
    locations_of_keywords = {'words':[],'starts' : [], 'stops': []}
    for index in keyword_dict[category]:
        #for form in ['text','lemmas','stems']:
        p = re.compile(keyword_dict[category][index]['text'])
        for m in p.finditer(text_file):
            locations_of_keywords["words"].append(m.group())
            locations_of_keywords["starts"].append(m.start())
            locations_of_keywords["stops"].append(m.end())
    return locations_of_keywords

def prevalence(keyword):
    return list(prevalence_df[prevalence_df['index'] == keyword]['count'])[0]/prevalence_df["count"].max()
    
def get_distances_and_prevalence(text_file):
    '''a list of distances from the start and end of each scope keyword to the nearest dbs keyword'''
    distances_and_prevalence = {}
    dbs = get_locations_of_keywords(text_file,category=list(keyword_dict.keys())[0])

    for category in keyword_dict.keys():
        if category == 'DBS':
            pass
        else:
            distances_and_prevalence[category] = {}
            locs = get_locations_of_keywords(text_file, category=category)
            distance_to_dbs_keywords = [[min(abs(np.array(dbs['starts']+dbs['stops'])-i)), min(abs(np.array(dbs['starts']+dbs['stops'])-j)) ] for i, j in zip(locs['starts'], locs['stops'])]
            distances_and_prevalence[category]["distances"] = np.min(np.array(distance_to_dbs_keywords), axis=1)
            distances_and_prevalence[category]["prevalence"] = [prevalence(word) for word in locs['words']]
    return distances_and_prevalence

def getScore(distances_and_prevalence, a=.5):
    score = 0
    for category in distances_and_prevalence.keys():
        arr = np.array(list(distances_and_prevalence[category].values()))
        arr[0] = np.exp(-a*(arr[0]-1))
        arr[1] = 1-arr[1]
        score += sum(arr[0]*arr[1])
    return score

#######
# streamlit specific -- all around variables


PWD = "/Users/antongolles/Documents/Work/ITU-Research/DBS_textual/"
relative_location = "../data/Shareholder_decks/"
list_dir = os.listdir(PWD+relative_location)

date_today = str(date.today())

companies = get_company_names(list_dir)

text_dicts = get_text_dicts(list_dir)
text_dicts = dict([(i.replace('text_from_shareholder_decks_','').replace('.npz',''),
	i)  for i in text_dicts])
sorted_text_dict_names = sorted(list(text_dicts.keys()))[::-1]
text_dict_name = text_dicts[sorted_text_dict_names[0]]
file = np.load(PWD+relative_location+text_dict_name, allow_pickle=True)
text_dict = file[file.files[0]].item()


keyword_file = np.load('../../data/keywords_dict.npz', allow_pickle=1)
keyword_dict = keyword_file[keyword_file.files[0]].item()



keyword_find_df_file_names = 1



date_latest = '2022-05-18'

prevalence_df = pd.read_csv('../../data/matches_on_words_df{}.csv'.format('2022-06-13'), index_col=0)

