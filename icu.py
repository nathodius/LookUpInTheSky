#!/usr/bin/env python

import getopt, sys
import geocoder


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
		coordinates = g.latlng
		print("coordinates", coordinates)

if __name__ == "__main__":
    main(sys.argv)