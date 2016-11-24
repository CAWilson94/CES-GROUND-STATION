from django.db import models

# Create your models here.

class SatelliteName(models.Model):
    name = models.CharField(max_length=70,unique=True)

    def __str__(self):
        return self.name

class TLE(models.Model):
    satellitename = models.OneToOneField(SatelliteName)
    line1 = models.CharField(max_length=70)
    line2 = models.CharField(max_length=70)

    def __str__(self):
        return self.name