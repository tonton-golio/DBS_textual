# duplicate_finder.py


filename = '../../dictionary_june.txt'

with open(filename) as f:
	file = f.read().split('\n')
new = True

out = {}
count = {}
for i in file:
	if i == '':
		new = True
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
		print(i, 'appears {} times, in '.format(count[i]['count']), count[i]['categories'])