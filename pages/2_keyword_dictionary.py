from DBS_utils import *


# Sidebar
st.title('Keyword dictionary')

def duplicate_finder():
	def duplicates_in_dictionary(filename = 'data/Keywords/dictionary_june.txt'):

		with open(filename) as f:
			file = f.read().split('\n')
		new = True

		out = {}
		count = {}
		for i in file:
			if i == '': new = True
			else:
				if new == True:
					out[i] = []
					last_title = i 
					new = False
					
				else:
					out[last_title].append(i)
					if i in count.keys():
						count[i]['count'] += 1
						count[i]['categories'] += [last_title]
					else:
						count[i] = {'count': 1, 'categories':[last_title]}

		for i in count.keys():
			if count[i]['count'] > 1:
				st.write(i, 'appears {} times, in '.format(count[i]['count']), count[i]['categories'])

	with st.sidebar:
		st.markdown('### ------------------')
		filename = file_selector(directory='data/Keywords/', radio_text='filename', filetype='txt')
		
	duplicates_in_dictionary(filename)

def make_keywords_dictionary():
	import spacy  # for lemmanizing
	nlp = spacy.load('en_core_web_sm')  # here we could easily use a bigger model
	from nltk.stem import PorterStemmer  # for stemming
	ps = PorterStemmer()  # this can also be changed out for other prebuilts

	def remove_trailing_spaces(string):
	    '''simple while loop for removing trailing spaces. returns string less trailing spaces.'''
	    while string[-1] == ' ':
	        string = string[:-1]
	        
	    return string

	def txt2dict(filename = 'data/Keywords/dictionary_v4.txt'):
		# load keywords from text file. Assumes entries are line seperated and categories are seperate by 3 lines
		with open(filename) as f:
		    text=f.read()[:-1]
		   

		# part 3
		lst = [i.split('\n') for i in text.split('\n\n\n')]

		dic = {}
		for i in lst:
		    dic[i[0]] = {}
		    for index, word in enumerate(i[1:]):
		        dic[i[0]][index]= {'text': remove_trailing_spaces(word)}


		# part 4
		for key in dic.keys():
		    for key2 in dic[key].keys():
		        doc = nlp(dic[key][key2]['text'])
		        lemmas = [word.lemma_ for word in doc]
		        dic[key][key2]['lemmas'] = lemmas
		        stems = [ps.stem(str(word)) for word in doc]
		        dic[key][key2]['stems'] = stems
		fig, ax = plt.subplots()
		ax.barh(range(len(dic)),[len(list(dic[key])) for key in dic.keys()])
		ax.set_yticks(range(len(dic)), dic.keys())
		st.pyplot(fig)
		plt.close()
		# part 5
		st.write('Saving as',f'{filename[:-4]}.npz')
		np.savez(f'{filename[:-4]}.npz', dic)

	with st.sidebar:
		st.markdown('### ------------------')
		filename = file_selector(directory='data/Keywords/', radio_text='filename', filetype='txt')


	txt2dict(filename)

def investigate():
	with st.sidebar:
		st.markdown('### ------------------')
		filename = file_selector(directory='data/Keywords/', radio_text='filename', filetype='npz')

	def load_dic_make_df(filename):
		file = np.load(filename, allow_pickle=1)
		dic_loaded = file[file.files[0]].item()
		df  = pd.concat({k: pd.DataFrame(v).T for k, v in dic_loaded.items()}, axis=0)
		return df

	def count_values(lst):
		d = {}
		for i in lst:
			d[i] = d[i]+1 if i in d else 1
		return d

	def plot_bar_from_df(df):
		cat = [i[0] for i in df.index]
		a = count_values(cat)
		fig = plt.figure()
		#plt.pie(a.values(), labels=a.keys()) 
		plt.barh(range(len(a)),list(a.values()))
		plt.yticks(range(len(a)), a.keys(), rotation=0)
		plt.title('Number of entries')
		st.pyplot(fig)
		plt.close()
		'dataframe:', df

	df = load_dic_make_df(filename)
	plot_bar_from_df(df)


func_dict = {
	'Duplicates in txt file': duplicate_finder,
	'make keywords dictionary': make_keywords_dictionary,
	'See results': investigate,
	}

with st.sidebar:
	func_name = st.radio('func', func_dict.keys())
func = func_dict[func_name]; func()