from rest_framework import generics, authentication, permissions
from user.serializers import UserSerializer, AuthTokenSerializer
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings

# Create your views here.
class CreateUserView(generics.CreateAPIView):
    #Crear un nuevo usuario en el sistema
    serializer_class = UserSerializer

class CreateTokenView(ObtainAuthToken):
    #Crear nuevo auth token para usuarios
    serializer_class = AuthTokenSerializer
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES

class ManageUserView(generics.RetrieveUpdateAPIView):
    #manejar el usuario autenticado 
    serializer_class = UserSerializer
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def get_object(self):
        #obtener y retornar usuario autenticado
        return self.request.user
