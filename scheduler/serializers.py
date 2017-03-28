from rest_framework import serializers
from scheduler.models import TLE, AzEl, Mission, NextPass

class TLESerializer(serializers.ModelSerializer):
    class Meta:
        model = TLE
        fields = ('id','name', 'line1', 'line2')

class AZELSerializer(serializers.ModelSerializer):
	class Meta:
		model = AzEl
		fields = ('id','azimuth','elevation')

class MissionSerializer(serializers.ModelSerializer):
	class Meta:
		model = Mission
		fields = ('id','name','TLE','status','priority')

class NextPassSerializer(serializers.ModelSerializer):
	class Meta:
		model = NextPass
		fields = ('__all__')

# class CompositeObjectSerializer(serializers.Serializer):
#     id = serializers.IntegerField()
#     name = serializers.CharField()