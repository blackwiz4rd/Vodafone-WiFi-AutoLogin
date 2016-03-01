#!/usr/bin/env python

#Vodafone-WiFi
#Automated login for it.portal.vodafone-wifi.com

#Interface
#isVodafone(custom_ssid) raises NotConnectedToVodafoneWiFiException(Exception)
#isLogged(history) 
#parseUrl(welcomeUrl, SUCCESS_URL)
#getInput()
#getPayload(USERFAKE, PASS)

import requests, objc
from os import path
from time import sleep

#WiFi class for OSX - NOT needed if using NetworkListener
objc.loadBundle('CoreWLAN',
                bundle_path='/System/Library/Frameworks/CoreWLAN.framework',
                module_globals=globals())
                
class WiFi(object):
	def __init__(self):
		self.wifi = CWInterface.interfaceNames()
		for iname in self.wifi:
			self.interface = CWInterface.interfaceWithName_(iname)
	
	def get_ssid(self):
		return self.interface.ssid()

#raised if SSID is not Vodafone or Vodafone extender
class NotConnectedToVodafoneWiFiException(Exception):
	def __init__(self):
		pass

#checks if SSID is Vodafone or Vodafone extender
def isVodafone(custom_ssid):
	wifi = WiFi()
	current_ssid = wifi.get_ssid()

	if current_ssid != 'Vodafone-WiFi' and current_ssid != custom_ssid:
		raise NotConnectedToVodafoneWiFiException()
		
	return True

#checks if login was made or not by looking if redirect has been done
def isLogged(history):

	if history:
		raise requests.ConnectionError

	return True
	
#can cause undefined behaviour depending on welcomeUrl
def parseUrl(welcomeUrl, SUCCESS_URL):
	return welcomeUrl[0:47] + 'login' + welcomeUrl[54:172] + '&userurl=' + SUCCESS_URL
	
#reads from file and splits input parameters
def getInput():
	f = open(path.join(path.expanduser('~'), 'input.txt'), 'r')
	input = f.read().split()
	f.close()
	return input
	
#sets data for post request
def getPayload(USERFAKE, PASS):
	return {
			'chooseCountry': 'VF_IT%2F', 
			'userFake': USERFAKE, 
			'UserName': 'VF_IT%2F' + USERFAKE, 
			'Password': PASS, 
			'rememberMe': 'true', 
			'_rememberMe': 'on'
			}

def main():
	print 'Please, report any error that may occurr at blackwiz4rd@gmail.com'

	input = ['','','']
	try:
		input = getInput()
	except IOError as e:
		print e

	ssid = input[0]
	USERNAME = input[1]
	PASSWORD = input[2]

	vodafone = False

	try:
		vodafone = isVodafone(ssid)
	except NotConnectedToVodafoneWiFiException as e:
		print 'not vodafone'

	if vodafone:
		#http://captive.apple.com/hotspot-detect.html
		SUCCESS_URL = 'http://www.apple.com/library/test/success.html'
		#later assigned
		hotspotUrl = ''	

		logged = False

		#if google isn't sending response raise exception
		try:
			sleep(10)
			r = requests.get(SUCCESS_URL, timeout=(10, 10))

			hotspotUrl = r.url
			logged = isLogged(r.history)
		except requests.exceptions.Timeout as e:
			print e
		except requests.ConnectionError as e:
			print e
			
		print 'logged var:'
		print logged

		#if not logged try login
		if hotspotUrl and not logged:
			print 'trying to login...'
		
			#generates login url from welcome url
			parsedUrl = parseUrl(hotspotUrl, SUCCESS_URL)	#can cause undefined behaviour -> query strings

			print 'login parsed url: ' + parsedUrl

			#Form Data used to login
			payload = getPayload(USERNAME, PASSWORD)
	
			#may return ConnectionError if login is successful because then it re-establishes connection
			try:
				r = requests.post(parsedUrl, data=payload, timeout=(20, 20))

				logged = isLogged(not r.history)
			except requests.exceptions.Timeout as e:
				print e
			except requests.ConnectionError as e:
				print e
		
	if logged:
		print 'logged'
	else:
		print 'may be not logged, check your username and password in input.txt'
if __name__ == "__main__":
    main()
