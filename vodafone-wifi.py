#!/usr/bin/env python

#Vodafone-WiFi
#Automated login for it.portal.vodafone-wifi.com

#Interface
#isVodafone(custom_ssid) raises NotConnectedToVodafoneWiFiException(Exception)
#isLogged(history) 
#parseUrl(welcomeUrl, SUCCESS_URL)
#getInput()
#getPayload(USERFAKE, PASS)

import requests
from os.path import join, expanduser, dirname, realpath
from time import sleep
#for osx
import objc
#for cross platform
from sys import platform
#for win and linux
from subprocess import check_output

#OSX - WiFi class
class WiFi(object):
	def __init__(self):
		if platform.startswith('win') or platform.startswith('cygwin'):
    			self.do_windows_stuff()
		elif platform.startswith('darwin'):
    			self.do_osx_stuff()
		elif platform.startswith('linux'):
		    	self.do_linux_stuff()
		else:
    			raise Exception("Nobody's written the stuff for {}, sorry".format(platform))

	def do_windows_stuff(self):
		self.ssid = ''
		subprocessoutput = check_output(['netsh', 'wlan', 'show', 'interface'])

		for line in subprocessoutput.splitlines():
			line = line.decode('UTF-8')
			if line.startswith('    SSID'):
				self.ssid = line.split(': ')[1]

	def do_osx_stuff(self):	
		objc.loadBundle('CoreWLAN',
                bundle_path='/System/Library/Frameworks/CoreWLAN.framework',
                module_globals=globals())
	
		self.wifi = CWInterface.interfaceNames()
			
		for iname in self.wifi:
			self.ssid = CWInterface.interfaceWithName_(iname).ssid()	

	def do_linux_stuff(self):
		self.ssid = ''
		subprocessoutput = check_output(["iwlist", "wlan0", "scan"])

		for line in subprocessoutput.split():
		  if line.startswith("ESSID"):
		    self.ssid = line.split('"')[1]

	def get_ssid(self):
		return self.ssid

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
	f = open(join(dirname(realpath(__file__)), 'input.txt'), 'r')
	input = f.read().split()
	f.close()
	if len(input) == 2:
		return ['', input[0], input[1]]
	
	return [input[0], input[1], input[2]]
	
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
	print('Please, report any error that may occurr at blackwiz4rd@gmail.com')

	input = ['','','']
	try:
		input = getInput()
	except IOError as e:
		print(e)

	ssid = input[0]
	USERNAME = input[1]
	PASSWORD = input[2]

	vodafone = False

	try:
		vodafone = isVodafone(ssid)
	except NotConnectedToVodafoneWiFiException as e:
		print('not vodafone')

	if vodafone:
		SUCCESS_URL = 'http://captive.apple.com/hotspot-detect.html'
		#later assigned
		hotspotUrl = ''	

		logged = False

		#if get request isn't sending response retry in 10 seconds
		while not hotspotUrl:
			try:
				r = requests.get(SUCCESS_URL, timeout=10)

				hotspotUrl = r.url
				logged = isLogged(r.history)
			except requests.exceptions.Timeout as e:
				print(e)
				print('retrying get request because of Timeout')
				sleep(10)
			except requests.ConnectionError as e:
				print(e)
				print('retrying get request because of ConnectionError')
				sleep(10)
			
		print('logged var:')
		print(logged)

		#if not logged try login
		if hotspotUrl and not logged:
			print('trying to login...')
		
			#generates login url from welcome url
			parsedUrl = parseUrl(hotspotUrl, SUCCESS_URL)	#can cause undefined behaviour -> query strings

			print('login parsed url: ' + parsedUrl)

			#Form Data used to login
			payload = getPayload(USERNAME, PASSWORD)
	
			#may return ConnectionError if login is successful because then it re-establishes connection
			try:
				r = requests.post(parsedUrl, data=payload, timeout=20)

				logged = isLogged(not r.history)
			except requests.exceptions.Timeout as e:
				print(e)
			except requests.ConnectionError as e:
				print(e)
		
		if logged:
			print('logged')
		else:
			print('maybe login failed, check your username and password in input.txt')
if __name__ == "__main__":
    main()
