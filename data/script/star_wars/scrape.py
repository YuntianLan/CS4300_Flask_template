#coding=utf-8

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
	'The Last Jedi.txt'
]

movies = [
	'Star Wars: Episode 1: The Phantom Menace',
	'Star Wars: Episode 2: Attack of the Clones',
	'Star Wars: Episode 3: Revenge of the Sith',
	'Star Wars: Episode 7: The Force Awakens',
	'Star Wars: Episode 8: The Last Jedi',
]

ends = ['.', '?', '!']
unwanted = ['title card', 'the end', 'star wars']

line_num = 0
chars = {}
scripts = []

widgets = ['Progress: ',Percentage(), ' ', Bar('#'),' ', Timer(),
		   ' ', ETA(), ' ', FileTransferSpeed()]

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

def process_scripts_3(lines, pbar, i):
	scripts = []
	for line in lines:
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





