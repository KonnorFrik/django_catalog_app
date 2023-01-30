from rest_framework import viewsets
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.reverse import reverse
from . import models
from . import serializers
from . import my_permissions
from django.contrib.auth.models import User



@api_view(["GET"])
def api_root(request):
    return Response({"usernotes": reverse("usernote-list", request=request),
                     "users": reverse("user-list", request=request)})


class UserNoteViewSet(viewsets.ModelViewSet):
    queryset = models.UserNote.objects.all()
    serializer_class = serializers.UserNoteSerializer
    permission_classes = [permissions.IsAuthenticated, my_permissions.IsOwner]


class TextNoteViewSet(viewsets.ModelViewSet):
    queryset = models.TextNote.objects.all()
    serializer_class = serializers.TextNoteSerializer
    permission_classes = [permissions.IsAuthenticated, my_permissions.IsOwner]


class AnyFileViewSet(viewsets.ModelViewSet):
    queryset = models.AnyFile.objects.all()
    serializer_class = serializers.AnyFileSerializer
    permission_classes = [permissions.IsAuthenticated, my_permissions.IsOwner]


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = serializers.UserSerializer
    permission_classes = [permissions.IsAuthenticated, my_permissions.IsOwner]
