from rest_framework import viewsets, mixins
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from core.models import Tag, Ingredient, Recipe 

from recipe import serializers
# Create your views here.

class BaseRecipeViewSet(viewsets.GenericViewSet, mixins.ListModelMixin, mixins.CreateModelMixin):
    #viewsets base
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        #retornar objetos para el usuario autenticado
        return self.queryset.filter(user=self.request.user).order_by('-name')

    def perform_create(self, serializer):
        #crear un nuevo ingredientes
        serializer.save(user=self.request.user)
  

class TagViewSet(BaseRecipeViewSet):
    #manejar los tags en la base de datos
    queryset = Tag.objects.all()
    serializer_class = serializers.TagSerializer


class IngredientViewSet(BaseRecipeViewSet):
    #manejar los tags en la base de datos
    queryset = Ingredient.objects.all()
    serializer_class = serializers.IngredientSerializer


class RecipeViewSet(viewsets.ModelViewSet):
    #manejar las recetas en la base de datos
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    queryset = Recipe.objects.all()
    serializer_class = serializers.RecipeSerializer

    def get_queryset(self):
        #retornar objetos para el usuario autenticado
        return self.queryset.filter(user=self.request.user)

    def get_serializer_class(self):
        #retorna el serializador adecuado
        if self.action == 'retrieve':
            return serializers.RecipeSerializer

        return self.serializer_class
    
