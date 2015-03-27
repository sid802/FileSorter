#-*- encoding: utf-8 -*-

#######################################################################
#
#			Takes a folder, and sorts all the TV show
#			in it based on their name.
#
#			For example, Caste S01E03 gets moved the
#			a folder named 'Castle' and sub folder 'Castle - Season 1'
#
#			This script works TV Show from with two different formats:
#			1) TVSHOW + S(season) + E(episode) (CastleS01E03)
#			2) TVSHOW + seasonXepisode (Caste 1x03)
#
#
#
#           By Sid :)
#######################################################################



import re, os, shutil, time

def parse_folder(folder_path):
	files_in_folder = [file for file in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, file))]
	

	#Patterns to understand file:

	#example: Caste.S01E06
	firstPattern = re.compile(r'(?P<show>.*?)S(?P<season>\d{2})E(?P<episode>\d{2})', re.IGNORECASE)

	#example: Caste 1x06
	secondPattern = re.compile(r'(?P<show>.*?)(?P<season>\d{1,2})x(?P<episode>\d{1,2})', re.IGNORECASE)

	for file in files_in_folder:

		#attempt first pattern
		match = firstPattern.search(file)

		#if failed, attempt second pattern
		if not match:
			match = secondPattern.search(file)

		#if match is successfull, sort the file
		if match:

			show = match.group('show')
			season = int(match.group('season'))
			episode = match.group('episode')

			#Filter show name. Turns 'American.Idol.' into 'American Idol'
			show_filtered = filter_show_name(show)

			#creates the target folder by adding show name and season to current folder
			target_folder = os.path.join(os.path.join(folder_path, show_filtered), "{show} - Season {season}".format(show = show_filtered, season = season))

			source_file = os.path.join(folder_path, file)

			move_to_folder(target_folder, source_file)

def filter_show_name(show_name):
	return re.sub(r'\s+', ' ', re.sub(r'[\W_]', r' ', show_name)).strip()

def move_to_folder(target_folder, source_file):
	''' If target folder doesnt exist, creates it and then moves the source file to the target folder '''

	if not os.path.exists(target_folder):
		os.makedirs(target_folder)

	file_name = os.path.basename(source_file)

	dst = os.path.join(target_folder, file_name)

	try:
		shutil.move(source_file, dst)
	except IOError, e:
		print "Couldn't put {0} in {1}. Error: {2}".format(source_file, target_folder, e)


if __name__ == '__main__':
	folder_path = raw_input("Enter folder of videos:\n")
	while not os.path.exists:
		folder_path = raw_input("Enter folder of videos:\n")
	start = time.time()
	parse_folder(folder_path)
	print 'This took {0} seconds'.format(time.time() - start)