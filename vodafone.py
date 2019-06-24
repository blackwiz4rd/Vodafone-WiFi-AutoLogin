#!/usr/bin/env python

#Vodafone-WiFi
#Automated login for it.portal.vodafone-wifi.com

#Interface
#isVodafone()
#isLogged(history) 
#parseUrl(welcomeUrl, SUCCESS_URL)
#getConfig()
#def getPayload(USERFAKE, PASS, CUSTOMER)
#def connect(USERNAME, PASSWORD, CUSTOMER, SUCCESS_URL)
#def loop_connect(LOOP, USERNAME, PASSWORD, CUSTOMER, SUCCESS_URL)

#dependencies
#remember to install with "sudo pip install requests"
import requests
#remember to install with "sudo pip install configparser"
import configparser
#remember to install with "sudo pip install logging"
import logging
from os.path import dirname, abspath, join
from time import sleep
# for url parsing
from sys import version_info
if version_info[0] < 3:
	from urlparse import parse_qs
	from urlparse import urlparse
	from urllib import urlencode
else:
	from urllib.parse import parse_qs
	from urllib.parse import urlparse
	from urllib.parse import urlencode

ROOT_DIR = dirname(abspath(__file__))

#raised if SSID is not Vodafone or Vodafone extender
class NotConnectedToVodafoneWiFiException(Exception):
	def __init__(self):
		logging.info('You are not connected to Vodafone-WiFi')

#checks if you are connected to a Vodafone Wi-Fi hotspot
def isVodafone(FORCE):
	#a get request on http://192.168.6.1 returns 403 when connected to a Vodafone Wi-Fi
	#other networks may return the same but it would be rare.
	if FORCE:
		return True;

	VODAFONE_IP = ['http://192.168.6.1', 'http://192.168.182.1']
	for IP in VODAFONE_IP:
		try:
			r = requests.get(IP, timeout=10)
			if r.status_code != 403:
				raise NotConnectedToVodafoneWiFiException()
		except requests.ConnectionError as e:
			logging.debug(e)
			raise NotConnectedToVodafoneWiFiException()

	logging.debug('You are connected to Vodafone-WiFi')
	return True

#checks if login was made or not by looking if redirect has been done
def isLogged(history):
	if history:
		raise requests.ConnectionError

	return True
	
def parseUrl(welcomeUrl, SUCCESS_URL):
	o = urlparse(welcomeUrl)
	q = parse_qs(o.query)
	q['res'] = ['login']
	q['userurl'] = [SUCCESS_URL]
	return o._replace(query=urlencode(q, True)).geturl()
	#can cause undefined behaviour depending on welcomeUrl
	# return welcomeUrl[0:47] + 'login' + welcomeUrl[54:172] + '&userurl=' + SUCCESS_URL
	
#reads from file and splits input parameters
def getConfig():
	dict = {}
	try:
		#getting configuration parameters from the .conf file
		c = configparser.ConfigParser()
		c.read(join(ROOT_DIR,'vodafone.conf'))
		dict['username'] = c.get('config', 'username')
		dict['password'] = c.get('config', 'password')
		dict['customer'] = c.get('config', 'customer')
		dict['loop'] = c.get('config', 'loop')
		dict['force'] = c.get('config', 'force')
	except:
		logging.debug("Please re-check the configuration file")
	return dict
	
#sets data for post request
def getPayload(USERFAKE, PASS, CUSTOMER):
	dict = {}
	dict['chooseCountry'] = CUSTOMER + '%2F'
	if CUSTOMER == 'VF_IT' or 'VF_ES':	
		dict['userFake'] = USERFAKE
	else:
		dict['userFake2'] = USERFAKE
	dict['UserName'] = CUSTOMER + '%2F' + USERFAKE
	dict['Password'] = PASS
	dict['rememberMe'] = 'true'
	dict['_rememberMe'] = 'on'

	return dict		

#connects to the network if there's a vodafone captive portal
def connect(FORCE, USERNAME, PASSWORD, CUSTOMER, SUCCESS_URL):
	#later assigned
	hotspotUrl = ''	
	vodafone = False
	logged = False

	vodafone = isVodafone(FORCE)

	#if get request isn't sending response retry in 10 seconds
	while not hotspotUrl and vodafone:
		try:
			r = requests.get(SUCCESS_URL, timeout=10)

			hotspotUrl = r.url
			logged = isLogged(r.history)
		except requests.exceptions.Timeout as e:
			logging.debug(e)
			logging.debug('Retrying get request because of Timeout')
			sleep(10)
		except requests.ConnectionError as e:
			logging.debug(e)
			logging.debug('Retrying get request because of ConnectionError')
			sleep(10)

		#if not logged try login
		if hotspotUrl and vodafone and not logged:
			logging.info('Trying to login...')
		
			#generates login url from welcome url
			#can cause undefined behaviour if captive portal structure is changed
			parsedUrl = parseUrl(hotspotUrl, SUCCESS_URL)

			logging.info('Login parsed url:\n ' + parsedUrl)
			logging.info('Making the payload')

			#Form Data used to login
			payload = getPayload(USERNAME, PASSWORD, CUSTOMER)
	
			#may return ConnectionError if login is successful because then it re-establishes connection
			try:
				r = requests.post(parsedUrl, data=payload, timeout=20)

				logged = isLogged(not r.history)
			except requests.exceptions.Timeout as e:
				logging.debug(e)
			except requests.ConnectionError as e:
				logging.debug(e)
		
		if logged:
			logging.info('>>> Logged!')
		else:
			logging.debug('Login failed, review your username and password in voadafone.conf')

def loop_connect(LOOP, FORCE, USERNAME, PASSWORD, CUSTOMER, SUCCESS_URL):
	while True:
		connect(FORCE, USERNAME, PASSWORD, CUSTOMER, SUCCESS_URL)
		if LOOP:
			break
		sleep(60)

def main():
	#Logging item
	logging.basicConfig(filename=join(ROOT_DIR,'vodafone.log'),format='%(asctime)s %(levelname)s %(message)s',level=logging.INFO, filemode='w')

	#Logging header
	logging.info('#################################################################')
	logging.info('Please, report any error that may occurr at blackwiz4rd@gmail.com')
	logging.info('#################################################################')

	config = {}
	try:
		logging.info('Reading the configuration file (vodafone.conf)')
		config = getConfig()
	except IOError as e:
		logging.debug(e)

	#Getting parameters
	USERNAME = config['username']
	PASSWORD = config['password']
	CUSTOMER = config['customer']
	LOOP = config['loop']
	FORCE = config['force']

	logging.info('Username: ' + USERNAME)
	logging.info('Password: ' + PASSWORD)
	logging.info('Customer: ' + CUSTOMER)
	logging.info('Loop: ' + LOOP)
	logging.info('Force: ' + FORCE)

	#Replace '@' with '%40'
	USERNAME.replace('@','%40')

	SUCCESS_URL = 'http://captive.apple.com/hotspot-detect.html'
	
	loop_connect(LOOP, FORCE, USERNAME, PASSWORD, CUSTOMER, SUCCESS_URL)

if __name__ == "__main__":
	main()
