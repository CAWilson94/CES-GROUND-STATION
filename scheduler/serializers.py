from rest_framework import serializers
from scheduler.models import TLE

class CubeSatSerializer(serializers.ModelSerializer):
    class Meta:
        model = TLE
        id = serializers.IntegerField(read_only=True)
        fields = ('name', 'line1', 'line2')