from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.test import APITestCase, APIClient

from tracker.models import Way
from users.models import User


class WayAPITestCase(APITestCase):

    def setUp(self) -> None:
        user1 = User.objects.create(email='test1@mail.com')
        user2 = User.objects.create(email='test2@mail.com')
        Way.objects.create(owner=user1, spot='test1', data_time='2024-10-05T01:57:20', action='test1', periodicity=1,
                           time_execution=120)
        Way.objects.create(owner=user2, spot='test2', data_time='2024-10-05T01:57:20', action='test2', periodicity=2,
                           time_execution=120, is_public=True)

    def test_way_create(self):
        data = {
            'spot': 'test3',
            'data_time': '2024-10-05T01:57:20',
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
            'data_time': '2024-10-05T01:57:20',
            'action': 'test3',
            'is_nice_way': True,
            'associated_way': 1,
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
            'data_time': '2024-10-05T01:57:20',
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
                'spot': 'test3',
                'data_time': '2024-10-05T01:57:20+03:00',
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
