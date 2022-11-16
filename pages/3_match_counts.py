from DBS_utils import *
st.title('Keyword matches')


with st.sidebar:
	load_or_run = st.radio('Load or run', ['load', 'run'])


if load_or_run == 'load':
	with st.sidebar:
		path = file_selector(directory='data/Results/Match_counts/', radio_text='select', filetype=None)
    

	# Load and display dataframe
	df, word_counts = load_match_counts(path)
	display_match_counts(df, word_counts)


elif load_or_run == 'run':
	with st.sidebar:
		st.markdown('### ------------------')

		filename_keywords = file_selector(directory='data/Keywords/', 
											radio_text='Keywords dict',
											filetype='npz')
		
		filename_text = file_selector(directory='data/Text_dicts/', 
											radio_text='Text dict')

		keyword_dict = dict_extractor(filename_keywords)
		text_dict = dict_extractor(filename_text)


	path = match_counts(keyword_dict, text_dict, file_location='data/Results/Match_counts/')
	df, word_counts = load_match_counts(path)
	display_match_counts(df, word_counts)