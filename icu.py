#!/usr/bin/env python

import getopt, sys
import geocoder
import  pywapi
import string


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


if __name__ == "__main__":
    main(sys.argv)