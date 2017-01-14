from rest_framework import serializers
from scheduler.models import TLE, AzEl

class TLESerializer(serializers.ModelSerializer):
    class Meta:
        model = TLE
        fields = ('id','name', 'line1', 'line2')

class AZELSerializer(serializers.ModelSerializer):
	class Meta:
		model = AzEl
		fields = ('id','azimuth','elevation')