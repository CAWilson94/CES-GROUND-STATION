import uuid
from django.db import models
from datetime import datetime
# Create your models here.


class TLE(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=30, unique=True, default="NAME")
    line1 = models.CharField(max_length=70)  # can't be null
    line2 = models.CharField(max_length=70)

    # def __init__(self, name, line1, line2):
    # self.name = name
    #     self.line1 = line1
    #     self.line2 = line2

    def __str__(self):
        return str(self.name)

    # objects = models.TLEManager()


class AzEl(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    azimuth = models.CharField(max_length=15)
    elevation = models.CharField(max_length=15)

    def __str__(self):
        return str(self.__dict__)

    def __eq__(self, other):
        azBool = 0
        altBool = 0
        try:
            azBool = self.azimuth == other.azimuth
            altBool = self.elevation == other.elevation
        except AttributeError:
            return False
        return azBool and altBool

        # can haz this just for testing? AK

    # def __eq__(self, other):
    # 	return self.__dict__ == other.__dict__


class Mission(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=30, unique=True)
    TLE = models.ForeignKey(TLE, on_delete=models.CASCADE)
    status = models.CharField(max_length=30)
    priority = models.IntegerField()
    #timestamp = models.DateTimeField()
    #delete=models.CharField(max_length=30)
    def __str__(self):

        #return str(self.name)
        return "id: " + str(self.id) + ", name: " + self.name  + ", status: " + self.status + ", priority: " + str(self.priority)


class NextPass(models.Model):
    #AOS
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    tle = models.ForeignKey(TLE, on_delete=models.CASCADE)

    mission=models.ForeignKey(Mission, on_delete=models.CASCADE)

    riseTime = models.DateTimeField()
    
    setTime = models.DateTimeField()

    duration = models.DurationField() 

    maxElevation = models.CharField(max_length=15)
    #AOS Az
    riseAzimuth = models.CharField(max_length=15)
    #LOS Az
    setAzimuth = models.CharField(max_length=15)

    

    def __str__(self):
        #return str(self.__dict__)
        return str(self.tle.name)
    def __eq__(self, other):
        # riseTime = datetime(17, 1, 19, 12, 0, 0)
        # setTime = datetime(17, 1, 19, 12, 0, 0)
        # duration = 0
        # maxElevation = 0
        # riseAzimuth = 0
        # setAzimuth = 0
        try:
            #Surely there is a better way but i dunno AK
            riseTime = self.riseTime == other.riseTime
            setTime = self.setTime == other.setTime
            duration = self.duration == other.duration
            maxElevation = self.maxElevation == other.maxElevation
            riseAzimuth = self.riseAzimuth == other.riseAzimuth
            setAzimuth = self.setAzimuth == other.setAzimuth
        except AttributeError:
            return False
        return riseTime and setTime and duration and maxElevation and riseAzimuth and setAzimuth

# #email
# class SatName(models.Model):
# chosensatlist=models.ForeignKey('ChosenSatList',related_name='sats')
# 	name = models.CharField(max_length=50)


# #user
# class ChosenSatList(models.Model):
# 	listName = models.CharField(max_length=20)


# class PassDetails(models.Model)
# nextpasses = models.ForeignKey(NextPasses)
# time = models.
# azimuth =
# elevation =
# #range? footprint?

# class Observer(models.Model):
# latitude = models.CharField(max_length=15)
# longtitude = models.CharField(max_length=15)
# elevation = models.IntegerField(max_length=15)

