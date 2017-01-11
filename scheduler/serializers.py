from rest_framework import serializers
from scheduler.models import TLE

class TLESerializer(serializers.ModelSerializer):
    class Meta:
        model = TLE
        fields = ('id','name', 'line1', 'line2')