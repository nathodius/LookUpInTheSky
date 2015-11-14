#!/usr/bin/env python

import getopt, sys
import geocoder
import  pywapi
import string
import ephem

def main(argv):


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

	weather_com_result = pywapi.get_weather_from_weather_com(zipCode)
	current_conditions = weather_com_result['current_conditions']['text']
	print ("current conditions", current_conditions)

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
