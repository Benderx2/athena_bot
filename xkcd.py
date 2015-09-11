import os
import sys
import socket
import threading
import ast
import signal
import types
import urllib2
import json
import difflib
import irc
import variables

from subprocess import PIPE, Popen

comics_titles = [""]

total_current_titles = 0
latest_index_num = 0

xkcd_url = "http://xkcd.com/"
json_fil = "/info.0.json"
def load_comics():
	global comics_titles, total_current_titles, latest_index_num
	try:
		latest_index_json = json.loads(urllib2.urlopen(xkcd_url + json_fil).read().replace("\n", "").replace("\r", "").replace("'", ""))
		latest_index_num = 0
		latest_index_num = int(latest_index_json['num'])
	except:
		return "Error fetching comic's latest index. Sorry."
	i = 0
	i += 1
	if os.path.isfile("xkcdtitles.txt") == True:
		# read it all!
		comics_titles = open("xkcdtitles.txt", 'rb').read().split("\n")
		comics_titles.pop()
		total_current_titles = len(comics_titles)
		i = len(comics_titles)
	print "Total comics in database: " + str(i) + "\nTotal Comics Online: " + str(latest_index_num)
	while i <= latest_index_num:
		try:
			json_data = urllib2.urlopen(xkcd_url + str(i) + json_fil).read().replace("\n", "").replace("\r", "").replace("'", "")
			topic_title = json.loads(json_data)['title']
			print topic_title
		except:
			exception = sys.exc_info()[0]
			if exception == KeyboardInterrupt:
				quit("User Quit")
			topic_title = "404"
		if topic_title == "":
				return "Error parsing JSON. Sorry."
		else:
				comics_titles.append(topic_title)
		i += 1
	return "Success"

def search_xkcd(comic_string):
	global comics_titles, total_current_titles, latest_index_num
	load_comics()
	# grab all comic titles and their image URLs
	# first get the latest comic index
	
	# now let's find the most matching string
	try:
		comic_title = difflib.get_close_matches(comic_string, comics_titles, 1)[0]	
		comic_index = 0
		comic_index = comics_titles.index(comic_title)
	except:
		irc.send_msg( str(sys.exc_info()), variables.head_user)
		return "Error. Unable to find comic title"
	target = open("xkcdtitles.txt", 'a')
	i = total_current_titles+1
	while i < len(comics_titles):
		target.write("%s\n" % comics_titles[i].encode('ascii', errors='backslashreplace').replace("\n", "").replace("\r", ""))
		i += 1
	return xkcd_url + str(comic_index+1)
