from django.contrib.auth import get_user_model
from django.urls import reverse 
from django.test import TestCase 

from rest_framework import status 
from rest_framework.test import APIClient

from core.models import Tag

from recipe.serializers import TagSerializer

TAGS_URL = reverse('recipe:tag-list')

class PublicTagsApiTestCase(TestCase):
    #probar los api tags disponibles públicamente
    def setUp(self):
        self.client = APIClient()

    def test_login_required(self):
        #prueba que login sea requerido para obtener los tags
        res = self.client.get(TAGS_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateTagsApiTestCase(TestCase):
    #probar los api tags disponibles privadamente
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            'test@datadosis.com',
            'password'
        )
        self.client = APIClient()
        self.client.force_authenticate(self.user)

    def test_retrieve_tags(self):
        #probamos a obtener tags
        Tag.objects.create(user=self.user, name='Meat')
        Tag.objects.create(user=self.user, name='Banana')

        res = self.client.get(TAGS_URL)

        tags = Tag.objects.all().order_by('-name')
        serializer = TagSerializer(tags, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_tags_limited_to_user(self):
        #probar que los tags retornados sean del usuario
        user2 = get_user_model().objects.create_user(
            'otro@dotadosis.com', 
            'testopass'
        )
        Tag.objects.create(user=user2, name='Raspberry')
        tag = Tag.objects.create(user=self.user, name='Confort Food')

        res = self.client.get(TAGS_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.data[0]['name'], tag.name)
