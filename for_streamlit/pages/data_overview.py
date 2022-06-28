from streamlit_utils import *

import streamlit as st


# Sidebar
st.title('Data overview')
st.sidebar.write("[github](https://github.com/tonton-golio)")


text_dict_name = text_dicts[st.sidebar.radio('text_dicts',sorted_text_dict_names)]

## make new text_dict
make_new_text_dictionary = st.sidebar.button('make_new_text_dictionary (building on latest), this takes a while')
if make_new_text_dictionary:
	make_text_dictionary(companies, PWD, relative_location,build_on_date=sorted_text_dict_names[0])



file = np.load(PWD+relative_location+text_dict_name, allow_pickle=True)
text_dict = file[file.files[0]].item()


# Lets see if we have an appropriate number of each
fullness_dict = {}
for company in text_dict.keys():
    fullness_dict[company] = []
    for report in text_dict[company].keys():
        year, quarter = int(report.split('_')[1]), int(report.split('_')[2][1])
        fullness_dict[company].append(year+quarter*.25-.25)
   
fig = plt.figure(figsize=(8,18))
for index,company in enumerate(sorted(list(fullness_dict.keys()))[::-1]):
    plt.scatter(fullness_dict[company], [index]*len(fullness_dict[company]))
plt.yticks(range(len(fullness_dict.keys())), sorted(list(fullness_dict.keys()))[::-1], rotation=0);
st.pyplot(fig)










