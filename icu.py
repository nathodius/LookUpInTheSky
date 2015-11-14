#!/usr/bin/env python

import getopt, sys
import geocoder
import  pywapi
import string
import urllib2
import json
import ephem	# for Satellite info
import pygame	# for audio
from twilio.rest import TwilioRestClient # for SMS
import RPi.GPIO as GPIO  # for LED's
from threading import Thread
import sys
import time

# LED thread
def flashLED():
	LED_PORT = 12 # GPIO pin 18
	GPIO.setmode(GPIO.BOARD)
	GPIO.setup(LED_PORT, GPIO.OUT) # configure GPIO as output

	for count in [1, 2, 3]:
		GPIO.output(LED_PORT, GPIO.HIGH)
		time.sleep(0.5) # blocking
		GPIO.output(LED_PORT, GPIO.LOW)
		time.sleep(0.5)

# Audio thread
def playSound():
	# CONFIGURE AUDIO
	pygame.mixer.init()
	pygame.mixer.music.load('rectrans.wav')

	# Play the sound
	pygame.mixer.music.play()
	while pygame.mixer.music.get_busy() == True:
		continue

def notify():
	# Flash LED on a separate thread
	led_thread=Thread(target=flashLED, args=())
	led_thread.start()

	# Play sound on a separate thread
	sound_thread=Thread(target=playSound, args=())
	sound.thread.start()

	# TWILIO CREDENTIALS
	ACCOUNT_SID = "AC9b2ca84eb482f25141612c4184991086"
	AUTH_TOKEN = "a3b144fabe06b268541eff165f9b1387"

	client = TwilioRestClient(ACCOUNT_SID, AUTH_TOKEN)

	# TWILIO SMS NOTIFICATION TEST
	# Send this prior to viewable event
	client.messages.create(
	to="(703) 286-9168", 
	from_="+13012653352", 
	body="I just want a different message this time",  
	)

def main(argv):

	notify()

	try:
		opts, args = getopt.getopt(sys.argv[1:], "z:s:")
	except getopt.GetoptError as err:
		print str(err) # will print something like "option -a not recognized"
		sys.exit(2) 

	zipCode = None
	NORAD_CatalogNumber = None

	print("zip code", zipCode)
	print("NORAD catalog number", NORAD_CatalogNumber)	

	for o, a in opts:
		if o == "-z":
			zipCode = a
		elif o == "-s":
			NORAD_CatalogNumber = a

	print("zip code", zipCode)
	print("NORAD catalog number", NORAD_CatalogNumber)

	if zipCode != None:
		g = geocoder.google(zipCode)
		location = g.latlng
		print("location", location) # Longitude and latitude.

	# weather_com_result = pywapi.get_weather_from_weather_com(zipCode)
	# current_conditions = weather_com_result['current_conditions']['text']
	# print ("current conditions", current_conditions)

	#############################################################################
	# Call openweathermap API
	# Info about url: API call that contains latitude, longitude, forecast day count, and API key (obtained upon signup)
	url = 'http://api.openweathermap.org/data/2.5/forecast/daily?lat=' + str(g.lat) + '&lon=' + str(g.lng) + '&cnt=16&APPID=c4758036688a08a0796290e8f5ebbe40'
	forecast = urllib2.urlopen(url)
	print("16-day forecast: ", json.loads(forecast.read()))
	##############################################################################

	##############################################################################
#	satellite = "VANGUARD 3"
#	line1 = "1 00020U 59007A   15315.53193246  .00000593  00000-0  24329-3 0  9991"
#	line2 = "2 00020  33.3468  44.5961 1669346 358.5309   1.0765 11.55084888 36273"
	
#	lat = str(g.lat)
#	lng = str(g.lng)
#	print(lat)
#	print(lng)

	# Read TLE
#	tle = ephem.readtle(satellite, line1, line2)

	# Compute TLE after setting the datetime
#	observer = ephem.Observer()
#	observer.lat = str(g.lat)
#	observer.long = str(g.lng)
	#tle.compute(ephem.Observer())
	##############################################################################


if __name__ == "__main__":
    main(sys.argv)
