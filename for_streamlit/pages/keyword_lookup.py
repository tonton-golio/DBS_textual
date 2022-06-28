import re
import numpy as np
import streamlit as st

from streamlit_utils import *


# Sidebar
st.title('Keyword matches')
st.sidebar.write("[github](https://github.com/tonton-golio)")


'''
keyword_find_dict_name = texrt_dicts[st.sidebar.radio('text_dicts',sorted_text_dict_names)]

## make new text_dict
make_new_keyword_find_dict_df = st.sidebar.button('make_new_keyword_find_dict_df (building on latest), this takes a while')
if make_new_keyword_find_dict_df:
	new_keyword_find_dict_df()

'''


df = pd.read_csv('../../data/results_dataframe_{}.csv'.format('2022-05-18'))#, index_col=[0,1])
df['period']=pd.to_datetime(df.period)
df.sort_values(['company', 'period'], inplace=True)

'dataframe:', df
