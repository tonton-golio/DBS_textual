from DBS_utils import *

load_or_run = 'run'

if load_or_run =='run':
	with st.sidebar:
		# file manangement
		filename_dists = file_selector(directory='data/Results/distances_and_prevalences/', 
											radio_text='dist file',
											filetype=None)

		distances_and_prevalences = dict_extractor(filename_dists)

data = {}

companies = distances_and_prevalences.keys():
for company in companies:
	data[company] = {}
	for report in distances_and_prevalences[company].keys():
		data[company][report] = {}
		for cat in distances_and_prevalences[company][report].keys():

			avg_dist = np.mean(distances_and_prevalences[company][report][cat]['distances'])
			data[company][report][cat+'_avg_dist'] = avg_dist
			data[company][report][cat+'_matches'] = len(distances_and_prevalences[company][report][cat]['distances'])

data

# make sure scores have cols of each category, and index of company+time



# add more cols:
'''
df[length] = len(text_dict[company][report]['text'])

df[cat_numMatches] = matchcounts[company][report]


avg distance
number of keywords found
score for each category
length of text (characters)

'''