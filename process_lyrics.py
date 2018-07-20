from string import punctuation
import re

#replaces any number with the number 6.
def replace_numbers(lyrics):
	lyrics = re.sub('\d', '6', lyrics)
	return lyrics

def clean_lyrics(lyrics, song_per_line):
	# punctuation string: '!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~'
	punctuation_regex = re.compile('[{}]'.format(punctuation.replace("'", "")))
	lyrics = punctuation_regex.sub(' ', lyrics)
	lyrics = re.sub(r"''+", " ", lyrics)
	lyrics = re.sub(r"'", "", lyrics)
	lyrics = re.sub(r"\\uFFFD", '_', lyrics) #replaces unicode unknown characters with underscores
	lyrics = re.sub('\x00', "", lyrics) #remove NUL bytes
	lyrics = lyrics.lower()
	lyrics = re.sub(r"\\r", ' ', lyrics) #remove line ending symbols
	lyrics = re.sub(r"\\n", ' ', lyrics) #remove line ending symbols
	lyrics = re.sub(r"[^a-z]_+[^a-z]", ' ', lyrics) #remove all underscores not preceded by a letter
	lyrics = re.sub(r"\\", ' ', lyrics) #remove backslashes
	lyrics = re.sub('  +', ' ', lyrics) #remove surplus spaces

	lyrics = replace_numbers(lyrics)

	lyrics = re.sub('\r', '\n', lyrics) #to be on the safe side of things.
	lyrics = re.sub('\n +', '\n', lyrics)
	lyrics = re.sub("\n\n+", '\n', lyrics) #remove empty lines
	if song_per_line:
		# lyrics = re.sub('\n', ' ', lyrics) #remove all brakes between lines within one song
		lyrics = re.sub('\n', '.\n', lyrics) #replace all breaks with breaks with dots
		lyrics = re.sub('  +', ' ', lyrics) #remove surplus spaces
		lyrics = re.sub(' \.', '.', lyrics) #remove surplus spaces
	
	return lyrics.strip() #remove spare start end spaces

#writes the cleaned lyrics to a new file, saving the first and last line number
#of each song in the new file in the index_file, so it can be retrieved later
##### song per line 
def clean_kaggle_songlyrics(kaggle_lyrics, new_file, index_file, song_per_line=False):
	with open(new_file, 'w') as new:
		with open(index_file, 'w') as new_index:
			with open(kaggle_lyrics, 'r') as kaggle:
				kaggle.readline() #skip first line
				data = kaggle.read()
				lines = data.split("\n\n\"")
				index_pointer = 0
				for line in lines:
					try:
						info, lyrics = line.split(".html,\"")
					except:
						break
					lyrics = re.sub("\s*\n\s*\n", '\n', lyrics) #remove empty lines between verses
					lyrics = clean_lyrics(lyrics, song_per_line)
					new.write(lyrics+'\n')
					
					song_id = (info[-8:])
					artist, song_name = info.split(',')[:2]
					artist = re.sub(r'\n', '', artist)
					song_name = re.sub('\"', '', song_name)

					new_index.write(song_id + ';' + str(index_pointer)+ ';' + str(index_pointer + len(lyrics.split('\n'))) +  ';' + artist + ';' + song_name + '\n')
					index_pointer += len(lyrics.split('\n'))

#clean one single lyrics file
def clean_txt(txt_file, new_file = ""):
	with open(txt_file, 'r') as raw:
		lyrics = raw.read()
		lyrics = clean_lyrics(lyrics)
		if new_file != "":
			with open(new_file, 'w') as new:
				new.write(lyrics+'\n')
		else:
			return lyrics