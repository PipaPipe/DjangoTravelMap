from django.core.management.base import BaseCommand

from ...models import Achievements
from ...models import Levels

levels = [
    {
        'points_for_level': 10
    },
    {
        'points_for_level': 20
    },
    {
        'points_for_level': 30
    }
]

achievements = [
    {
        'name': 'Лайк - турист',
        'description': 'Проставить 5 лайков на метки другим пользователям',
        'points': 10
    },
    {
        'name': 'Метко - мастер',
        'description': 'Создать 5 меток с описанием',
        'points': 20
    },
    {
        'name': 'Лайк - легенда',
        'description': 'Получить 5 лайков на своих метках от других пользователей',
        'points': 30
    },
]


class Command(BaseCommand):
    def handle(self, *args, **options):
        for elem in levels:
            level = Levels.objects.create(points_for_level=elem['points_for_level'])
        for elem in achievements:
            achievement = Achievements.objects.create(name=elem['name'],
                                                      description=elem['description'],
                                                      points=elem['points'])
        print("finish")






