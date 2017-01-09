"""
Pyephem basic examples 

"""

import ephem


def az_alt_venus():
	gatech = ephem.Observer()
	gatech.lon = '-84.39733'
	gatech.lat = '33.775867'
	gatech.elevation = 320
	gatech.date = '1984/5/30 16:22:56'
	v = ephem.Venus(gatech)
	print('%s %s' % (v.alt, v.az))

# Expected output: 	72:19:44.8 134:14:25.3


def az_alt_mars():
	gatech = ephem.Observer()
	gatech.lon = '-84.39733'
	gatech.lat = '33.775867'
	gatech.elevation = 320
	gatech.date = '1984/5/30 16:22:56'
	v = ephem.Mars(gatech)
	print('%s %s' % (v.alt, v.az))