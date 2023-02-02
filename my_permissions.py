from rest_framework import permissions

class IsOwner(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        return obj.user == request.user

class AllowAnyNotList(permissions.BasePermission):

    def has_permission(self, request, view):
        if view.action == "list":
            return False

        return True

