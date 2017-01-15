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

# class AzEl(object):
# 	azimuth = ""
# 	elevation = ""

# 	def __init__(self,azimuth,elevation):
# 		self.azimuth = azimuth
# 		self.elevation = elevation


# class TLEManager(models.Manager):
    
#     def create_TLE(self, name, line1, line2):
#         TLEObject = self.create(name=name, line1=line1, line2=line2)
#         return TLEObjectook