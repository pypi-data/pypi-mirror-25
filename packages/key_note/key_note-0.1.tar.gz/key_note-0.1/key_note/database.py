import os
import sys
import sqlite3
import pdb

DATABASE = os.path.expanduser('~/.key_note')
if not os.path.exists(DATABASE):
	os.mkdir(DATABASE)
DATABASE = os.path.join(DATABASE, 'note.db')
if os.path.exists(DATABASE):
	CONNECT = sqlite3.connect(DATABASE)
else:
	CONNECT = sqlite3.connect(DATABASE)
	CONNECT.cursor().executescript('''
create table keywords (
  keyword string primary key not null,
  ids string not null
);
create table notes (
  id integer primary key,
  keywords string not null,
  content string not null
);''')

def after_run():
	CONNECT.close()
	return

def insert_note(keywords, content):
	keywords.sort()
	keywords_s = ' '.join(keywords)
	cursor = CONNECT.execute('select id, keywords from notes')
	id_keywords = cursor.fetchall()
	pre_ids = [x[0] for x in id_keywords]
	pre_keywords = [x[1] for x in id_keywords]

	i = -1
	for j,kk in enumerate(pre_keywords): 
		if kk == keywords_s:
			i = j
			break
	if i != -1:
		cursor = CONNECT.execute('select content from notes where id = ?', (pre_ids[i],))
		content = content + '\n' + cursor.fetchall()[0][0]
		CONNECT.execute('UPDATE notes set content = ? where id = ?', (content, pre_ids[i]))
		print("warning: the note with the keywords is already stored. The content is added to it")
	else: 
		not_in = set(range(len(pre_ids))) - set(pre_ids)
		cur_id = not_in.pop() if not_in else len(pre_ids)
		CONNECT.execute('insert into notes (id, keywords, content) values (?, ?, ?)', (cur_id, keywords_s, content))
		for keyword in keywords:
			cursor = CONNECT.execute('select ids from keywords where keyword=?', (keyword,))
			ids = cursor.fetchall()
			if ids:
				ids = ids[0][0]
				ids = ids + str(cur_id) + '_'	
				CONNECT.execute('update keywords set ids = ? where keyword = ?', (ids, keyword))
			else: 
				ids = str(cur_id)+"_"
				CONNECT.execute('insert into keywords (keyword, ids) values (?, ?)', (keyword, ids))  
	CONNECT.commit()
	return 


def get_notes_by_ids(ids):
	notes = []
	for i in ids:
		cursor = CONNECT.execute('select id, keywords, content from notes where id=?', (i,))
		notes.append(cursor.fetchall()[0])
	return notes
		
def get_notes_by_keys(keywords):
	sets = []	
	for keyword in keywords:
		cursor = CONNECT.execute('select ids from keywords where keyword=?', (keyword,))
		ids = cursor.fetchall()
		if ids:
			ids = ids[0][0].strip('_').split('_')
			sets.append(set(ids))
		else:
			return []
	if sets:
		set0 = sets[0]
		for s in sets[1:]:
			set0.intersection_update(s)
		return get_notes_by_ids(set0)
	else:
		return []

def change(keywords, content):
	# keywords: non-empty list; content: a non-empty string after striped	
	notes = get_notes_by_keys(keywords)
	if len(notes) == 0:
		insert_note(keywords, content)
		print('Warning: the notes had no note with "%s" keywords. You just added the note.' % ' '.join(keywords)) 
	elif len(notes) == 1:
		CONNECT.execute('update notes set content = ? where id = ?', (content, notes[0][0]))
		CONNECT.commit()
	else:
		insert_note(keywords, content)
		print('Warning: the notes had %d note with "%s" keywords. You just added the note.' % (len(notes), ' '.join(keywords))) 
	return

def _delete(one_note):
	id, keywords = one_note[0:2]
	CONNECT.execute('delete from notes where id = ?', (str(id),))
	for keyword in keywords.split():
		cursor = CONNECT.execute('select ids from keywords where keyword=?', (keyword,))
		ids = cursor.fetchall()[0][0]
		ids = ids.strip('_').split('_')
		index = ids.index(str(id))
		ids.pop(index)
		if ids:
			ids = '_'.join(ids) + '_'
			CONNECT.execute('update keywords set ids = ? where keyword = ?', (ids, keyword))
		else: 
			CONNECT.execute('delete from keywords where keyword = ?', (keyword,))
	CONNECT.commit()
	return
	
def delete(keywords, recursive=False):
	notes = get_notes_by_keys(keywords)
	if len(notes) == 0:
		print('Warning: the notes had no note with "%s" keywords. You delete nothing.' % ' '.join(keywords)) 
	elif len(notes) == 1:
		_delete(notes[0])
	else:
		if recursive:
			for note in notes:
				_delete(note)
		else:
			print('Error: there are %d notes with "%s". You can delete them by recursive mood.' % (len(notes), ' '.join(keywords)))	
	return

def scan_notes():
	key_ids = CONNECT.execute('select keyword, ids from keywords').fetchall()
	result = []
	for key, ids in key_ids:
		n = len(ids.strip('_').split('_'))
		result.append((key, n))	
	return result
