from rest_framework import serializers

from profiles_api import models


class HelloSerializer(serializers.Serializer):
    """ Serializa un campo para probar nuestro APIView """
    name = serializers.CharField(max_length=10)


class UserProfileSerializer(serializers.ModelSerializer):
    """ Serializa objeto de perfil de usuario """

    """ Se llama class meta """
    class Meta:
        model = models.UserProfile
        fields = ('id', 'name', 'email', 'password')
        extra_kwargs = {
            'password': {
                'write_only': True,
                'style': {
                    'input_type': 'password'
                }
            }
        }

    """ Sobreescribimos una función, en este caso create """

    def create(self, validated_data):
        """ Crear y retornar un usuario """
        user = models.UserProfile.objects.create_user(
            email=validated_data['email'],
            name=validated_data['name'],
            password=validated_data['password']
        )

        return user

    def update(self, instance, validated_data):
        """ Actualiza cuenta de usuario """
        if 'password' in validated_data:
            password = validated_data.pop('password')
            instance.set_password(password)

        return super().update(instance, validated_data)


class ProfileFeedItemSerializer(serializers.ModelSerializer):
    """ Serializador de un item de feed """

    class Meta:
        model = models.ProfileFeedItem
        fields = ('id', 'status_text', 'created_on', 'user_profile')
        extra_kwargs = {
            'user_profile': {
                'read_only': True
            }
        }
