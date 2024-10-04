from django.conf import settings
from django.db import models

NULLABLE = {'blank': True, 'null': True}


class Way(models.Model):
    UNITS_MEASUREMENT_CHOICES = {
        ('HH', 'Часы'),
        ('MM', 'Минуты'),
        ('SS', 'Секунды')
    }
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='Пользователь',
                              related_name='way', **NULLABLE)
    spot = models.CharField(max_length=200, verbose_name='Место')
    data_time = models.DateTimeField(auto_now=False, verbose_name='Дата и время')
    action = models.TextField(verbose_name='Действие')
    is_nice_way = models.BooleanField(default=False, verbose_name='Приятная привычка')
    associated_way = models.ForeignKey('self', on_delete=models.SET_NULL, verbose_name='Связанная привычка', **NULLABLE)
    periodicity = models.IntegerField(verbose_name='Периодичность в днях')
    reward = models.CharField(max_length=200, verbose_name='Вознаграждение', **NULLABLE)
    time_execution = models.IntegerField(verbose_name='Время в секундах')
    is_public = models.BooleanField(default=False, verbose_name='Публичная привычка')

    def __str__(self):
        return (f'{self.owner} {self.action} {self.is_nice_way} {self.associated_way} {self.periodicity} {self.reward} '
                f'{self.time_execution} {self.is_public}')

    class Mets:
        verbose_name = 'Привычка'
        verbose_name_plural = 'Привычки'
