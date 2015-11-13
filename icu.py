#!/usr/bin/env python

import getopt, sys

def main(argv):

	print("running...")

	try:
		opts, args = getopt.getopt(sys.argv[1:], "z:s:")
		print ("init getopt")
	except getopt.GetoptError as err:
		print ("uhoh")
		print str(err) # will print something like "option -a not recognized"
		sys.exit(2)

	print("done with try-except")


	zipCode = None
	NORAD_CatalogNumber = None  

	print ("init vars") 

	print("zip code", zipCode)
	print("NORAD catalog number", NORAD_CatalogNumber)	

	for o, a in opts:
		if o == "-z":
			zipCode = a
		elif o == "-s":
			NORAD_CatalogNumber = a

	print("zip code", zipCode)
	print("NORAD catalog number", NORAD_CatalogNumber)

if __name__ == "__main__":
    main(sys.argv)