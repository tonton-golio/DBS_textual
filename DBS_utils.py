#DBS_utils.py

import os
from datetime import date
from pdfminer.high_level import extract_text
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from tqdm import tqdm


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
    for company in companies:
        report_filenames = os.listdir(PWD+relative_location+company)
        if company in dictionary.keys():
            pass
        else:
            dictionary[company] = {}
        for report_filename in tqdm(report_filenames):
            if report_filename[:-4] in dictionary[company].keys():
                print('already in dataset', relative_location+company+'/'+report_filename)
            elif report_filename[-4:] == '.pdf':
                try:
                    #print(relative_location+company+'/'+report_filename)
                    text = extract_text(relative_location+company+'/'+report_filename)
                    dictionary[company][report_filename[:-4]] = {'text':text}
                except:
                    print('ERROR:', relative_location+company+'/'+report_filename)
            else:
                print('not a pdf', relative_location+company+'/'+report_filename)
    date_today = str(date.today())
    np.savez(relative_location+f'text_from_shareholder_decks_{date_today}.npz', dictionary)