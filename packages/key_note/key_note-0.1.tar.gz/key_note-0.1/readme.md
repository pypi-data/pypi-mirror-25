# Note
This is a tool for writing, restoring and retriving notes in command line. Here are some examples of command:


1. **note add/a note\_file**   
   add a note. the note file's first line is keywords seperated by whitespaces, the rest of lines are content.
2. **note delete/d [-r] keyword1 [keyword2...]**  
   delete the notes with the keywords
3. **note get/g keyword0 [keyword1 ... keywordN]**  
   print notes about the keyword(s)
4. **note change/c note\_file**  
   for the note with keywords in note\_file, the note in database will be changed.  
5. **note scan/s**  
	dispaly the information of the notes which have stored.  
6. **note -h**  
   display help infomation

# Implementation
For each note, it has two components which are keyword(s) and content.
In order to save the notes, a database is created. The database has two tables. One table is a dict, whose keys and values are the keywords and the note ids. Each id links to a note. The other table has three columns: the notes' ids, the keywords which the notes linked to, the note contents.

```
create table keywords (
  keyword string primary key not null,
  ids string not null
);

create table notes (
  id integer primary key autoincrement,
  keywords string not null,
  content string not null
);
```

# to do
1. get notes with bool filter
2. suppert a gui
