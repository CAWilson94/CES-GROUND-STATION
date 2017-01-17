from django.db import models

# Create your models here.


class TLE(models.Model):
    name = models.CharField(max_length=30,unique=True,default="NAME")
    line1 = models.CharField(max_length=70)#can't be null
    line2 = models.CharField(max_length=70)

#     objects = models.TLEManager()


class AzEl(models.Model):
	azimuth = models.CharField(max_length =15)
	elevation = models.CharField(max_length=15)

# class Observer(models.Model):
# latitude = models.CharField(max_length=15)
# longtitude = models.CharField(max_length=15)
# elevation = models.IntegerField(max_length=15)

# class NextPasses(models.Model, cascade)
# tle = models.ForeignKey(TLE.name)
# #AOS
# riseTime = models.DateField(auto) #maybe datetime but that means rounding errors, maybe that's only really for time stamps
# #LOS
# setTime = models.
# duration = models.DurationField()#still that's python datetime
# maxElevation = models.CharField(max_length=5)
# #AOS Az
# riseAzimuth = models.CharField(max_length =15)
# #LOS Az
# setAzimuth = models.CharField(max_length =15)

# class PassDetails(models.Model)
# nextpasses = models.ForeignKey(NextPasses)
# time = models.
# azimuth =
# elevation =
# #range? footprint?

