from django.shortcuts import render
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from core.models import Tag 

from recipe import serializers
# Create your views here.

class TagViewSet(viewsets.GenericViewSet, mixins.ListModelMixin):
    #manejar los tags en la base de datos
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    queryset = Tag.objects.all()
    serializers_class = serializers.TagSerializer