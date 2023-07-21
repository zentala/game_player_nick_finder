# game_player_nick_finder/app/tests.py
from django.test import TestCase

class YourModelTestCase(TestCase):
    def setUp(self):
        # Dodaj przykładowe obiekty do testów
        YourModel.objects.create(field1='Przykład 1', field2=42)
        YourModel.objects.create(field1='Przykład 2', field2=99)

    def test_something(self):
        # Dodaj swoje testy modelu
        obj1 = YourModel.objects.get(field1='Przykład 1')
        obj2 = YourModel.objects.get(field1='Przykład 2')
        self.assertEqual(obj1.field2, 42)
        self.assertEqual(obj2.field2, 99)
