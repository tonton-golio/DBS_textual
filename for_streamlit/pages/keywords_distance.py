# keywords_distance.py

import streamlit as st

from streamlit_utils import *


load_or_run = st.sidebar.radio('choose one:', ['load', 'run'])


if load_or_run == 'run':
	data = {}
	for i, company in enumerate(text_dict.keys()):
		if i%5==0:
			st.write(round(i/len(companies)*100),'%')

		data[company] = {}
		for report in text_dict[company].keys():
			try:
				report_formatted = ''.join(report.split('_')[1:])
				data[company][report_formatted] = getScore(get_distances_and_prevalence(text_dict[company][report]['text']))
			except:
				print(report)
	df = pd.DataFrame.from_dict(data).sort_index()
	'dataframe', df
	df.to_csv('../../data/scores_{}.csv'.format(round(time.time())))
else:
	loc = "/Users/antongolles/Documents/Work/ITU-Research/data/"
	files_in_data = os.listdir(loc)
	score_files = []
	max_time, latest_score_file = 0, None
	for file in files_in_data:
		if file[:6] == 'scores':
			score_files.append(file)
			timeStamp = int(file.split('_')[1].replace('.csv',''))
			if timeStamp > max_time:
				max_time = timeStamp
				latest_score_file = file
	if latest_score_file == None:
		st.write('no file found')
	else:
		df = pd.read_csv(loc+latest_score_file)
		df.rename(columns={'Unnamed: 0': 'period'}, inplace=True)
		df['time'] = df['period'].apply(lambda x: int(x.split('Q')[0])+(int(x.split('Q')[1])-1)*.25)
		df.set_index('time', inplace=True)
		'dataframe', df
		df.drop(columns=['period'], inplace=True)
		fig, ax = plt.subplots()
		df.plot(ax=ax)
		plt.legend([])
		st.pyplot(fig)

		





	