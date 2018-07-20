import midi
from os import walk, rmdir, remove
from os.path import join, basename
from os import mkdir, makedirs
from time import sleep

TRAINING_PATH = "data/training_bits"

class LyricObject:
	def __init__(self, start_tick, midi_filename, old_pattern):
		self.lyrics = ""
		self.start_tick = start_tick
		self.end_tick = 0
		self.is_closed = False

		self.resolution = old_pattern.resolution
		self.midi_filename = midi_filename
		self.reset_pattern()

	def reset_pattern(self):
		self.pattern = midi.Pattern(resolution=self.resolution)
		self.current_track = ""

	def text_fit(self, text):
		if (len(self.lyrics) + len(text)) <= 140:
			return True
		else:
			return False

	def add_text(self, text):
		self.lyrics += text.lower() #extra text handling!!!

	def end_current_track(self):
		if self.current_track != "":
			eot = midi.EndOfTrackEvent(tick=1)
			self.current_track.append(eot)

	def new_track(self):
		if self.current_track != "":
			self.end_current_track()
		self.current_track = midi.Track()
		self.pattern.append(self.current_track)

	def append_event(self, event):
		self.current_track.append(event)

def second_per_tick(pattern):
	spt = []
	for track in pattern:
		for event in track:
			if type(event) == midi.SetTempoEvent:
				spt.append((event.get_mpqn() / pattern.resolution * 1.0) / 1000000)
	if len(list(set(spt))) > 1 or len == 0:
		print("SECOND PER TICK CALCULATION IS WRONG!!!")
		return 0
	try:
		return spt[0]
	except:
		return 0

def make_lyric_objects_seconds_long(seconds_long, lyric_objects, pattern):
	spt = second_per_tick(pattern)
	for lyric_object in lyric_objects:
		lyric_object.end_tick = lyric_object.start_tick + round(seconds_long / spt)

def ticks_per_beat(pattern):
	return pattern.resolution

#assuming 4/4 time schedule
def ticks_per_bar(pattern):
	return ticks_per_beat(pattern) * 4

def make_lyric_objects_bars_long(bars_long, lyric_objects, pattern):
	tpb = ticks_per_bar(pattern)
	for lyric_object in lyric_objects:
		lyric_object.end_tick = lyric_object.start_tick + (bars_long * tpb)


def make_lyric_bits_for_song(midi_filename):
	try:
		pattern = midi.read_midifile(midi_filename)
	except:
		print("THATS ONE BAD MIDI!::: ", midi_filename)
		return 0

	if len(pattern) <= 1:
		print("skipping, because \"" + midi_filename + "\" contains only one track")
		return 0

	pattern.make_ticks_abs()

	clean_midi_filename = basename(midi_filename)

	training_path = join(TRAINING_PATH, clean_midi_filename[:-4]) + "/"

	lyric_objects = []
	for track in pattern:
		start_new_line = True
		line = ""
		newest = 0

		for event in track:
			if type(event) == midi.LyricsEvent:
				line += event.text #add words to sentence
				if start_new_line: #create a new lyric_object at the start of a new sentence
					lyric_objects.append(LyricObject(event.tick, clean_midi_filename, pattern))
					start_new_line = False

				if event.text == '\r': #maybe also search for '\n'?
					if line == "\r" or line == "song title \r" or line  == "artist \r" or line == "copyright \r": #keeps line out of the lyric_bits
						line = ""
						if lyric_objects[-1].lyrics == "":
							del lyric_objects[-1]
							start_new_line = True
						continue
					for lyric_object in lyric_objects:
						if not lyric_object.is_closed: #add the sentence to every lyric_object that isn't closed and where it fits.
							if lyric_object.text_fit(line):
								lyric_object.add_text(line)
								lyric_object.end_tick = event.tick
							else:
								lyric_object.is_closed = True

					line = ""
					start_new_line = True


	if len(lyric_objects) > 0:
		print("+++ lyrics were found for", clean_midi_filename)

		if second_per_tick(pattern) == 0:
			return 0
		
		try:
			makedirs(training_path)
		except:
			pass

		make_lyric_objects_seconds_long(60, lyric_objects, pattern)
		# make_lyric_objects_bars_long(16, lyric_objects, pattern)


		if save_lyric_bits(training_path, lyric_objects) == 0:
			print("No lyric bits left, so skipping.")
			#remove lyric bits file here?
			remove(training_path + lyric_objects[0].midi_filename + ".lyric_bits")
			rmdir(training_path)
			return 0

		correct_tracks = 0
		for i in range(0, len(pattern)):
			# print("\n+++ working on track", i+1)
			correct_tracks += add_audio_bits(pattern, lyric_objects, i, training_path, midi_filename)
			remove_audio_bits_from(lyric_objects)
		if correct_tracks == 0:
			print("all instruments were incorrect, so skipping.")
			#remove lyric bits file here?
			remove(training_path + lyric_objects[0].midi_filename + ".lyric_bits")
			rmdir(training_path)

	else:
		print("--- No lyrics were found in", clean_midi_filename)

def remove_audio_bits_from(lyric_objects):
	for lyric_object in lyric_objects:
		lyric_object.reset_pattern()

#write the lyric_bits to file
def save_lyric_bits(training_path, lyric_objects):
	skipped = 0
	with open(training_path + lyric_objects[0].midi_filename + ".lyric_bits", 'w') as new_file:
		for i, lyric_object in enumerate(lyric_objects):
			if lyric_object.lyrics == "":
				skipped +=1
				continue #skip empty objects
			try:
				new_file.write(lyric_object.lyrics)
				new_file.write("TICK_RANGE:" + str(lyric_object.start_tick) + "--" + str(lyric_object.end_tick) + "_" + str(i) + '\n')
			except:
				skipped +=1

	print("+++ ", len(lyric_objects) - skipped, "lyric_objects were created in \"" + training_path + lyric_object.midi_filename + ".lyric_bits\".")
	return len(lyric_objects) - skipped

def get_instruments_from_track(track):
	for event in track:
		if type(event) == midi.ProgramChangeEvent:
			if len(event.data) == 1:
				print(event)
				return event.data[0]
			else:
				# print(">>>>>>>>There is something with this instrument<<<<<<<<")
				# print("Instrument: " + event.data[0])
				pass
	return 0 #zero is nothing right?
	

def add_audio_bits(pattern, lyric_objects, track_n, training_path, midi_filename):
	pattern_orig = midi.read_midifile(midi_filename)
	i = track_n
	for track, track_orig in zip(pattern, pattern_orig):
		if i == 0:
			instrument_id = get_instruments_from_track(track)
			if instrument_id < 1 or instrument_id > 32:
				print("=== this instrument_id ", str(instrument_id), " is not a melody instrument.")
				print("====Skipping this track.")
				return 0
			for lyric_object in lyric_objects: 
				lyric_object.new_track()
			for event, event_orig in zip(track, track_orig):
				for lyric_object in lyric_objects:
					if event.tick >= lyric_object.start_tick and event.tick <= lyric_object.end_tick:
						# print(lyric_object.start_tick, event.tick, lyric_object.end_tick)
						if event_orig.tick == 0:
							event_orig.tick == 1
						lyric_object.append_event(event_orig)
		i-=1

	for lyric_object in lyric_objects:
		lyric_object.end_current_track()
	save_audio_bits(join(training_path, str(track_n)) + "/", lyric_objects)
	return 1

def save_audio_bits(training_path, lyric_objects):
	try:
		makedirs(training_path)
		# print("+++ +++ training_path created .")
	except:
		# print("+++ --- training_path already exists.")
		pass

	for i, lyric_object in enumerate(lyric_objects):
		midi.write_midifile(training_path + lyric_object.midi_filename + str(i) + ".mid", lyric_object.pattern)


def retrieve_files(path, file_extension):
	f = []
	for root, dirs, files in walk(path):
		for file in files:
			if file.lower().endswith(file_extension):
				f.append(join(root, file))
	return f

def retrieve_midi_files(path):
	return retrieve_files(path, ".mid")

def retrieve_lyric_bits_files(path):
	return retrieve_files(path, ".lyric_bits")

def make_lyric_bits(midi_path):
	midi_files = retrieve_midi_files(midi_path)
	for midi_filename in midi_files:
		print("\nworking on: " + midi_filename)
		make_lyric_bits_for_song(midi_filename)
	print("all the training_bits have been created.")

#####examples:
## create examples of an entire folder
# midi_path = "input/midis/130000_Pop_Rock_Classical_Videogame_EDM_MIDI_Archive[6_19_15]/G/G/"
# make_lyric_bits(midi_path)

#####
## create examples for one specific MIDI file
# make_lyric_bits_for_song("garbage-androgyny.mid")
# midi_filename = "input/midis/130000_Pop_Rock_Classical_Videogame_EDM_MIDI_Archive[6_19_15]/G/G/garbage-androgyny.mid"

