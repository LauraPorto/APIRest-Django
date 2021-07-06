from django.contrib.auth import get_user_model, authenticate
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers

class UserSerializer(serializers.ModelSerializer):
    #Serializador para el objeto de usuarios
    class Meta:
        model = get_user_model()
        fields = ('email', 'password', 'name')
        extra_kwargs = {'password':{'write_only': True, 'min_length': 5}}

    def create(self, validated_data):
        #Creamos nuevo usuario con la clave encriptada
        return get_user_model().objects.create_user(**validated_data)

    def update(self, instance, validated_data):
        #actualiza el usuario, configura el password y lo retorna
        password = validated_data.pop('password', None)
        user = super().update(instance, validated_data)

        if password:
            user.set_password(password)
            user.save()
        
        return user

class AuthTokenSerializer(serializers.Serializer):
    #serializador para el objeto de autenticación del usuario
    email = serializers.CharField()
    password = serializers.CharField(
        style={'input_type': 'password'},
        trim_whitespace=False
    )

    def validate(self, attrs):
        #validar o autenticar el usuarios
        email = attrs.get('email')
        password = attrs.get('password')

        user = authenticate(
            request=self.context.get('request'),
            username = email,
            password = password
        )
        if not user:
            msg = _('Unable to authenticate with provided credentials')
            raise serializers.ValidationError(msg, code='authorization')

        attrs['user'] = user
        return attrs