#Vodafone-WiFi
#Automated login for it.portal.vodafone-wifi.com

import requests, sys, objc, time

#WiFi class for OSX
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

#checks if ssid is vodafone or specified ssid in input	
class NotConnectedToVodafoneWiFiException(Exception):
	def __init__(self):
		print 'NotConnectedToVodafoneWiFiException'
	
def isVodafone(custom_ssid):
	wifi = WiFi()
	current_ssid = wifi.get_ssid()

	if current_ssid != 'Vodafone-WiFi' and current_ssid != custom_ssid:
		raise NotConnectedToVodafoneWiFiException()
		
	return True

#checks if login was made or not
def isLogged(str1, str2):
	return (str1).startswith(str2)
	
def parseUrl(welcomeUrl, successUrl):
	return welcomeUrl[0:47] + 'login' + welcomeUrl[54:172] + '&userurl=' + successUrl
	
def getInput():
	f = open('input.txt', 'r')
	input = f.read().split()
	f.close()
	return input
	
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
		pass

	if vodafone:
		url = 'http://www.apple.com/library/test/success.html'

		#if google isn't sending response exit the program
		try:
			r = requests.get(url, timeout=5)
		except requests.exceptions.Timeout as e:
			print e
	
		print 'welcome url: '
		print r.url
		print 'status_code: '
		print r.status_code

		#if response url is not success page Login into hotspot
		logged = isLogged(r.url, url)
		if not logged:
		
			#generates login url from welcome url
			parsedUrl = parseUrl(r.url, url)

			print 'login parsed url: ' + parsedUrl

			#Form Data used to login
			payload = getPayload(USERNAME, PASSWORD)
	
			#returns ConnectionError if login is successful
			try:
				r = requests.post(parsedUrl, data = payload)
				print 'status_code: '
				print r.status_code
				logged = True
			except requests.ConnectionError as e:
				print e

		if logged:
			print 'You are logged to a Vodafone router'
		else:
			print 'Error: You are not logged, have miss-spelled your username/password?'
		
if __name__ == "__main__":
    main()
