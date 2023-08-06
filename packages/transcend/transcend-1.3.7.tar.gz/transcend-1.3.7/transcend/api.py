import requests
import os, sys

credentials_file = './credentials.py'

def set_credentials(fil):
	credentials_file = fil

def make_request(credentials_file, endpoint, resource_server = "https://transcend.io"):
	# Ensure credentials file exists
	if not os.path.exists(credentials_file):
		return("Credentials file does not exist")
	
	#  Read in credentials
	folder, fil = os.path.split(credentials_file)
	sys.path.insert(0, folder)
	credentials = __import__(os.path.splitext(fil)[0])
			
	# the url to make the api request to
	request_url = "%s/api/%s?appId=%s" % (resource_server, endpoint, credentials.CLIENT_ID)
	
	# the header used for authentication of the request
	headers = {"Authorization":"Bearer %s" % credentials.ACCESS_TOKEN}
	
	# send the request
	r = requests.get(request_url, headers = headers)
	
	# Parse the response
	if r.status_code == 200:
		# successful response
		return r.json()
	else:
		print r.content 

def request(endpoint):
	return make_request(credentials_file, endpoint)