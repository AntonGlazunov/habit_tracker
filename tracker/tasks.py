from datetime import date
from time import sleep

from celery import shared_task
from dateutil.relativedelta import relativedelta
from tracker.models import Way
from tracker.services import send_telegram_message


@shared_task
def check_today_ways():
    today = date.today()
    ways = Way.objects.filter(data_time__year=today.year, data_time__month=today.month, data_time__day=today.day)
    for way in ways:
        if way.owner.chat_id is not None:
            if way.reward is not None:
                text = f'Сегодня в  месте, {way.spot}, в {way.data_time} вы должны выполнить действие, {way.action}, за это вы получите {way.reward}'
            elif way.associated_way is not None:
                text = f'Сегодня в  месте, {way.spot}, в {way.data_time} вы должны выполнить действие, {way.action}, за это вы можете перейти к привычке {way.associated_way.action}'
            else:
                text = f'Сегодня в месте {way.spot} в {way.data_time} вы можете по радовать себя действием {way.action}'
            response = send_telegram_message(text=text, chat_id=way.owner.chat_id)
            if response.get('ok'):
                update_time = way.data_time + relativedelta(days=+int(way.periodicity))
                way.data_time = update_time
                way.save()
                sleep(5)
                return 'Рассылка успешна'
            else:
                return 'Ошибка отправки'
        else:
            return 'Пользователь не добавил chat_id'

