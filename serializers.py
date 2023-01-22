from rest_framework import serializers
from . import models
from django.contrib.auth.models import User


class UserNoteSerializer(serializers.HyperlinkedModelSerializer):
    #url = serializers.HyperlinkedIdentityField(view_name='user-detail', read_only=True)

    class Meta:
        model = models.UserNote
        fields = ['id', 'note_title', 'note_description']#, 'url']
        #extra_kwargs = {'url': {'lookup_field': 'user-detail'}}



class TextNoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.TextNote
        fields = ('id', 'txt_title', 'txt_text', 'pub_date', 'user_note')


class AnyFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.AnyFile
        fields = ('id', 'title', 'pub_date', 'user_note')


class UserSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = User
        fields = ('id', 'username')#, 'url')
