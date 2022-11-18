from DBS_utils import *

load_or_run = 'run'

if load_or_run =='run':
	with st.sidebar:
		# file manangement
		filename_dists = file_selector(directory='data/Results/distances_and_prevalences/', 
											radio_text='dist file',
											filetype=None)

		distances_and_prevalences = dict_extractor(filename_dists)


		filename_text = file_selector(directory='data/Text_dicts/', 
											radio_text='Text dict',
											filetype=None)

		text_dict = dict_extractor(filename_text)

data = {}

companies = distances_and_prevalences.keys()
for company in companies:
	data[company] = {}
	for report in distances_and_prevalences[company].keys():
		data[company][report] = {}
		for cat in distances_and_prevalences[company][report].keys():

			avg_dist = np.mean(distances_and_prevalences[company][report][cat]['distances'])
			data[company][report][cat.split()[0]+'_avg_dist'] = avg_dist
			data[company][report][cat.split()[0]+'_matches'] = len(distances_and_prevalences[company][report][cat]['distances'])

df = pd.concat({k: pd.DataFrame(v).T for k, v in data.items()}, axis=0)
df.reset_index(inplace=True)
df.rename(columns={'level_0':'company', 'level_1':'report'}, inplace=True)

a = text_dict['Dexcom'].keys()
a

lengths = [len(text_dict[company][report]['text']) for company, report in zip(df.company, df.report)]


df["length"] = lengths

df
