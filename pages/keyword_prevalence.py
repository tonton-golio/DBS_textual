from DBS_utils import *
st.markdown(r"""
    # Keyword prevalence
    we look for number of matches of each keyword. As is clear (and expected) the
    prevalence of some keyword is much higher than that of others. We will use this
    for weighting influence.
    """)
with st.sidebar:
    load_or_run = st.radio('choose one:', ['load', 'run'])

if load_or_run == 'load':

    prevalence_df = pd.read_csv('data/Results/matches_on_words_df{}.csv'.format('2022-06-13'), index_col=0)

    fig, ax = plt.subplots(5,1, figsize=(13,20))

    for index, cat in enumerate(prevalence_df.category.unique()):
        
        sns.barplot(data=prevalence_df[prevalence_df.category == cat],
                    x='index', y='count', ax=ax[index]);
        ax[index].set_xticklabels(ax[index].get_xticklabels(),rotation = 90);
        ax[index].set_title(cat)
        ax[index].set_ylabel(cat)
    plt.tight_layout()
    st.pyplot(fig)
    plt.close()

elif load_or_run == 'run':
    match_count()


'''
the DataFrame of keyword matches is obtained using the following code
'''

st.code('''matches_on_words = {}


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
                    
''')

'''
I know, I know... it's not very pretty :/
'''