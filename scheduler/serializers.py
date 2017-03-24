from rest_framework import serializers
from scheduler.models import TLE, AzEl, Mission

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


# class ChosenSatListSerializer(serializers.ModelSerializer):
# 	sats = serializers.ListField(child=ChosenSatSerializer())


# class ChosenSatArraySerializer(serializers.Serializer):
# 	child = serializers.CharField()

# class SatSerialiser(serializers.ModelSerializer):
# 	class Meta:
# 		model = SatName
# 		fields=['id','email']

# class ChosenSatArraySerializer(serializers.Serializer):
# 	#child = serializers.CharField()
# 	sats=SatSerialiser(many=True)
# 	listName=serializers.CharField()

# class CompositeObjectSerializer(serializers.Serializer):
#     id = serializers.IntegerField()
#     name = serializers.CharField()