import os
import sys
from . import database

def add(path):
	with open(path) as f:
		keywords = f.readline().strip().decode('utf8').split()
		content = f.read().strip().decode('utf8')
	if len(keywords) == 0:
		print('Error. The first line of %s is keywords seperated by whitespace.\nThe number of keywords should not less than one.' % path)
	elif content == '':
		print("Error. The note's content is in the %.\nThe content should not be empyt." % path) 	
	else:
		database.insert_note(keywords, content)
	return

def get(keywords):
	notes = database.get_notes_by_keys(keywords)
	if not notes:
		print('Error. There are no notes with keywords "%s"' % ' '.join(keywords))
	else:
		for note in notes:
			print("## %s" % note[1])
			print(note[2]+'\n')
	return

def change(path):
	with open(path) as f:
		keywords = f.readline().strip().decode('utf8').split()
		content = f.read().strip().decode('utf8')
	database.change(keywords, content)
	return

def delete(keywords, recursive=False):
	database.delete(keywords, recursive)	
	return

def scan():
	key2num = database.scan_notes()
	key2num.sort(key=lambda x: x[1], reverse=True)
	note_num = sum(x[1] for x in key2num)
	print("%d keywords    %d notes\n" %(len(key2num), note_num))
	print('numbers    keywords')
	for key, num in key2num:
		print('% 7d    %s' % (num, key))

