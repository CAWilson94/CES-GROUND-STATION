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
import datetime


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

# need observer and thing looking at
def tle():
	gatech = ephem.Observer()
	gatech.lon = '-84.39733'
	gatech.lat = '33.775867'
	gatech.elevation = 320
	gatech.date = '2017/01/10 16:22:56'
	line1 = "ISS"
	line2 = "1 25544U 98067A   17006.57365116  .00016717  00000-0  10270-3 0  9005"
	line3 = "2 25544  51.6418 123.9690 0007015  56.3626 303.8195 15.54006317 36615"
	iss = ephem.readtle(line1, line2, line3)
	iss.compute(gatech)
	print('%s' % (iss.alt))
	# Expected output: -83:23:17.7
	print('%s' % (iss.az))
	# Expected output: 67:19:50.8


# need observer and thing looking at
def glasgow():
	glasgow = ephem.Observer()
	glasgow.lon = '-4.4333'  # + EAST ( gpredict defaults at WEST)
	glasgow.lat = '55.8667' # + NORTH
	glasgow.elevation = 0 # From elevationmap.net
	glasgow.date = datetime.datetime.now()
	line1 = "CANX-2"
	line2 = "1 32790U 08021H   17009.81203317  .00000243  00000-0  32442-4 0  9992"
	line3 = "2 32790  97.5788  39.6856 0013256 340.5856  19.4854 14.87512065471295"
	iss = ephem.readtle(line1, line2, line3)
	iss.compute(glasgow)
	print('%s' % (iss.az))
	print('%s' % (iss.alt))

glasgow();

"""

Figures out alt and az through lat and long. Both of which 
seem to have direct conversions: 

Latitude: 1 deg = 110.574 km
Longitude: 1 deg = 111.320*cos(latitude) km

could use these for the conversion for alt?

This doesn't fully correct for the Earth's polar flattening 
- for that you'd probably want a more complicated formula using the WGS84 reference ellipsoid (the model used for GPS)
"""