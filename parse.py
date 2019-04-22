#coding=utf-8

files = [
	'the_sorcerers_stone.txt',
	'chamber_of_secrets.txt',
	'prisoner_of_azkaban.txt',
	'goblet_of_fire.txt',
]

movies = [
	'Harry Potter and the Sorcers Stone',
	'Harry Potter and the Chamber of Secrets',
	'Harry Potter and the Prisoners of Azkaban',
	'Harry Potter and the Goblet of Fire',
]

ends = ['.', '?', '!']
unwanted = ['title card', 'the end']

line_num = 0
chars = {}
scripts = []


def legal_char(s):
	if len(s) > 20 or s.lower() in unwanted: return False
	illegal = ['(', ')', '-', ':'] + ends
	for c in s:
		if c in illegal: return False
	return True
	

def sanitize(s):
	if '(' in s:
		s = s[:s.find('(')] + s[s.find(')')+1:]
	return s

get_movie = lambda s: movies[int(s[4:])]

def get_script(i, char, line):
	global line_num
	if (i, char) not in chars:
		chars[(i, char)] = len(chars)
	uid = 'sw_u%d' % chars[(i, char)]
	mid = 'sw_m%d' % i
	lid = 'sw_L%d' % line_num
	line_num += 1
	return [lid, uid, mid, char, line]

def make(script):
	lid, uid, mid, char, line = script
	s_info = ' +++$+++ '.join(script)
	c_info = ' +++$+++ '.join([uid, char, mid, get_movie(mid), '?', '?'])
	return s_info, c_info


def main():
	global scripts
	for i, url in enumerate(urls):
		if i == 4:
			lines = []
			with open(url, 'r') as f:
				for line in f:
					lines.append(line[:-1])
		else:
			text = rq.get(url).text
			text = text[text.find('<pre>')+5:text.rfind('</pre>')]
			lines = text.split('\n')

		print('Processing %s, %d lines in total' % (movies[i], len(lines)))
		pbar = ProgressBar(widgets=widgets, maxval=len(lines)).start()
		scripts += funcs[i](lines, pbar, i)
		pbar.finish()
	# import pdb; pdb.set_trace()
	sw_lines = open('star_wars_movie_lines.txt', 'w+')
	sw_chars = open('star_wars_movie_characters_metadata.txt', 'w+')
	all_chars = set()
	for sc in scripts:
		s_info, c_info = make(sc)
		sw_lines.write((s_info + '\n').encode('utf-8'))
		all_chars.add(c_info + '\n')
	for c_info in all_chars:
		sw_chars.write(c_info.encode('utf-8'))
	sw_lines.close()
	sw_chars.close()

def process_scripts_1(lines, pbar, i, sep):
	scripts = []
	cur_char, cur_words = None, None
	for lnum, line in enumerate(lines):
		line = sanitize(line)
		line = line.replace('<b>', '')
		line = line.replace('</b>', '')
		line = line.replace('<br>', '')
		line = line.replace('</br>', '')
		if not line or not (cur_char or (sep in line)): continue
		if not cur_char:
			cur_char, cur_words = line.split(sep, 1)
		else:
			cur_words = '%s %s' % (cur_words, line)
		if line[-1] in ends:
			if legal_char(cur_char):
				scripts.append(get_script(i, cur_char, cur_words))
			cur_char, cur_words = None, None
		pbar.update(lnum + 1)
	return scripts

def process_scripts_2(lines, pbar, i):
	scripts = []
	while lines:
		while lines and lines[0][:3] != '<b>':
			lines.pop(0)
		if not lines: break
		char = lines.pop(0)[3:].strip()
		line = lines.pop(0)[4:].strip()
		while lines and lines[0][:3] not in ['', '<b>']:
			line += ' ' + lines.pop(0).strip()
		if legal_char(char):
			scripts.append(get_script(i, char, sanitize(line)))
	return scripts

def get_lines(line):
	ans = []
	while line.count(':') > 1:
		i = line.rfind(':')
		while not line[i] in ends:
			i -= 1
		ans.append(line[i+2:])
		line = line[:i+1]
	ans.append(line)
	ans.reverse()
	return ans



def process_scripts_3(lines, pbar, i):
	scripts = []
	for sub_line in lines:
		for line in get_lines(sub_line):
			sp = line.split(': ', 1)
			if len(sp) < 2: continue
			char, words = sp
			if legal_char(char):
				scripts.append(get_script(i, char, sanitize(words)))
	return scripts

funcs = [
	lambda lines, pbar, i: process_scripts_1(lines, pbar, i, ' : '),
	process_scripts_2,
	lambda lines, pbar, i: process_scripts_1(lines, pbar, i, ': '),
	process_scripts_2,
	process_scripts_3,
]

if __name__ == '__main__':
	main()





