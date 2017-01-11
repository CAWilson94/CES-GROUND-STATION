from django.db import models

# Create your models here.


class TLE(models.Model):
    #satellitename = models.OneToOneField(SatelliteName)
    #satellitename = models.ForeignKey(SatelliteName, on_delete=models.CASCADE)
    name = models.CharField(max_length=30,unique=True,default="NAME")
    line1 = models.CharField(max_length=70)
    line2 = models.CharField(max_length=70)

    class Meta:
    	ordering = ('name',)#worth the db cost?