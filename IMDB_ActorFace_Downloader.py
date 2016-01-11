# Hey team, here is the script we need to download every actor's 
# profile photo from IMDB.com to prep for our analysis.
# Since there are over 6 million actors I suggest we divide them up
# on our different machines to be more efficient and save time.
#
# Directions:
# 	1. Install imdbpie:
#		'pip install imdbpie' or 'sudo easy_install imdbpie'
#	2. Move this file to desktop, go to desktop
#	   directory in Terminal/ CommandPrompt:
#		'cd desktop'
#	3. Edit the number of actors you are pulling, or edit the range of IDs
#		Do this by changing the 'number_of_actors' variable, and/or the first number 
#		in the range(*)
#	3. Run the script:
#		'python IMBD_ActorFace_Downloader.py'
#
#		You should see all of the photos downloading to a new folder 
#		called 'Actor_Faces' saved under each respective IMDB ID.



from imdbpie import Imdb
from BeautifulSoup import BeautifulSoup
import urllib
import os

try:
	os.makedirs('Actor_Faces')
	print 'Creating Actor_Faces folder...'
except OSError, msg:
	print 'Folder already exisits...'
	pass

imdb = Imdb()
imdb = Imdb(anonymize=True)
imdb = Imdb(cache=True)


number_of_actors = 1000

actor_id_list = range(1, number_of_actors)

for id in actor_id_list:
	print '-----------STARTING DOWNLOAD-----------'
	print ''
	try:	
		if len(str(id)) == 1:
			actor_id = 'nm' + '000000' + str(id)
		elif len(str(id)) == 2:
			actor_id = 'nm' + '00000' + str(id)
		elif len(str(id)) == 3:
			actor_id = 'nm' + '0000' + str(id)
		elif len(str(id)) == 4:
			actor_id = 'nm' + '000' + str(id)
		elif len(str(id)) == 5:
			actor_id = 'nm' + '00' + str(id)
		elif len(str(id)) == 6:
			actor_id = 'nm' + '0' + str(id)
		elif len(str(id)) == 7:
			actor_id = 'nm' + str(id)
		else:
			print 'Check ID length'
		try:
			actor_name = imdb.get_person_by_id(actor_id).name
		except:
			print '----------- ERROR -----------'
			print ''
			print actor_id, ' is not a valid ID.'
			print ''
			continue 
		save_image = str(actor_id) + '.jpg'
		actor_url = 'http://www.imdb.com/name/' + str(actor_id)
		actor_imdb_page = urllib.urlopen(actor_url)
		soup = BeautifulSoup(actor_imdb_page.read())
		actor_picture = soup.find('img', {'id' : 'name-poster' } )['src']
		save_image = str(actor_id) + '.jpg'
		print 'Downloaded image for %s ID: %s'  % (actor_name, actor_id)
		urllib.urlretrieve(actor_picture, 'Actor_Faces/' + save_image)
		print ''
	except TypeError:
		print '----------- ERROR -----------'
		print ''
		print actor_name, ' has no picture.'
		print ''
		continue








