from rest_framework import serializers

from tracker.models import Way


class WaySerializer(serializers.ModelSerializer):
    class Meta:
        model = Way
        fields = ['spot', 'data_time', 'action', 'is_nice_way', 'periodicity', 'reward', 'associated_way',
                  'time_execution', 'is_public']


