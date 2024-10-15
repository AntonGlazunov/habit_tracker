import datetime

from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.test import APITestCase, APIClient

from tracker.models import Way
from tracker.tasks import check_today_ways
from users.models import User


class WayAPITestCase(APITestCase):

    def setUp(self) -> None:
        tz = datetime.timezone(datetime.timedelta(hours=3))
        user1 = User.objects.create(email='test1@mail.com')
        user2 = User.objects.create(email='test2@mail.com')
        user3 = User.objects.create(email='test3@mail.com')
        Way.objects.create(pk=2, owner=user1, spot='test1',
                           data_time=datetime.datetime.now(tz=tz).strftime('%Y-%m-%d %H:%M%z'), action='test1',
                           periodicity=1,
                           time_execution=120)
        Way.objects.create(pk=3, owner=user2, spot='test2',
                           data_time=datetime.datetime.now(tz=tz).strftime('%Y-%m-%d %H:%M%z'), action='test2',
                           periodicity=2,
                           time_execution=120, is_public=True)
        Way.objects.create(pk=4, owner=user3, spot='test2',
                           data_time=datetime.datetime.now(tz=tz).strftime('%Y-%m-%d %H:%M%z'), action='test2',
                           periodicity=2, is_nice_way=True, time_execution=120, is_public=True)

    def test_way_create(self):
        self.maxDiff = None
        tz = datetime.timezone(datetime.timedelta(hours=3))
        data = {
            'spot': 'test3',
            'data_time': datetime.datetime.now(tz=tz).strftime('%Y-%m-%d %H:%M%z'),
            'action': 'test3',
            'is_nice_way': True,
            'periodicity': 3,
            'time_execution': 120,
            'is_public': True,
        }
        response = self.client.post(
            '/tracker/way/',
            data=data
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED
        )

        user = User.objects.get(email='test1@mail.com')
        client = APIClient()
        client.force_authenticate(user=user)

        data = {
            'spot': 'test3',
            'data_time': datetime.datetime.now(tz=tz).strftime('%Y-%m-%d %H:%M%z'),
            'action': 'test3',
            'is_nice_way': True,
            'associated_way': 3,
            'reward': 'test3',
            'periodicity': 8,
            'time_execution': 150,
            'is_public': True,
        }

        response = client.post(
            '/tracker/way/',
            data=data
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST
        )

        self.assertEqual(
            response.json(),
            {'non_field_errors': ["Выбери что то одно или 'reward' или 'associated_way'",
                                  "Тут 'time_execution' слишком много секундочек",
                                  "В поле 'associated_way' не приятная привычка",
                                  "Проверьте поля 'reward' 'associated_way' у приятной привычки нет вознаграждений",
                                  "Периодичность 'periodicity' привычки должна быть чаще раза в неделю"]}
        )

        self.assertRaises(
            ValidationError
        )

        data = {
            'spot': 'test3',
            'data_time': datetime.datetime.now(tz=tz).strftime('%Y-%m-%d %H:%M%z'),
            'action': 'test3',
            'is_nice_way': True,
            'periodicity': 7,
            'time_execution': 120,
            'is_public': True,
        }

        response = client.post(
            '/tracker/way/',
            data=data
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED
        )

        self.assertEqual(
            response.json(),
            {
                'pk': 1,
                'spot': 'test3',
                'data_time': datetime.datetime.now(tz=tz).strftime('%Y-%m-%dT%H:%M:00+03:00'),
                'action': 'test3',
                'is_nice_way': True,
                'periodicity': 7,
                'reward': None,
                'associated_way': None,
                'time_execution': 120,
                'is_public': True,
            }
        )

        self.assertTrue(
            Way.objects.filter(spot='test3').exists()
        )

    def test_way_list(self):
        self.maxDiff = None
        tz = datetime.timezone(datetime.timedelta(hours=3))
        response = self.client.get('/tracker/way/')

        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED
        )

        user = User.objects.get(email='test1@mail.com')
        client = APIClient()
        client.force_authenticate(user=user)

        response = client.get('/tracker/way/')

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

        self.assertEqual(
            response.json(),
            {'count': 1, 'next': None, 'previous': None, 'results': [
                {'pk': 2, 'action': 'test1', 'associated_way': None,
                 'data_time': datetime.datetime.now(tz=tz).strftime('%Y-%m-%dT%H:%M:00+03:00'),
                 'is_nice_way': False, 'is_public': False, 'periodicity': 1, 'reward': None, 'spot': 'test1',
                 'time_execution': 120}]}
        )

        user = User.objects.get(email='test2@mail.com')
        client1 = APIClient()
        client1.force_authenticate(user=user)

        response = client1.get('/tracker/way/')

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

        self.assertEqual(
            response.json(),
            {'count': 1, 'next': None, 'previous': None, 'results': [
                {'pk': 3, 'action': 'test2', 'associated_way': None,
                 'data_time': datetime.datetime.now(tz=tz).strftime('%Y-%m-%dT%H:%M:00+03:00'),
                 'is_nice_way': False, 'is_public': True, 'periodicity': 2, 'reward': None, 'spot': 'test2',
                 'time_execution': 120}]}
        )

    def test_way_retrieve(self):
        self.maxDiff = None
        tz = datetime.timezone(datetime.timedelta(hours=3))
        response = self.client.get('/tracker/way/1/')

        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED
        )

        user = User.objects.get(email='test1@mail.com')
        client = APIClient()
        client.force_authenticate(user=user)

        response = client.get('/tracker/way/2/')

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

        self.assertEqual(
            response.json(),
            {'pk': 2, 'action': 'test1', 'associated_way': None,
             'data_time': datetime.datetime.now(tz=tz).strftime('%Y-%m-%dT%H:%M:00+03:00'),
             'is_nice_way': False, 'is_public': False, 'periodicity': 1, 'reward': None, 'spot': 'test1',
             'time_execution': 120}
        )

        response = client.get('/tracker/way/3/')

        self.assertEqual(
            response.status_code,
            status.HTTP_404_NOT_FOUND
        )

        self.assertEqual(
            response.json(),
            {'detail': 'No Way matches the given query.'}
        )

        response = client.get('/tracker/way/5/')

        self.assertEqual(
            response.status_code,
            status.HTTP_404_NOT_FOUND
        )

        self.assertEqual(
            response.json(),
            {'detail': 'No Way matches the given query.'}
        )

    def test_way_put(self):
        self.maxDiff = None
        tz = datetime.timezone(datetime.timedelta(hours=3))
        data = {
            'spot': 'test3',
            'data_time': datetime.datetime.now(tz=tz).strftime('%Y-%m-%d %H:%M%z'),
            'action': 'test3',
            'is_nice_way': True,
            'periodicity': 3,
            'time_execution': 120,
            'is_public': True,
        }
        response = self.client.put(
            '/tracker/way/2/',
            data=data
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED
        )

        user = User.objects.get(email='test1@mail.com')
        client = APIClient()
        client.force_authenticate(user=user)

        data = {'spot': 'test1', 'data_time': datetime.datetime.now(tz=tz).strftime('%Y-%m-%d %H:%M%z'),
                'action': 'test1', 'associated_way': 3,
                'is_nice_way': True, 'is_public': False, 'periodicity': 8, 'reward': 'test1', 'time_execution': 150}

        response = client.put(
            '/tracker/way/2/',
            data=data
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST
        )

        self.assertEqual(
            response.json(),
            {'non_field_errors': ["Выбери что то одно или 'reward' или 'associated_way'",
                                  "Тут 'time_execution' слишком много секундочек",
                                  "В поле 'associated_way' не приятная привычка",
                                  "Проверьте поля 'reward' 'associated_way' у приятной привычки нет вознаграждений",
                                  "Периодичность 'periodicity' привычки должна быть чаще раза в неделю"]}
        )

        self.assertRaises(
            ValidationError
        )

        data = {'spot': 'test5', 'data_time': datetime.datetime.now(tz=tz).strftime('%Y-%m-%d %H:%M%z'),
                'action': 'test2',
                'is_nice_way': False, 'is_public': True, 'periodicity': 7, 'reward': 'test1', 'time_execution': 100}

        response = client.put(
            '/tracker/way/2/',
            data=data
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

        self.assertEqual(
            response.json(),
            {
                'pk': 2,
                'spot': 'test5',
                'data_time': datetime.datetime.now(tz=tz).strftime('%Y-%m-%dT%H:%M:00+03:00'),
                'action': 'test2',
                'is_nice_way': False,
                'periodicity': 7,
                'reward': 'test1',
                'associated_way': None,
                'time_execution': 100,
                'is_public': True,
            }
        )

        self.assertTrue(
            Way.objects.filter(spot='test5').exists()
        )

        response = client.put(
            '/tracker/way/3/',
            data=data
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_404_NOT_FOUND
        )

    def test_way_patch(self):
        self.maxDiff = None
        tz = datetime.timezone(datetime.timedelta(hours=3))
        data = {
            'spot': 'test3',
            'data_time': datetime.datetime.now(tz=tz).strftime('%Y-%m-%d %H:%M%z'),
            'action': 'test3',
            'is_nice_way': True,
            'periodicity': 3,
            'time_execution': 120,
            'is_public': True,
        }
        response = self.client.patch(
            '/tracker/way/2/',
            data=data
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED
        )

        user = User.objects.get(email='test1@mail.com')
        client = APIClient()
        client.force_authenticate(user=user)

        data = {'spot': 'test1', 'data_time': datetime.datetime.now(tz=tz).strftime('%Y-%m-%d %H:%M%z'),
                'action': 'test1', 'associated_way': 3,
                'is_nice_way': True, 'is_public': False, 'periodicity': 8, 'reward': 'test1', 'time_execution': 150}

        response = client.patch(
            '/tracker/way/2/',
            data=data
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST
        )

        self.assertEqual(
            response.json(),
            {'non_field_errors': ["Выбери что то одно или 'reward' или 'associated_way'",
                                  "Тут 'time_execution' слишком много секундочек",
                                  "В поле 'associated_way' не приятная привычка",
                                  "Проверьте поля 'reward' 'associated_way' у приятной привычки нет вознаграждений",
                                  "Периодичность 'periodicity' привычки должна быть чаще раза в неделю"]}
        )

        self.assertRaises(
            ValidationError
        )

        data = {'spot': 'test5', 'data_time': datetime.datetime.now(tz=tz).strftime('%Y-%m-%d %H:%M%z'),
                'action': 'test2',
                'is_nice_way': False, 'is_public': True, 'periodicity': 7, 'reward': 'test1', 'time_execution': 100}

        response = client.patch(
            '/tracker/way/2/',
            data=data
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

        self.assertEqual(
            response.json(),
            {
                'pk': 2,
                'spot': 'test5',
                'data_time': datetime.datetime.now(tz=tz).strftime('%Y-%m-%dT%H:%M:00+03:00'),
                'action': 'test2',
                'is_nice_way': False,
                'periodicity': 7,
                'reward': 'test1',
                'associated_way': None,
                'time_execution': 100,
                'is_public': True,
            }
        )

        self.assertTrue(
            Way.objects.filter(spot='test5').exists()
        )

        response = client.patch(
            '/tracker/way/3/',
            data=data
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_404_NOT_FOUND
        )

    def test_way_delite(self):
        self.maxDiff = None
        response = self.client.delete('/tracker/way/1/')

        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED
        )

        user = User.objects.get(email='test1@mail.com')
        client = APIClient()
        client.force_authenticate(user=user)

        response = client.delete('/tracker/way/2/')

        self.assertEqual(
            response.status_code,
            status.HTTP_204_NO_CONTENT
        )

        response = client.delete('/tracker/way/1/')

        self.assertEqual(
            response.status_code,
            status.HTTP_404_NOT_FOUND
        )

    def test_tasks_and_send_message_telegrsm(self):
        response = check_today_ways()

        self.assertEqual(
            response,
            'Пользователь не добавил chat_id'
        )

        user = User.objects.get(email='test1@mail.com')
        user.chat_id = 12314141
        user.save()

        response = check_today_ways()

        self.assertEqual(
            response,
            'Ошибка отправки'
        )

        user.chat_id = 154908784
        user.save()

        response = check_today_ways()

        self.assertEqual(
            response,
            'Рассылка успешна'
        )

    def test_way_public_list(self):
        self.maxDiff = None
        tz = datetime.timezone(datetime.timedelta(hours=3))

        response = self.client.get('/tracker/way-public-list/')

        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED
        )

        user = User.objects.get(email='test3@mail.com')
        client = APIClient()
        client.force_authenticate(user=user)

        response = client.get('/tracker/way-public-list/')

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

        self.assertEqual(
            response.json(),
            {'count': 2, 'next': None, 'previous': None, 'results': [
                {'action': 'test2', 'associated_way': None,
                 'data_time': datetime.datetime.now(tz=tz).strftime('%Y-%m-%dT%H:%M:00+03:00'),
                 'is_nice_way': False, 'periodicity': 2, 'reward': None, 'spot': 'test2',
                 'time_execution': 120},
                {'action': 'test2', 'associated_way': None,
                 'data_time': datetime.datetime.now(tz=tz).strftime('%Y-%m-%dT%H:%M:00+03:00'),
                 'is_nice_way': True, 'periodicity': 2, 'reward': None, 'spot': 'test2',
                 'time_execution': 120}]}
        )
