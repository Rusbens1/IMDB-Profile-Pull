from imdbpie import Imdb
from BeautifulSoup import BeautifulSoup
import urllib
import os
import pandas as pd
import sys
import csv, json
import multiprocessing
import time
import httplib, base64
reload(sys)
sys.setdefaultencoding('utf-8')





try:
	os.makedirs('Actor_Faces')
	print 'Creating Actor_Faces folder...'
except OSError, msg:
	print 'Folder already exisits...'
	pass

imdb = Imdb()
imdb = Imdb(anonymize=True)
imdb = Imdb(cache=True)


number_of_actors = 1581675

actor_id_list = range(1581670, number_of_actors)


actor_ids = []
actor_names = []


names = pd.read_excel('Actor_names.xlsx')
n = names.iterrows()
actor_names = []

actor_ids = []

for i in n:
    actor_names.append(i[1][0])

print len(actor_names)
for name in actor_names:
	try:
		actor_name = imdb.search_for_person(str(name))
	except:
		continue
	print 'Converting ' + str(name) + ' to IMDB id:  ' + str(actor_name[0]['imdb_id'].replace('nm',''))
	actor_ids.append(actor_name[0]['imdb_id'].replace('nm',''))
	print 'Total actor count: ' + str(len(actor_ids))

no_pic = []

ids = pd.DataFrame(actor_ids)

ac_ids = {}
ac_ages = {}
ac_names = []
ac_pred_age = []


for id in actor_ids:
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
		actor_born = soup.find('time', {'itemprop' : 'birthDate' } )['datetime']
		try:
			actor_death = soup.find('time', {'itemprop' : 'deathDate' } )['datetime']
			age = int(actor_death[0:4]) - int(actor_born[0:4])
			print str(actor_name) + ' is ' + str(age) + ' years old.'
			ac_ages[str(actor_name)] = int(age)
		except:
			age = 2015 - int(actor_born[0:4])
			print str(actor_name) + ' is ' + str(age) + ' years old.'
			ac_ages[str(actor_name)] = int(age)


		save_image = str(actor_name) + '.jpg'
		print 'Downloaded image for %s ID: %s'  % (actor_name, actor_id)
		print 'Total actor images in collection: ' + str(len(ac_ids))
		ac_ids[str(actor_name)] = int(actor_id.replace('nm',''))
		ac_names.append(actor_name)
		urllib.urlretrieve(actor_picture, 'Actor_Faces/' + save_image)
		print ''
	except TypeError:
		print '----------- ERROR -----------'
		print ''
		print actor_name, ' has no picture.'
		no_pic.append(actor_name)
		print ''
		print no_pic
		print ''
		print 'There are a total of ' + str(len(no_pic)) + ' actors in our collection without pictures.'
		print ''
		continue
textfile = open("/Users/RZB/Desktop/Faces_&_Oxford_Results/ComputerVisionKeys.txt", "r")
lines = textfile.readlines()
pkey = lines[0].split("Primary = '")[1].split("'")[0]
skey = lines[1].split("Secondary = '")[1].split("'")[0]
wait=float(lines[2].split("Buffer_seconds = '")[1].split("'")[0]) #For sleep function paramter
textfile.close()

params = urllib.urlencode({
   # Notes 1/3 for user: Specify your API subscription key
   'subscription-key': skey,
   # Notes 2/3 for user: Specify values for optional parameters or leave as 'All'
   'visualFeatures': 'All',
})


final_ids = []
final_names = []
final_ages = []
final_pred_ages = []
beauty_score = []

pic_err = []

try:

	headers = {
	'Content-type': 'application/octet-stream',
	}
	#Initializing body variable
	body = "" 
	# Replace directory value with your own and make sure you add '/' at the end
	directory = '/Users/RZB/Desktop/Faces_&_Oxford_Results/Actor_Faces/'

	for subdir, dirs, files in os.walk(directory):
		for file in files:
			filename = file
			#print("file is", filename)
			fullpath = directory+filename
			#print("full path is", fullpath)
			#Don't need the following
			#file_ext=os.path.basename(fullpath)
			file_woext=os.path.splitext(os.path.basename(fullpath))[0]
			file_out=file_woext+'.json'
			f = open(fullpath, "rb")
			body = f.read()
			f.close()

			conn = httplib.HTTPSConnection('api.projectoxford.ai')
			conn.request("POST", "/vision/v1/analyses?%s" % params, body, headers)
			response = conn.getresponse()
			data = response.read()
			face = json.loads(data)
			name = str(filename.split('.jpg')[0])
			try:
				age = face['faces'][0]['age']
				print ''
				print 'Oxford API thinks ' + str(name) + ' is ' + str(age) + ' years old.'
				print 'They are actually ' + str(ac_ages[name]) + ' years old.'
				print 'Beauty score = ' + str(int(ac_ages[name]) - int(age)) + '.'
				print ''
				print 'Waiting 3 seconds to avoid exceeding API rate limit...'
				time.sleep(3)
				final_ids.append(str(ac_ids[name]))
				final_names.append(str(name))
				final_ages.append(str(ac_ages[name]))
				final_pred_ages.append(str(age))
				beauty_score.append(str(int(ac_ages[name]) - int(age)))
			except KeyError as e:
				print e

			except IndexError as e:
				print ''
				print 'ERROR: Could not recognize face for ' + str(name)
				print ''
				pic_err.append(name)

			


	        #print int(data['faces']['age'])
	        conn.close()
except Exception as e:
	print(e)
final = pd.DataFrame()
no_picture = pd.DataFrame(no_pic)
pic_error = pd.DataFrame(pic_err)

final['ACTOR_NAMES'] = final_names
final['ACTOR_IDS'] = final_ids
final['ACTOR_AGE'] = final_ages
final['ACTOR_OXFORD_AGE'] = final_pred_ages
final['BEAUTY_SCORE'] = beauty_score

final.to_csv('Final_Results.csv')

no_picture.to_csv('Actors_Without_Pics.csv')
pic_error.to_csv('Actors_With_Picture_Errors.csv')

print ''
print ''
print ''
print 'Check Final_Results.csv for the results!'
print 'Check Actors_Without_Pics.csv for a list of the actors who didnt have IMDB pics.'
print 'Check Actors_With_Picture_Errors for a list of actors whose picture were not recognized by the API.'

