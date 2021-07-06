from django.contrib.auth import get_user_model
from django.urls import reverse 
from django.test import TestCase 

from rest_framework import status 
from rest_framework.test import APIClient

from core.models import Ingredient

from recipe.serializers import IngredientSerializer

INGREDIENTS_URL = reverse('recipe:ingredient-list')

class PublicIngredientsApiTestCase(TestCase):
    #probar los api ingredinetes disponibles públicamente
    def setUp(self):
        self.client = APIClient()

    def test_login_required(self):
        #prueba que login sea requerido para obtener los tags
        res = self.client.get(INGREDIENTS_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

class PrivateIngredientsApiTestCase(TestCase):
    #probar los api ingredinetes disponibles privadamente
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            'test@datadosis.com', 
            'testopass'
        )
        self.client.force_authenticate(self.user)

    def test_retrieve_ingredient_list(self):
        #probar a obtener la lista de los ingredientes
        Ingredient.objects.create(user=self.user, name='milk')
        Ingredient.objects.create(user=self.user, name='cheese')

        res = self.client.get(INGREDIENTS_URL)

        ingredients = Ingredient.objects.all().order_by('-name')
        serializer = IngredientSerializer(ingredients, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_ingredients_limited_to_user(self):
        #probar que los tags retornados sean del usuario
        user2 = get_user_model().objects.create_user(
            'otro@dotadosis.com', 
            'testopass'
        )
        Ingredient.objects.create(user=user2, name='RasVinegarpberry')
        ingredient = Ingredient.objects.create(user=self.user, name='Food')

        res = self.client.get(INGREDIENTS_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.data[0]['name'], ingredient.name)