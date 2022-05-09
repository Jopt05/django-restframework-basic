from rest_framework import permissions


class UpdateOwnProfile(permissions.BasePermission):
    """ Permite al usuario editar su propio perfil """

    def has_object_permission(self, request, view, obj):
        """ Chequear si usuario está intentando editar su propio perfil """
        if request.method in permissions.SAFE_METHODS:
            return True

        """ Chequear si el ID del usuario coincide con el que quiere actualizar"""
        return obj.id == request.user.id


class UpdateOwnStatus(permissions.BasePermission):
    """ Permite actualizar propio status feed """

    def has_object_permission(self, request, view, obj):
        """ Chequear si usuario está intentando editar su propio feed """
        if request.method in permissions.SAFE_METHODS:
            return True

        """ Chequear si el ID del usuario coincide con el que quiere actualizar"""
        return obj.user_profile_id == request.user.id
