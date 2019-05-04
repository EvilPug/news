from django.test import TestCase
from django.contrib.auth import get_user_model

User = get_user_model()


class TestUserModel(TestCase):

    def test_can_create_user(self):
        user = User.objects.create_user(email='user@example.com',
                                        username='test')
        self.assertTrue(user)

    def test_can_create_superuser(self):
        superuser = User.objects.create_superuser(
            username='test',
            email='superuser@example.com',
            password='secret'
        )
        self.assertTrue(superuser)

    def test_string_representation(self):
        user = User.objects.create_user(email='user@example.com', username='test')
        self.assertEqual(str(user), 'test')
