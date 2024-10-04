from rest_framework import serializers

from tracker.models import Way
from tracker.validators import RewardValidator, TimeExecutionValidator, AssociatedWayValidator, IsNiceWayValidator, \
    PeriodicityValidator


class WaySerializer(serializers.ModelSerializer):
    class Meta:
        model = Way
        fields = ['spot', 'data_time', 'action', 'is_nice_way', 'periodicity', 'reward', 'associated_way',
                  'time_execution', 'is_public']
        validators = [RewardValidator(reward='reward', associated_way='associated_way'),
                      TimeExecutionValidator(field='time_execution'),
                      AssociatedWayValidator(field='associated_way'),
                      IsNiceWayValidator(is_nice_way='is_nice_way', reward='reward', associated_way='associated_way'),
                      PeriodicityValidator(field='periodicity')]
