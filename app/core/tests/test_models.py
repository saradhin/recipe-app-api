"""
Tests for models.
"""
from django.test import TestCase
from django.contrib.auth import get_user_model
from decimal import Decimal
from core import models

def create_user(email='user@example.com', password='testpass123'):
    """create and return a new user"""
    return get_user_model().objects.create_user(email, password)

class ModelTests(TestCase):
    """Test models"""

    def test_create_user_with_email_succesful(self):
        """Test creating user with an email is succesful"""

        email = 'test@example.com'
        password = 'testpass123'
        user = get_user_model().objects.create_user(
            email=email,
            password=password
        )

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_new_user_email_normalized(self):
        """Test email is normalized user email"""
        sample_email= [
            ['test1@EXAMPLE.com', 'test1@example.com'],
            ['test2@Example.com', 'test2@example.com'],
            ['test3@EXaMPLE.com', 'test3@example.com'],
            ['test4@exaMple.com', 'test4@example.com']
        ]

        for email, expected in sample_email:
            user = get_user_model().objects.create_user(email=email, password='sample123')
            self.assertEqual(user.email, expected)

    def test_new_user_without_email_raises_error(self):

        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(email="", password='sample123')

    def test_super_user_with_email_succesful(self):
        """Test creating super user with email succesful"""

        user = get_user_model().objects.create_superuser(email="testsup1@example.com", password='sample123')
        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)

    def test_create_recipe(self):
        """Test creating recipe"""
        user = get_user_model().objects.create_user(
            'test@example.com',
            'testpass123'
        )

        recipe = models.Recipe.objects.create(
            user=user,
            title='Sample Recipe Name',
            time_minutes = 5,
            price= Decimal('5.50'),
            description = 'Sample recipe description'
        )

        self.assertEqual(str(recipe), recipe.title)

    def test_create_tag(self):
        """Testc creating tag is succesful"""
        user = create_user()
        tag = models.Tag.objects.create(user=user, name='Tag1')

        self.assertEqual(str(tag), tag.name)
