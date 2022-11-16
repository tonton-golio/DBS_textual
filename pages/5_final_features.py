from DBS_utils import *

load_or_run = 'run'

if load_or_run =='run':
	with st.sidebar:
		# file manangement
		filename_dists = file_selector(directory='data/Results/distances_and_prevalences/', 
											radio_text='dist file',
											filetype=None)

	file = np.load(filename_dists, allow_pickle=True)
	distances_and_prevalences = file[file.files[0]]

distances_and_prevalences
# make sure scores have cols of each category, and index of company+time



# add more cols:
'''
df[length] = len(text_dict[company][report]['text'])

df[cat_numMatches] = matchcounts[company][report]



'''