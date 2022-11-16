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


# regular expressions
def count_re_matches(re_string, string):
    return len(re.findall(re_string, string))

def count_re_matches_diff(re_string, string):
    return len(set(re.findall(re_string, string)))



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
	df.to_csv('../data/results_dataframe_{}.csv'.format(str(date.today())))

def match_count():
    companies = os.listdir('data/Shareholder_decks')
    matches_on_words = {}

    matches_on_words_company = {}
    for company in companies:
        matches_on_words_company[company] = {}

        
    matches_on_words_quarter = {}
    for quarter in df.level_1.apply(lambda x: ''.join(x.split('_')[1:])).unique():
        matches_on_words_quarter[quarter] = {}


    companies = text_dict.keys()
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
                            finding = count_re_matches_diff(i, string)
                            if (finding != 0 and found == False):
                                if text in matches_on_words.keys():
                                    matches_on_words[text]['count'] += 1
                                else:
                                    matches_on_words[text] = {'count' : 1, 'category':cat}
                                    
                                if text in matches_on_words_company[company].keys():
                                    matches_on_words_company[company][text] += 1
                                else:
                                    matches_on_words_company[company][text] = 1
                                    
                                quarter = ''.join(report.split('_')[1:])
                                if text in matches_on_words_quarter[quarter].keys():
                                    matches_on_words_quarter[quarter][text] += 1
                                else:
                                    matches_on_words_quarter[quarter][text] = 1
                                
                                count += finding
                                found=True
                                break
                        break

    matches_on_words_df = pd.DataFrame.from_dict(matches_on_words).T.sort_values('count', ascending=False).reset_index()
    matches_on_words_df

    matches_on_words_df.to_csv('data/Results/matches_on_words_df{}.csv'.format(str(date.today())))




    fig, ax = plt.subplots(6,1, figsize=(13,20))

    for index, cat in enumerate(matches_on_words_df.category.unique()):
        
        sns.barplot(data=matches_on_words_df[matches_on_words_df.category == cat],
                    x='index', y='count', ax=ax[index]);
        ax[index].set_xticklabels(ax[index].get_xticklabels(),rotation = 90);
        ax[index].set_title(cat)
        ax[index].set_ylabel(cat)
    plt.tight_layout()
    st.pyplot(fig)
    plt.close()


def match_counts(keyword_dict, text_dict):
    companies = text_dict.keys()
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
                            
                text_dict[company][report][cat] = count

    st.write('lookup done')

    #### convert to DataFrame and format
    df = pd.concat({k: pd.DataFrame(v).T for k, v in text_dict.items()}, axis=0).drop(columns=['text'])
    df.reset_index(inplace=True)

    df=df[:-1] # cuz the last one is currently bad

    df['level_2'] = df['level_1'].apply(get_yearMonth)
    df.rename({'level_2': 'period', 'level_0':'company'}, axis=1, inplace=True)

    df = df.groupby(by=['period', 'company']).sum()
    df.to_csv(f'data/Results/match_counts_{str(date.today())}.csv')
    return df

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

'''
PWD = "/Users/antongolles/Documents/Work/ITU-Research/DBS_textual/"
relative_location = "data/Shareholder_decks/"
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


keyword_file = np.load('data/Keywords/keywords_dict.npz', allow_pickle=1)
keyword_dict = keyword_file[keyword_file.files[0]].item()



keyword_find_df_file_names = 1



date_latest = '2022-05-18'

prevalence_df = pd.read_csv('data/Results/matches_on_words_df{}.csv'.format('2022-06-13'), index_col=0)


'''
