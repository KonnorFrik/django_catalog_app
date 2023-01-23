from rest_framework import serializers
from . import models
from django.contrib.auth.models import User


class UserNoteSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name='catalog:usernote-detail',
        read_only=True)

    text_notes = serializers.HyperlinkedRelatedField(
        many=True,
        read_only=True,
        view_name='catalog:textnote-detail',
        source='textnote_set')

    files = serializers.HyperlinkedRelatedField(
        many=True,
        read_only=True,
        view_name='catalog:file-detail',
        source='anyfile_set')

    class Meta:
        model = models.UserNote
        fields = ('id',
                  'note_title',
                  'note_description',
                  'url',
                  'text_notes',
                  'files')


class TextNoteSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name='catalog:textnote-detail',
        read_only=True)

    class Meta:
        model = models.TextNote
        fields = ('id',
                  'txt_title',
                  'txt_text',
                  'pub_date',
                  'user_note',
                  'url')


class AnyFileSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name='catalog:file-detail',
        read_only=True)

    class Meta:
        model = models.AnyFile
        fields = ('id',
                  'title',
                  'pub_date',
                  'user_note',
                  'url')


class UserSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name='catalog:user-detail',
        read_only=True)

    notes = serializers.HyperlinkedRelatedField(
        many=True,
        read_only=True,
        view_name='catalog:usernote-detail',
        source='usernote_set')

    class Meta:
        model = User
        fields = ('id',
                  'username',
                  'url',
                  'notes')
