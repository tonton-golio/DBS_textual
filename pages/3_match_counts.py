from DBS_utils import *
st.title('Keyword matches')


with st.sidebar:
	load_or_run = st.radio('Load or run', ['load', 'run'])


if load_or_run == 'load':
	# get filenames
	list_dir = os.listdir('data/Results/')
	files = []
	for i in list_dir:
		if i[0] != '.':
			files.append(i)

	# Choose filename
	with st.sidebar:
		st.markdown('### ------------------')
		filename = st.radio('filename',files)
	path = 'data/Results/'+filename

	# Load and display dataframe
	df = pd.read_csv(path)#, index_col=[0,1])
	df['period']=pd.to_datetime(df.period)
	df.sort_values(['company', 'period'], inplace=True)
	'dataframe:', df


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


	df = match_counts(keyword_dict, text_dict)
	'dataframe', df