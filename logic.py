import django.http

from . import models
from . import forms
from binaryornot.check import is_binary

import mimetypes

from django.shortcuts import get_object_or_404, reverse
from django.contrib import auth
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404
from django.conf import settings


def create_new_user(username: str, password: str) -> bool:
    try:
        models.User.objects.create_user(username=username, password=password)

    except Exception:
        result = False

    else:
        result = True

    return result


def login(request: django.http.HttpRequest, username: str, password: str) -> User | bool:
    try:
        user = auth.authenticate(username=username, password=password)
        auth.login(request=request, user=user)

    except AttributeError:
        return False

    return user


def create_user_note(request: django.http.HttpRequest) -> bool:
    try:

        # get params for UserNote obj which create below
        note_title = request.POST.get('note_title')
        note_description = request.POST.get("note_description")

        # create UserNote obj
        user = get_object_or_404(models.User, username=request.user.username)  # Need User instance, NOT LazyObj
        note_obj = models.UserNote.objects.create(note_title=note_title, note_description=note_description, user=user)

    except KeyError as e:

        try:
            note_obj.delete()

        except Exception as e:  # NameError, and mb ValueError
            return False

        return False

    else:
        return True


def add_file_for_note(request: django.http.HttpRequest, note_obj: models.UserNote) -> bool:
    file_form = forms.AnyFileForm(request.POST, request.FILES)

    if not file_form.is_valid():
        return False

    try:
        file_obj = file_form.save()

    except Http404:
        return False

    else:
        note_obj.anyfile_set.add(file_obj)
        return True


def add_text_for_note(request: django.http.HttpRequest, note_obj: models.UserNote) -> bool:
    text_form = forms.TextNoteForm(request.POST, request.FILES)

    if not text_form.is_valid():
        return False

    title = text_form.data.get('txt_title') or ""
    text = text_form.data.get('txt_text')

    try:
        text_obj = models.TextNote.objects.create(txt_title=title, txt_text=text, user_note=note_obj)

    except Exception as e:
        return False

    else:
        return True


def get_download_file_response(file_id: int) -> django.http.HttpResponse | bool:
    try:
        # get file_obj and prepare it
        file_obj = get_object_or_404(models.AnyFile, pk=file_id)
        file_name = str(file_obj.file)

        if len(splitted := file_name.split('.')) > 1:
            file_ext = '.' + splitted[-1]

        else:
            file_ext = ""

        # define a abs_path to file
        file_path = settings.MEDIA_ROOT + '/' + file_name

        if is_binary(file_path):
            path_ = open(file_path, 'rb')  # HttpResponse constructor need a fd

        else:
            path_ = open(file_path, 'r')
            file_ext = file_ext or '.txt'

        # define a mimetype for response headers below
        mime_type, _ = mimetypes.guess_type(file_path)

    except (ObjectDoesNotExist, Http404):
        return False

    else:
        response = django.http.HttpResponse(path_, content_type=mime_type)
        response['Content-Disposition'] = f"attachment; filename={file_obj.title + file_ext}"
        return response

