from datetime import date
from pdfminer.high_level import extract_text
from tqdm import tqdm
import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import re
import os ; import sys
import time


st.sidebar.write("[github](https://github.com/tonton-golio)")


# file manangement
def file_selector(directory='data/Results/', radio_text='select', filetype=None):
    # get filenames
    list_dir = sorted(os.listdir(directory))
    filenames = []
    for i in list_dir:
        if i[0] != '.':
            if filetype != None:
                if i.split('.')[1] == filetype:
                    filenames.append(i)
            else:
                filenames.append(i)

    filename = st.radio(radio_text, filenames)
    return directory+filename

def dict_extractor(filename):
    file = np.load(filename, allow_pickle=1)
    dictionary = file[file.files[0]].item()
    return dictionary


# General
def get_yearMonth(string):
    splitted = string.split('_')
    year = int(splitted[1])
    month = (int(splitted[2][-1]))*3

    time_stamp = date(year,month,1)
    return time_stamp


# regular expressions
def count_re_matches(re_string, string):
    return len(re.findall(re_string, string))

def count_re_matches_diff(re_string, string):
    return len(set(re.findall(re_string, string)))


# 1 shareholder decks
def make_text_dictionary(companies, shareholder_decks_location = "data/Shareholder_decks/", save_location = "data/Text_dicts/", build_on_date='2022-02-22'):
    """
        I dont wanna do this whole thing again... every time i add more data...
        perhaps make an output file rather than the excessive printing
    """
    if build_on_date != None:
        file = np.load(f'{save_location}{build_on_date}.npz', allow_pickle=True)
        dictionary = file[file.files[0]].item()

    else:
        dictionary = {}

    errors = {'already in dataset' : [],
                'extraction error' : [],
                'not a pdf'        : []
                }
    for company in tqdm(companies):
        report_filenames = os.listdir(shareholder_decks_location+company)
        
        if company in dictionary.keys(): pass
        else: dictionary[company] = {}
        
        for report_filename in report_filenames:
            report = report_filename[:-4]
            file_extension = report_filename[-4:]

            if report in dictionary[company].keys():
                errors['already in dataset'].append(f'{company}/{report_filename}')
            elif file_extension == '.pdf':
                try:
                    text = extract_text(shareholder_decks_location+company+'/'+report_filename, caching=False)

                    dictionary[company][report] = {'text':text}
                except:
                    errors['extraction error'].append(f'{company}/{report_filename}')
            else:
                errors['not a pdf'].append(f'{company}/{report_filename}')
    
    print('ERRORS:\n',errors)
    np.savez(save_location+f'{str(date.today())}.npz', dictionary)

# 2 Keyword dict



# 3 match counts
def match_counts(keyword_dict, text_dict, file_location='data/Results/'):
    word_counts = {}
    companies = text_dict.keys()
    for company in tqdm(companies):
        reports = text_dict[company].keys()
        for report in reports:
            string = text_dict[company][report]['text']
            for cat in keyword_dict.keys():

                count_cat = 0
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
                                count_cat += finding
                                if cat in word_counts:
                                    word_counts[cat][text] = finding
                                else:
                                    word_counts[cat]= {text: finding}
                                found = True
                                break
                        break
                
                         
                text_dict[company][report][cat] = count_cat

    st.write('lookup done')

    #### convert to DataFrame and format
    df = pd.concat({k: pd.DataFrame(v).T for k, v in text_dict.items()}, axis=0).drop(columns=['text'])
    df.reset_index(inplace=True)

    df=df[:-1] # cuz the last one is currently bad

    df['level_2'] = df['level_1'].apply(get_yearMonth)
    df.rename({'level_2': 'period', 'level_0':'company'}, axis=1, inplace=True)

    df = df.groupby(by=['period', 'company']).sum()
    path = f'{file_location}{str(date.today())}.npz'
    np.savez(path, (df, word_counts))

    return path

def load_match_counts(path):
    file = np.load(path, allow_pickle=True)
    df, word_counts = file[file.files[0]]
    return df, word_counts

def display_match_counts(df, word_counts):
    st.write(df)

    fig, ax = plt.subplots(1, len(word_counts), figsize=(10,8))
    for idx, cat in enumerate(word_counts):
        ax[idx].barh(range(len(word_counts[cat])),
                    word_counts[cat].values())
        ax[idx].set_yticks(range(len(word_counts[cat])), 
                            word_counts[cat].keys(), 
                            rotation=0, )
        ax[idx].set(title=cat.split()[0])
    plt.tight_layout()
    st.pyplot(fig)
    plt.close()


# 4 obtain scores
def get_locations_of_keywords(text_file,keyword_dict, category ='DBS'):
    locations_of_keywords = {'words':[],'starts' : [], 'stops': []}
    for index in keyword_dict[category]:
        #for form in ['text','lemmas','stems']:
        p = re.compile(keyword_dict[category][index]['text'])
        for m in p.finditer(text_file):
            locations_of_keywords["words"].append(m.group())
            locations_of_keywords["starts"].append(m.start())
            locations_of_keywords["stops"].append(m.end())
    return locations_of_keywords

def prevalence(word_counts, keyword):
    wc = word_counts
    max_val = max([max(wc[i].values()) for i in wc])
    for i in word_counts:
        if keyword in word_counts[i].keys():
            return word_counts[i][keyword]/max_val
    return 0

    
def get_distances_and_prevalence(text_file, keyword_dict, word_counts):
    '''a list of distances from the start and end of each scope keyword to the nearest dbs keyword'''

    distances_and_prevalence = {}
    dbs = get_locations_of_keywords(text_file,keyword_dict, category=list(keyword_dict.keys())[0])

    for category in keyword_dict.keys():
        if category == 'DBS':
            pass
        else:
            distances_and_prevalence[category] = {}
            locs = get_locations_of_keywords(text_file, keyword_dict,  category=category)
            distance_to_dbs_keywords = [[min(abs(np.array(dbs['starts']+dbs['stops'])-i)), min(abs(np.array(dbs['starts']+dbs['stops'])-j)) ] for i, j in zip(locs['starts'], locs['stops'])]
            distances_and_prevalence[category]["distances"] = np.min(np.array(distance_to_dbs_keywords), axis=1)
            distances_and_prevalence[category]["prevalence"] = [prevalence(word_counts, word) for word in locs['words']]
    return distances_and_prevalence

def getScores(distances_and_prevalence, a=.5):
    scores = {}
    for category in distances_and_prevalence.keys():
        arr = np.array(list(distances_and_prevalence[category].values()))
        arr[0] = np.exp(-a*(arr[0]-1))
        arr[1] = 1-arr[1]
        scores[category] = sum(arr[0]*arr[1])
    return scores

