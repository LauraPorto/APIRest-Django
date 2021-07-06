from django.test import TestCase
from django.contrib.auth import get_user_model

from core import models

def sample_user(email='test@datadosis.com', password='testopass'):
    #crear usuario ejemplo
    return get_user_model().objects.create_user(email, password)

class ModelTest(TestCase):

    def test_create_user_with_email_successful(self):
        #Probar crear un nuevo usuario con un email correctamente#
        email = 'test@datadosis.com'
        password = 'Testpass123'
        user = get_user_model().objects.create_user(
            email = email, password = password
        )

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_new_user_email_normalized(self):
        #Testeo email para nuevo usuario normalizado (minúscula despues de @)#
        email = 'test@DATADOSIS.COM'
        user = get_user_model().objects.create_user(
            email, 
            'Testpass123'
        )

        #Esta es la función que hace que se normalice el email#
        self.assertEqual(user.email, email.lower())
        
    def test_new_user_invalid_email(self):
        #Nuevo usuario email inválido (comprobación de error)#
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(None, 'Testpass123')

    def test_create_new_superuser(self):

        #Probar superusuario creado#
        email = 'test@datadosis.com'
        password = 'Testpass123'
        user = get_user_model().objects.create_superuser(
            email = email, password = password
        )

        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)

    def test_tag_str(self):
        #probar representación en cadena de texto del tag
        tag = models.Tag.objects.create(
            user=sample_user(), 
            name='Meat'
        )
        self.assertEqual(str(tag), tag.name)