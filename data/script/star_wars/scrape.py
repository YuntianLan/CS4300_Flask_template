import requests as rq
from progressbar import *

urls = [
	# The Phantom Menace
	'https://www.imsdb.com/scripts/Star-Wars-The-Phantom-Menace.html',
	# Attack of the Clones
	'https://www.imsdb.com/scripts/Star-Wars-Attack-of-the-Clones.html',
	# Revenge of the Sith
	'https://www.imsdb.com/scripts/Star-Wars-Revenge-of-the-Sith.html',
	# The Force Awakens
	'https://www.imsdb.com/scripts/Star-Wars-The-Force-Awakens.html',
	# The Last Jedi TBF
]

movies = [
	'Star Wars: Episode 1: The Phantom Menace',
	'Star Wars: Episode 2: Attack of the Clones',
	'Star Wars: Episode 3: Revenge of the Sith',
	'Star Wars: Episode 7: The Force Awakens',
]

ends = ['.', '?', '!']
unwanted = ['TITLE CARD']

line_num = 0
chars = {}
scripts = []

widgets = ['Progress: ',Percentage(), ' ', Bar('#'),' ', Timer(),
		   ' ', ETA(), ' ', FileTransferSpeed()]

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
	for i, url in enumerate(urls):
		text = rq.get(url).text
		text = text[text.find('<pre>')+5:text.rfind('</pre>')]
		import pdb; pdb.set_trace()
		# text = text.replace('<b>', '')
		# text = text.replace('</b>', '')
		text = text.replace('<br>', '')
		text = text.replace('</br>', '')
		lines = text.split('\n')

		print('Processing %s, %d lines in total' % (movies[i], len(lines)))
		pbar = ProgressBar(widgets=widgets, maxval=len(lines)).start()
		############################################################
		for lnum, line in enumerate(lines):
			# print(i, lnum, line)
			line = sanitize(line)
			if not (cur_char or (' : ' in line)): continue
			if not cur_char:
				cur_char, cur_words = line.split(' : ', 1)
			else:
				cur_words = '%s %s' % (cur_words, line)
			if line[-1] in ends:
				scripts.append(get_script(i, cur_char, cur_words))
				if cur_char in unwanted: scripts.pop()
				cur_char, cur_words = None, None
			pbar.update(lnum + 1)
		############################################################
		pbar.finish()

	sw_lines = open('star_wars_movie_lines.txt', 'w+')
	sw_chars = open('star_wars_movie_characters_metadata.txt', 'w+')
	all_chars = set()
	for sc in scripts:
		s_info, c_info = make(sc)
		sw_lines.write(s_info + '\n')
		all_chars.add(c_info + '\n')
	for c_info in all_chars:
		sw_chars.write(c_info)
	sw_lines.close()
	sw_chars.close()

def process_scripts_1(lines, pbar, sep):
	scripts = []
	cur_char, cur_words = None, None
	for lnum, line in enumerate(lines):
		line = sanitize(line)
		if not (cur_char or (sep in line)): continue
		if not cur_char:
			cur_char, cur_words = line.split(sep, 1)
		else:
			cur_words = '%s %s' % (cur_words, line)
		if line[-1] in ends:
			scripts.append(get_script(i, cur_char, cur_words))
			if cur_char in unwanted: scripts.pop()
			cur_char, cur_words = None, None
		pbar.update(lnum + 1)
	return scripts

def process_scripts_2(lines, pbar):
	scripts = []
	

funcs = [
	lambda lines, pbar: process_scripts_1(lines, pbar, ' : '),
	process_scripts_2,

]

if __name__ == '__main__':
	main()





