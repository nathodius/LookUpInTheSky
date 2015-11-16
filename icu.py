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
import datetime
from BeautifulSoup import BeautifulSoup
from datetime import datetime
import datetime
import math
from math import degrees
from calendar import timegm

def seconds_between(d1, d2):
    return abs((d2 - d1).seconds)

def datetime_from_time(tr):
    year, month, day, hour, minute, second = tr.tuple()
    dt = datetime.datetime(year, month, day, hour, minute, int(second))
    return dt

def get_next_pass(lon, lat, alt, tle):

	sat = ephem.readtle(str(tle[0]), str(tle[1]), str(tle[2]))

	observer = ephem.Observer()
	observer.lat = str(lat)
	observer.long = str(lon)
	#observer.elevation = alt
	observer.pressure = 0
	observer.horizon = '-0:34'

	now = nextTime = datetime.datetime.utcnow()
	observer.date = now

	tr, azr, tt, altt, ts, azs = observer.next_pass(sat)

	duration = int((ts - tr) *60*60*24)
	rise_time = datetime_from_time(tr)
	mid_time = rise_time + datetime.timedelta(seconds = duration)
	max_time = datetime_from_time(tt)
	set_time = datetime_from_time(ts)

	observer.date = max_time

	sun = ephem.Sun()
	sun.compute(observer)
	sat.compute(observer)

	sun_alt = round(math.degrees(sun.alt)) 

	rise_time = str(rise_time.timetuple()[0]) + ' ' + str(rise_time.timetuple()[1]) + ' ' + str(rise_time.timetuple()[2]) + ' ' + str(rise_time.timetuple()[3]) + ' ' + str(rise_time.timetuple()[4])

	set_time = str(set_time.timetuple()[0]) + ' ' + str(set_time.timetuple()[1]) + ' ' + str(set_time.timetuple()[2]) + ' ' + str(set_time.timetuple()[3]) + ' ' + str(set_time.timetuple()[4])

	visible = [None]*5

	while None in visible:
		if sat.eclipsed is False and -25 < sun_alt < -10 :
			#riseTime[]
			for index in range(5):
				if visible[index] is None:
					visible[index] = mid_time
					break
					
		#else:
		# Change time.
		# Check out the next pass.
		nextTime = nextTime + datetime.timedelta(hours = 1)
		observer.date = nextTime
		sun = ephem.Sun()
		sun.compute(observer)
		sat.compute(observer)
		sun_alt = round(math.degrees(sun.alt)) 
		tr, azr, tt, altt, ts, azs = observer.next_pass(sat)
		duration = int((ts - tr) *60*60*24)
		rise_time = datetime_from_time(tr)
		max_time = datetime_from_time(tt)
		set_time = datetime_from_time(ts)
		mid_time = rise_time + datetime.timedelta(seconds = duration)
		rise_time = str(rise_time.timetuple()[0]) + ' ' + str(rise_time.timetuple()[1]) + ' ' + str(rise_time.timetuple()[2]) + ' ' + str(rise_time.timetuple()[3]) + ' ' + str(rise_time.timetuple()[4])
		set_time = str(set_time.timetuple()[0]) + ' ' + str(set_time.timetuple()[1]) + ' ' + str(set_time.timetuple()[2]) + ' ' + str(set_time.timetuple()[3]) + ' ' + str(set_time.timetuple()[4])
		#print(rise_time)

	return visible

# Global variable to keep track of time.
# Audio and LED notifications should be on for 10 mins
snap_time = time.time() # Gets current time in seconds

#LED thread
def flashLED():
	LED_PORT = 12 # GPIO pin 18
	GPIO.setmode(GPIO.BOARD)
	GPIO.setwarnings(False)
	GPIO.setup(LED_PORT, GPIO.OUT) # configure GPIO as output

	while ((time.time() - snap_time) / 60) < 10:
		GPIO.output(LED_PORT, GPIO.HIGH)
		time.sleep(1) # blocking
		GPIO.output(LED_PORT, GPIO.LOW)
		time.sleep(1)

# Audio thread
def playSound():
	# CONFIGURE AUDIO
	pygame.mixer.init()
	pygame.mixer.music.load('rectrans.wav')

	# Play the sound (for 10 mins)
	while ((time.time() - snap_time) / 60) < 10:
		pygame.mixer.music.play()
		time.sleep(3)
		while pygame.mixer.music.get_busy() == True:
			continue

def notify():
	# Save snapshot of time at the moment this function is invoked
	snap_time = time.time() # Wall time (vs. process time, to bypass sleep())

	# Flash LED on a separate thread
	led_thread=Thread(target=flashLED, args=())
	led_thread.start()

	# Play sound on a separate thread
	sound_thread=Thread(target=playSound, args=())
	sound_thread.start()

	# TWILIO CREDENTIALS
	ACCOUNT_SID = "AC9b2ca84eb482f25141612c4184991086"
	AUTH_TOKEN = "a3b144fabe06b268541eff165f9b1387"

	client = TwilioRestClient(ACCOUNT_SID, AUTH_TOKEN)

	# TWILIO SMS NOTIFICATION TEST
	# Send this prior to viewable event
	client.messages.create(
	to="(703) 286-9168", 
	from_="+13012653352", 
	body="The aliens are gonna destroy us! Nah, your satellite is about to be visible.",  
 	)

def main(argv):

	print # blank line

	# notify()

	try:
		opts, args = getopt.getopt(sys.argv[1:], "z:s:")
	except getopt.GetoptError as err:
		print str(err) # will print something like "option -a not recognized"
		sys.exit(2) 

	zipCode = None
	NORAD_CatalogNumber = None

	for o, a in opts:
		if o == "-z":
			zipCode = a
		elif o == "-s":
			NORAD_CatalogNumber = a

	print("zip code", zipCode)
	print("NORAD catalog number", NORAD_CatalogNumber)

	#############################################################################
	# Call openweathermap API
	# Info about url: API call that contains latitude, longitude, forecast day count, and API key (obtained upon signup)
	if (zipCode != None) and (NORAD_CatalogNumber != None):

		g = geocoder.google(zipCode)
		lat_rad = math.radians(g.lat)
		lng_rad = math.radians(g.lng)
		weather_url = 'http://api.openweathermap.org/data/2.5/forecast/daily?lat=' + str(g.lat) + '&lon=' + str(g.lng) + '&cnt=16&APPID=c4758036688a08a0796290e8f5ebbe40'
		forecast = urllib2.urlopen(weather_url)
		forecast_json = json.loads(forecast.read())
		print("Printing 16-day forecast: ")
		print (forecast_json)
		weatherCondition = [False]*16
		for i in range(16):
			if forecast_json["list"][i]["clouds"] <= 20:
				weatherCondition[i] = True



		print # Print separation 

		NORAD_CatalogNumber_url = 'http://www.celestrak.com/cgi-bin/TLE.pl?CATNR=' + NORAD_CatalogNumber
		tle = urllib2.urlopen(NORAD_CatalogNumber_url)
		tle_json = json.loads(json.dumps(tle.read()))
		parsed_html = BeautifulSoup(tle_json)
		html_pre = parsed_html.body.find('pre').text
		pre_lines = html_pre.split('\n')
		print("Printing tle data: ")
		print pre_lines[0]
		line1 = pre_lines[1]
		print line1
		line2 = pre_lines[2]
		print line2
		tle = ephem.readtle(NORAD_CatalogNumber, line1, line2)
		start_time = datetime.datetime.utcnow()
		tle.compute(start_time)
		#pre_lines[0] = NORAD_CatalogNumber
		satTimes = get_next_pass(lng_rad, lat_rad, tle.elevation, pre_lines)

		print

		print satTimes
		notify()

		# for i in range(5):
		# 	#print satTimes[i]
		# 	for j in range(len(weatherCondition)):
		# 		#print weatherCondition[j]
		# 		if weatherCondition[j] == True and ( (satTimes[i] - (datetime.datetime.now() + datetime.timedelta(days = j))).seconds < 12000  ):
		# 			print ("match at", i, j)



if __name__ == "__main__":
    main(sys.argv)
