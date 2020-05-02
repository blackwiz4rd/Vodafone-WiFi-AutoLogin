#!/usr/bin/env python

#Vodafone-WiFi
#Automated login for it.portal.vodafone-wifi.com

import requests
import configparser
import logging
import argparse
from os.path import dirname, abspath, join
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
#TODO: check if there is a better way
def isVodafone(FORCE, TIMEOUT):
	#a get request on http://192.168.6.1 returns 403 when connected to a Vodafone Wi-Fi
	#other networks may return the same but it would be rare.
	if FORCE:
		return True;

	VODAFONE_IP = ['http://192.168.6.1', 'http://192.168.182.1']
	isVodafone = False

	for IP in VODAFONE_IP:
		try:
			r = requests.get(IP, timeout=TIMEOUT)
			isVodafone = r.status_code != 403
		except requests.ConnectionError as e:
			logging.debug(e)

	if not isVodafone:
		raise NotConnectedToVodafoneWiFiException()
	logging.debug('You are connected to Vodafone-WiFi')
	return isVodafone

#checks if login was made or not by looking if redirect has been done
#TODO: check if it works
def isLogged(history):
	if history:
		raise requests.ConnectionError

	return True

def parseUrl(welcomeUrl, SUCCESS_URL):
	o = urlparse(welcomeUrl)
	q = parse_qs(o.query)
	q['res'] = ['login']
	q['userurl'] = [SUCCESS_URL]
	return o._replace(query=urlencode(q, True)).geturl().replace("%3A",":").replace("%2F","/")
	#can cause undefined behaviour depending on welcomeUrl
	# return welcomeUrl[0:47] + 'login' + welcomeUrl[54:172] + '&userurl=' + SUCCESS_URL

#reads from file and splits input parameters
def getConfig():
	dict = {}
	# try:
		#getting configuration parameters from the .conf file
	c = configparser.RawConfigParser()
	c.read(join(ROOT_DIR,'vodafone.conf'))
	dict['username'] = c.get('config', 'username')
	dict['password'] = c.get('config', 'password')
	dict['customer'] = c.get('config', 'customer')
	dict['force'] = c.get('config', 'force')
	dict['success_url'] = c.get('config', 'success_url')
	dict['timeout'] = c.get('config', 'timeout')
	if c.has_option('autogen', 'vodafone_url'):
		dict['vodafone_url'] = c.get('autogen', 'vodafone_url')
	# except:
	# 	logging.debug("Please re-check the configuration file")
	return dict

# set url
def setConfig(VODAFONE_URL, SKIP_VODAFONE_URL):
	c = configparser.RawConfigParser()
	if not SKIP_VODAFONE_URL:
		c.read(join(ROOT_DIR,'vodafone.conf'))
	if not c.has_section('autogen'):
		c.add_section('autogen')
	c.set('autogen', 'vodafone_url', VODAFONE_URL)
	if not SKIP_VODAFONE_URL:
		with open(join(ROOT_DIR,'vodafone.conf'), 'w') as configfile:
			c.write(configfile)
	else:
		with open(join(ROOT_DIR,'vodafone.conf'), 'a') as configfile:
			c.write(configfile)

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

def getVodafoneUrl(SUCCESS_URL, TIMEOUT):
	hotspotUrl = ''
	logged = False

	try:
		r = requests.get(SUCCESS_URL, timeout=TIMEOUT)

		hotspotUrl = r.url
		logged = isLogged(r.history)
	except requests.exceptions.Timeout as e:
		logging.debug(e)
		logging.debug('Retrying get request because of Timeout')
	except requests.ConnectionError as e:
		logging.debug(e)
		logging.debug('Retrying get request because of ConnectionError')

	return hotspotUrl, logged

#connects to the network if there's a vodafone captive portal
def connect(FORCE, USERNAME, PASSWORD, CUSTOMER, SUCCESS_URL, VODAFONE_URL, TIMEOUT):
	logged = False

	logging.info('Trying to login...')

	#generates login url from welcome url
	#can cause undefined behaviour if captive portal structure is changed
	parsedUrl = parseUrl(VODAFONE_URL, SUCCESS_URL)

	logging.info('Login parsed url:\n ' + parsedUrl)
	logging.info('Making the payload')

	#Form Data used to login
	payload = getPayload(USERNAME, PASSWORD, CUSTOMER)

	#may return ConnectionError if login is successful because then it re-establishes connection
	try:
		r = requests.post(parsedUrl, data=payload, timeout=TIMEOUT)

		logged = isLogged(not r.history)
	except requests.exceptions.Timeout as e:
		logging.debug(e)
	except requests.ConnectionError as e:
		logging.debug(e)

	if logged:
		logging.info('>>> Logged!')
	else:
		logging.debug('Login failed, review your username and password in vodafone.conf')
	return logged

def main():
	#Logging item
	logging.basicConfig(filename=join(ROOT_DIR,'vodafone.log'),format='%(asctime)s %(levelname)s %(message)s',level=logging.DEBUG, filemode='w')

	#Logging header
	logging.info('############################################################################')
	logging.info('Report issues: https://github.com/blackwiz4rd/Vodafone-WiFi-AutoLogin/issues')
	logging.info('############################################################################')

	#Argument parser
	parser = argparse.ArgumentParser()
	parser.add_argument('-s', '--skip', action='store_true',
		help="Skip creating a new vodafone_url in vodafone.conf")
	args = parser.parse_args()
	SKIP_VODAFONE_URL = args.skip

	#Configuration
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
	FORCE = config['force'] == 'True'
	SUCCESS_URL = config['success_url']
	TIMEOUT = int(config['timeout'])
	HAS_VODAFONE_URL = 'vodafone_url' in config
	if HAS_VODAFONE_URL:
		VODAFONE_URL = config['vodafone_url']

	logging.info('Username: ' + USERNAME)
	logging.info('Customer: ' + CUSTOMER)
	logging.info('Force: ' + str(FORCE))
	logging.info('Success url: ' + SUCCESS_URL)
	logging.info('Vodafone url: ' + str(HAS_VODAFONE_URL))

	#Replace '@' with '%40'
	USERNAME.replace('@','%40')

	vodafone = isVodafone(FORCE, TIMEOUT)
	if vodafone:
		logged = False
		if not SKIP_VODAFONE_URL or not HAS_VODAFONE_URL:
			VODAFONE_URL, logged = getVodafoneUrl(SUCCESS_URL, TIMEOUT)
			setConfig(VODAFONE_URL, SKIP_VODAFONE_URL)
		if not logged:
			connect(FORCE, USERNAME, PASSWORD, CUSTOMER, SUCCESS_URL, VODAFONE_URL, TIMEOUT)

if __name__ == "__main__":
	main()
