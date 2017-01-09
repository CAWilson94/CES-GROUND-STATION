"""
Pyephem basic examples 

Output format: 
---------------
degrees, minutes of arc, and seconds of arc
----------------


To run from python shell: 
-------------------------
	from exampleCW import * 

	then call functions as needed
-------------------------

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

# Expected output: -71:51:57.3 25:28:20.0

def tle():
	line1 = "ISS (ZARYA)"
	line2 = "1 25544U 98067A   03097.78853147  .00021906  00000-0  28403-3 0  8652"
	line3 = "2 25544  51.6361  13.7980 0004256  35.6671  59.2566 15.58778559250029"
	iss = ephem.readtle(line1, line2, line3)
	iss.compute('2003/3/23')
	print('%s %s' % (iss.sublong, iss.sublat))
	lat = iss.sublat
	longiss = iss.sublong
	print('%s' % (iss.az))


# Expected output: -76:24:18.3 13:05:31.1

"""

Figures out alt and az through lat and long. Both of which 
seem to have direct conversions: 

Latitude: 1 deg = 110.574 km
Longitude: 1 deg = 111.320*cos(latitude) km

could use these for the conversion for alt?

This doesn't fully correct for the Earth's polar flattening 
- for that you'd probably want a more complicated formula using the WGS84 reference ellipsoid (the model used for GPS)
"""