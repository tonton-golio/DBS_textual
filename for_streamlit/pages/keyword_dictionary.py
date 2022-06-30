import re
import numpy as np
import streamlit as st

from streamlit_utils import *


# Sidebar
st.title('Keyword dictionary')
st.sidebar.write("[github](https://github.com/tonton-golio)")



file = np.load('../../data/keywords_dict.npz', allow_pickle=1)
dic_loaded = file[file.files[0]].item()


df_keywords  = pd.concat({k: pd.DataFrame(v).T for k, v in dic_loaded.items()}, axis=0)

'dataframe:', df_keywords