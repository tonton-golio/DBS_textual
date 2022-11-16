from DBS_utils import *


load_or_run = st.sidebar.radio('choose one:', ['load', 'run'])

if load_or_run == 'run':

	with st.sidebar:
		# file manangement
		filename_keywords = file_selector(directory='data/Keywords/', 
											radio_text='Keywords dict',
											filetype='npz')
		filename_text = file_selector(directory='data/Text_dicts/', 
											radio_text='Text dict')
		filename_counts = file_selector(directory='data/Results/Match_counts/', 
											radio_text='Match counts file')
		keyword_dict = dict_extractor(filename_keywords)
		text_dict = dict_extractor(filename_text)
		companies = text_dict.keys()
		_, word_counts = load_match_counts(filename_counts)


	data = {}
	distances_and_prevalences = {}
	for i, company in enumerate(companies):
		data[company] = {}
		distances_and_prevalences[company] = []
		for report in text_dict[company].keys():
			try:
			

				distances_and_prevalence = get_distances_and_prevalence(text_dict[company][report]['text'], keyword_dict, word_counts)
				distances_and_prevalences[company][report] = distances_and_prevalence

				report_name_formatted = ''.join(report.split('_')[1:])
				data[company][report_name_formatted] = getScores(distances_and_prevalence)
			except:
				st.write('Error at', report)

	df = pd.DataFrame.from_dict(data).sort_index()
	df = pd.concat({k: pd.DataFrame(v).T for k, v in data.items()}, axis=1)
	'dataframe', df
	df.to_csv(f'data/Results/Scores/{str(date.today())}.csv')

	np.savez(f'data/Results/distances_and_prevalences/{str(date.today())}', distances_and_prevalences)

	
elif load_or_run =='load':
	with st.sidebar:
		# file manangement
		filename_scores = file_selector(directory='data/Results/Scores/', 
											radio_text='Scores csv',
											filetype='csv')

	df = pd.read_csv(filename_scores, index_col=0, header=[0,1])
	df