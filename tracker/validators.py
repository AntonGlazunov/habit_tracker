from rest_framework.serializers import ValidationError

from tracker.models import Way


class RewardValidator:

    def __init__(self, reward, associated_way):
        self.reward = reward
        self.associated_way = associated_way

    def __call__(self, value):
        if dict(value).get(self.reward) and dict(value).get(self.associated_way) is not None:
            raise ValidationError("Выбери что то одно или 'reward' или 'associated_way'")


class TimeExecutionValidator:
    def __init__(self, field):
        self.field = field

    def __call__(self, value):
        if int(dict(value).get(self.field)) > 120:
            raise ValidationError("Тут 'time_execution' слишком много секундочек")


class AssociatedWayValidator:
    def __init__(self, field):
        self.field = field

    def __call__(self, value):
        associated_way = dict(value).get(self.field)
        if associated_way is not None and not associated_way.is_nice_way:
            raise ValidationError("В поле 'associated_way' не приятная привычка")


class IsNiceWayValidator:
    def __init__(self, is_nice_way, reward, associated_way):
        self.is_nice_way = is_nice_way
        self.reward = reward
        self.associated_way = associated_way

    def __call__(self, value):
        is_nice_way = dict(value).get(self.is_nice_way)
        reward = dict(value).get(self.reward)
        associated_way = dict(value).get(self.associated_way)
        if is_nice_way:
            if reward or associated_way is not None:
                raise ValidationError("Проверьте поля 'reward' 'associated_way' у приятной привычки нет вознаграждений")


class PeriodicityValidator:
    def __init__(self, field):
        self.field = field

    def __call__(self, value):
        periodicity = dict(value).get(self.field)
        if int(periodicity) > 7:
            raise ValidationError("Периодичность 'periodicity' привычки должна быть чаще раза в неделю")
