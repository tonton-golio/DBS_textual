from DBS_utils import *
import streamlit as st

st.sidebar.write("[github](https://github.com/tonton-golio)")


def overview():
    st.title('Data overview')

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
    plt.close()


def report_lengths():
    st.markdown('## Report lengths')


    # Lets find the outliers
    lengths_company = {}
    for company in text_dict.keys():
        lengths_company[company] = {}
        for report in text_dict[company].keys():
            try:
                report = company+'_'+'_'.join(report.split('_')[1:])
                report_length = len(text_dict[company][report]['text']) 
            except:
                report_length = None
            lengths_company[company][''.join(report.split('_')[1:])] = report_length 
    lengths_df = pd.DataFrame.from_dict((lengths_company)).sort_index()
    
    fig, ax = plt.subplots()
    sns.heatmap(lengths_df, ax=ax)
    st.pyplot(fig)
    plt.close()


def inspector_gadget():
    st.markdown('## Inspector gadget')
    cols = st.columns(2)
    company = cols[0].selectbox('company', text_dict.keys())
    report = cols[1].selectbox('report', text_dict[company].keys())

    st.markdown(text_dict[company][report]['text'])

func_dict = {
    'overview': overview,
    'report_lengths' : report_lengths,
    'inspector_gadget': inspector_gadget,
    }

with st.sidebar:
    func_name = st.radio('func', func_dict.keys())


# get filenames
text_dict_names = sorted(os.listdir("data/Text_dicts/"))
text_dict_name = st.sidebar.radio('text dict',text_dict_names)


# make new text_dict
make_new_text_dictionary = st.sidebar.button('Build new (this takes a while)')
if make_new_text_dictionary:        
    make_text_dictionary(
        companies        = os.listdir("data/Shareholder_decks/"),
        shareholder_decks_location = "data/Shareholder_decks/",
        save_location = "data/Text_dicts/",
        build_on_date     = None)


# Load
file = np.load('data/Text_dicts/'+text_dict_name, allow_pickle=True)
text_dict = file[file.files[0]].item()


# run page
func = func_dict[func_name]; func()







