from django.db import models

# Create your models here.


class TLE(models.Model):
    name = models.CharField(max_length=30,unique=True,default="NAME")
    line1 = models.CharField(max_length=70)#can't be null
    line2 = models.CharField(max_length=70)

    