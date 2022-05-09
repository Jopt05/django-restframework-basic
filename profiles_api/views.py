from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, filters
from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings
from rest_framework.permissions import IsAuthenticated

from profiles_api import serializers, models, permissions
# Create your views here.


class HeloApiView(APIView):
    """ API View de prueba """

    """ Clase de hello serializer """
    serializer_class = serializers.HelloSerializer

    def get(self, request, format=None):
        """ Retornar lista de características del APIView """

        an_apiview = [
            'Usamos metodos HTTP como funciones',
            'Es similar a una vista tradicional de Django',
            'Nos da el mejor control sobre la lógica de nuestra aplicación'
        ]

        """ Convierte la info en formato Json
        Puede ser una lista o un diccionario """
        return Response({
            'message': 'Hello World',
            'an_apiview': an_apiview
        })

    def post(self, request):
        """ Crea un mensjae con nuestro nombre """

        serializer = self.serializer_class(data=request.data)

        """ Permite validar la información """
        if serializer.is_valid():
            name = serializer.validated_data.get('name')
            message = f'Hello {name}'
            return Response({
                'message': message
            })
        else:
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )

    def put(self, request, pk=None):
        """ Maneja actualizar un objeto """

        return Response({
            'method': 'PUT'
        })

    def patch(self, request, pk=None):
        """ Maneja actualización parcial de un objeto """

        return Response({
            'method': 'PATCH'
        })

    def delete(self, request, pk=None):
        """ Maneja borrado de un objeto """

        return Response({
            'method': 'DELETE'
        })


class HelloViewSet(viewsets.ViewSet):
    """ Test API Viewset """
    serializer_class = serializers.HelloSerializer

    def list(self, request):
        """ Retornar mensaje de hola mundo """

        a_viewset = [
            'Usa acciones (list, create, retrieve)',
            'Automáticamente mapea a los URL usando routers',
            'Provee funcionalidad con menos código'
        ]

        return Response({
            'message': 'Hola!',
            'a_viewset': a_viewset
        })

    def create(self, request):
        """ Crear un nuevo mensaje de hola mundo """
        serializer = self.serializer_class(data=request.data)

        """ Permite validar la información """
        if serializer.is_valid():
            name = serializer.validated_data.get('name')
            message = f'Hello {name}'
            return Response({
                'message': message
            })
        else:
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )

    def retrieve(self, request, pk=None):
        """ Obtiene un objeto y su ID """

        return Response({
            'http_method:' 'GET'
        })

    def update(self, request, pk=None):
        """ Actualiza un objeto """

        return Response({
            'http_method:' 'PUT'
        })

    def update(self, request, pk=None):
        """ Actualiza parcialmente el objeto """

        return Response({
            'http_method:' 'PATCH'
        })

    def destroy(self, request, pk=None):
        """ Destruye un objeto """

        return Response({
            'http_method:' 'DELETE'
        })


class UserProfileViewSet(viewsets.ModelViewSet):
    """ Crear y actualizar perfiles """

    serializer_class = serializers.UserProfileSerializer
    queryset = models.UserProfile.objects.all()
    authentication_classes = (TokenAuthentication,)
    permission_classes = (permissions.UpdateOwnProfile,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name', 'email')


class UserLoginApiView(ObtainAuthToken):
    """  Crea tokens de autenticación para usuario """
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES


class UserProfileFeedViewSet(viewsets.ModelViewSet):
    """ Maneja el crear, leer y actualizar el feed """
    authentication_classes = (TokenAuthentication,)
    serializer_class = serializers.ProfileFeedItemSerializer
    queryset = models.ProfileFeedItem.objects.all()
    permission_classes = (
        permissions.UpdateOwnStatus,
        IsAuthenticated
    )

    def perform_create(self, serializer):
        """ Setea el perfil para el usuario que está logeado """
        serializer.save(user_profile=self.request.user)
