import django.http
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, reverse, get_object_or_404
from django.contrib.auth import logout  # , login, authenticate
from django.contrib import auth
from django.contrib.auth.decorators import login_required  # ,  permission_required
# from django.views import generic
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned

from . import serializers
from . import forms
from . import models
from . import logic


def index(request: django.http.HttpRequest):
    try:
        user = get_object_or_404(auth.models.User, id=request.user.id)

    except django.http.Http404:
        user = None

    context = {'user': user}
    return render(request=request, template_name="info/index.html", context=context)


def login(request: django.http.HttpRequest):
    login_html_template = "user/auth/login.html"

    if not request.method == "POST":
        form = forms.LoginForm()
        context = {"form": form, 'message': "Welcome"}
        return render(request=request, template_name=login_html_template, context=context)

    form = forms.LoginForm(request.POST)

    if not form.is_valid():
        context = {"form": form, 'message': "Invalid Login or Password\nTry again"}
        return render(request=request, template_name=login_html_template, context=context)

    username = request.POST.get("username")
    password = request.POST.get("password")

    user = logic.login(request=request, username=username, password=password)

    if not user:
        context = {"form": form, 'message': "Can not login. Try again"}
        return render(request=request, template_name=login_html_template, context=context)

    return HttpResponseRedirect(reverse('catalog:user_home_page', args=(user.id,)))  # GOOD


def registration(request: django.http.HttpRequest):
    template_name = "user/auth/registration.html"

    if not request.method == "POST":
        form = forms.RegistrationForm()
        context = {"form": form, 'message': "Welcome"}
        return render(request=request, template_name=template_name, context=context)

    form = forms.RegistrationForm(request.POST)

    if not form.is_valid():
        context = {"form": form, 'message': "Invalid form"}
        return render(request=request, template_name=template_name, context=context)

    username = request.POST.get("username")
    password = request.POST.get("password")

    if not logic.create_new_user(username=username, password=password):
        context = {"form": form, 'message': "This name already taken"}
        return render(request=request, template_name=template_name, context=context)


    user = logic.login(request=request, username=username, password=password)

    if not user:
        context = {"form": form, 'message': "Can not to auto login\nTry again"}
        return render(request=request, template_name=template_name, context=context)

    return HttpResponseRedirect(reverse('catalog:user_home_page', args=(user.id,)))  # GOOD


@login_required(redirect_field_name="", login_url="/catalog/account/login/")
def logout_user(request: django.http.HttpRequest):
    logout(request=request)
    return HttpResponseRedirect(reverse("catalog:login"))


@login_required(redirect_field_name="", login_url="/catalog/account/login/")
def user_home_page(request: django.http.HttpRequest, user_id: int):
    try:
        message = request.session['message']
        request.session['message'] = ""

    except Exception:
        message = ""

    user = get_object_or_404(models.User, id=user_id)
    context = {'user': user, 'message': message}
    return render(request=request, template_name="user/home_page.html", context=context)


@login_required(redirect_field_name="", login_url="/catalog/account/login/")
def add_user_content(request: django.http.HttpRequest, user_id: int):
    template_name = "file/add_user_content.html"

    if not request.method == "POST":
        form = forms.UserNoteForm()
        context = {'form': form, 'id': user_id}
        return render(request=request, template_name=template_name, context=context)

    form = forms.UserNoteForm(request.POST)

    if not form.is_valid():
        context = {'form': form, 'id': user_id, 'message': "Invalid form"}
        return render(request=request, template_name=template_name, context=context)

    if not logic.create_user_note(request=request):
        context = {'form': form, 'id': user_id, 'message': "Unknown error. Please try again"}
        return render(request=request, template_name=template_name, context=context)

    return HttpResponseRedirect(reverse('catalog:user_home_page', args=(request.user.id,)))


@login_required(redirect_field_name="", login_url="/catalog/account/login/")
def user_note_detail(request: django.http.HttpRequest, user_id: int, note_id: int):
    template_name = "user/user_note_detail.html"

    try:
        user = request.user
        user_note = get_object_or_404(models.UserNote, id=note_id)

        try:
            message = request.session['message']
            request.session['message'] = ""

        except KeyError:
            message = ""

    except ObjectDoesNotExist:
        message = "Unknown error :c"
        context = {'message': message}
        return render(request=request, template_name=template_name, context=context)

    else:
        contex = {'note': user_note, 'user': user, 'message': message}
        return render(request=request, template_name=template_name, context=contex)


# TODO refactor this
@login_required(redirect_field_name="", login_url="/catalog/account/login/")
def add_file_for_note(request: django.http.HttpRequest, user_id: int, note_id: int):
    template_name = "file/add_file_for_note.html"

    if not request.method == "POST":
        try:
            user = request.user
            user_note = get_object_or_404(models.UserNote, id=note_id)
            form = forms.AnyFileForm()

        except django.http.Http404:
            user = request.user
            form = forms.AnyFileForm()
            message = "Unknown error :c"
            context = {'message': message, 'form': form, 'user': user}
            return render(request=request, template_name=template_name, context=context)

        else:
            contex = {'form': form, 'note': user_note, 'user': user}
            return render(request=request, template_name=template_name, context=contex)

    try:
        user_note = get_object_or_404(models.UserNote, id=note_id)

    except (ObjectDoesNotExist, MultipleObjectsReturned):
        message = "Unknown error :c"
        form = forms.AnyFileForm()
        user = request.user
        context = {'form': form, 'user': user, 'message': message}
        return render(request=request, template_name=template_name, context=context)

    else:
        if not logic.add_file_for_note(request, user_note):
            message = "Can't add a file"
            user = request.user
            form = forms.AnyFileForm()
            context = {'note': user_note, 'form': form, 'user': user, 'message': message}
            return render(request=request, template_name=template_name, context=context)

        return HttpResponseRedirect(reverse('catalog:user_note_detail', args=(request.user.id, note_id)))  # GOOD


@login_required(redirect_field_name="", login_url="/catalog/account/login/")
def add_text_for_note(request: django.http.HttpRequest, user_id: int, note_id: int):
    template_name = "file/add_text_for_note.html"

    if not request.method == "POST":
        try:
            user_note = get_object_or_404(models.UserNote, id=note_id)
            form = forms.TextNoteForm()

        except django.http.Http404:
            form = forms.TextNoteForm()
            message = "Unknown error :c"
            context = {'message': message, 'form': form, 'user': request.user}
            return render(request=request, template_name=template_name, context=context)

        else:
            context = {'user': request.user, 'form': form, 'note': user_note}
            return render(request=request, template_name=template_name, context=context)

    try:
        user_note = get_object_or_404(models.UserNote, id=note_id)

    except (ObjectDoesNotExist, MultipleObjectsReturned):
        message = "Unknown error :c"
        form = forms.TextNoteForm()
        user = request.user
        context = {'form': form, 'user': user, 'message': message}
        return render(request=request, template_name=template_name, context=context)

    else:
        if not logic.add_text_for_note(request, user_note):
            message = "Can't add a text"
            user = request.user
            form = forms.TextNoteForm(request.POST)
            context = {'note': user_note, 'form': form, 'user': user, 'message': message}
            return render(request=request, template_name=template_name, context=context)

        return HttpResponseRedirect(reverse('catalog:user_note_detail', args=(request.user.id, note_id)))  # GOOD


@login_required(redirect_field_name="", login_url="/catalog/account/login/")
def show_user_text(request: django.http.HttpRequest, user_id: int, note_id: int, text_id: int):
    try:
        text_obj = get_object_or_404(models.TextNote, id=text_id)

    except Exception as e:
        message = "Unknown Error :c"
        # context = {'user': request.user, 'message': message, }
        request.session['message'] = message
        return HttpResponseRedirect(reverse('catalog:user_note_detail', args=(request.user.id, note_id)))

    else:
        context = {'user': request.user, 'text': text_obj}
        return render(request=request, template_name="user/user_text_full.html", context=context)


@login_required(redirect_field_name="", login_url="/catalog/account/login/")
def download_user_file(request: django.http.HttpRequest, user_id: int, file_id: int):
    response = logic.get_download_file_response(file_id=file_id)

    if not response :
        return django.http.HttpResponseRedirect(reverse('catalog:user_home_page', args=(request.user.id,)))

    return response


@login_required(redirect_field_name="", login_url="/catalog/account/login/")
def delete_file_from_note(request: django.http.HttpRequest, user_id: int, note_id: int, file_id: int):
    reverse_name = 'catalog:user_home_page'

    if not request.method == "POST":
        request.session['message'] = "Something wrong with method"
        return django.http.HttpResponseRedirect(reverse(reverse_name, args=(request.user.id,)))

    if not request.POST.get("_method", "").lower() == 'delete':
        request.session['message'] = "Something wrong"
        return django.http.HttpResponseRedirect(reverse(reverse_name, args=(request.user.id,)))

    try:
        file_obj = models.AnyFile.objects.get(id=file_id)
        #note_id = file_obj.user_note.id
        file_obj.delete()

    except Exception:
        request.session['message'] = "Error on delete file"
        return django.http.HttpResponseRedirect(reverse(reverse_name, args=(request.user.id, )))

    else:
        return django.http.HttpResponseRedirect(reverse('catalog:user_note_detail', args=(request.user.id, note_id,)))


@login_required(redirect_field_name="", login_url="/catalog/account/login/")
def delete_text_from_note(request: django.http.HttpRequest, user_id: int, note_id: int, text_id: int):
    reverse_name = 'catalog:user_home_page'

    if not request.method == "POST":
        request.session['message'] = "Something wrong with method"
        return django.http.HttpResponseRedirect(reverse(reverse_name, args=(request.user.id,)))

    if not request.POST.get("_method", "").lower() == 'delete':
        request.session['message'] = "Something wrong"
        return django.http.HttpResponseRedirect(reverse(reverse_name, args=(request.user.id,)))

    try:
        text_obj = models.TextNote.objects.get(id=text_id)
        #note_id = text_obj.user_note.id
        text_obj.delete()

    except Exception:
        request.session['message'] = "Error on delete file"
        return django.http.HttpResponseRedirect(reverse(reverse_name, args=(request.user.id,)))

    else:
        return django.http.HttpResponseRedirect(reverse('catalog:user_note_detail', args=(request.user.id, note_id,)))


@login_required(redirect_field_name="", login_url="/catalog/account/login/")
def delete_user_note(request: django.http.HttpRequest, user_id: int, note_id: int):
    reverse_name = 'catalog:user_home_page'

    if not request.method == "POST":
        request.session['message'] = "Something wrong with method"
        return django.http.HttpResponseRedirect(reverse(reverse_name, args=(request.user.id,)))

    if not request.POST.get("_method", "").lower() == 'delete':
        request.session['message'] = "Something wrong"
        return django.http.HttpResponseRedirect(reverse(reverse_name, args=(request.user.id,)))

    try:
        note_obj = get_object_or_404(models.UserNote, id=note_id)
        note_obj.delete()

    except Exception:
        request.session['message'] = "Error on delete note"
        return django.http.HttpResponseRedirect(reverse(reverse_name, args=(request.user.id,)))

    else:
        return django.http.HttpResponseRedirect(reverse(reverse_name, args=(request.user.id,)))


@login_required(redirect_field_name="", login_url="/catalog/account/login/")
def edit_text_from_note(request: django.http.HttpRequest, user_id: int, note_id: int, text_id: int):
    try:
        text_note_obj = get_object_or_404(models.TextNote, id=text_id)

    except models.TextNote.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == "GET":
        try:
            message = request.session['message']
            request.session['message'] = ""

        except Exception:
            message = ""

        serialized_text_obj = serializers.TextNoteSerializer(text_note_obj, context={'request': request})

        text_form = forms.TextNoteForm(serialized_text_obj.data)

        context = {"form": text_form, 'user': request.user, 'message': message or "Edit you'r note"}
        return render(request=request, template_name='file/edit_text_for_note.html', context=context)

    if not request.POST.get("_method", "").lower() == 'put':
        request.session['message'] = "Something wrong"
        return django.http.HttpResponseRedirect(reverse('catalog:edit_text_from_note', args=(request.user.id, note_id, text_id)))

    serialized_obj = serializers.TextNoteSerializer(text_note_obj, data=request.POST)

    if serialized_obj.is_valid():
        serialized_obj.save()
        return HttpResponseRedirect(reverse("catalog:user_note_detail", args=(request.user.id, note_id)))


@login_required(redirect_field_name="", login_url="/catalog/account/login/")
def edit_file_from_note(request: django.http.HttpRequest, user_id: int, note_id: int, file_id: int):
    try:
        file_note_obj = get_object_or_404(models.AnyFile, id=file_id)

    except models.AnyFile.DoesNotExist:
        return HttpResponse(status=404)


    if request.method == "GET":
        try:
            message = request.session['message']
            request.session['message'] = ""

        except Exception:
            message = ""

        serialized_file_obj = serializers.AnyFileSerializer(file_note_obj, context={'request': request})

        #print(f"\n{serialized_file_obj.data}\n")

        file_form = forms.AnyFileForm(serialized_file_obj.data)

        context = {"form": file_form, 'user': request.user, 'message': message or "Edit you'r file"}
        return render(request=request, template_name='file/edit_file_for_note.html', context=context)

    if not request.POST.get("_method", "").lower() == 'put':
        request.session['message'] = "Something wrong"
        return django.http.HttpResponseRedirect(reverse('catalog:edit_file_from_note', args=(request.user.id, note_id, file_id)))

    serialized_obj = serializers.AnyFileSerializer(file_note_obj, data=request.POST)

    if serialized_obj.is_valid():
        serialized_obj.save()
        print("\nSAVED, go to detail page\n")
        return HttpResponseRedirect(reverse("catalog:user_note_detail", args=(request.user.id, note_id)))


#def test_(request: django.http.HttpRequest, filename: str):
#
    #try:
        #print()
        #print(f"REQ USER: {request.user}")
        #print(f"REQ USER ID: {request.user.id}")
        #print(f"REQ USER TYPE: {type(request.user)}")
        #print()
        #print(f"REQ METHOD: {request.method}")
        #print(f"REQ POST: {request.POST}")
        #print(f"REQ GET: {request.GET}")
        #print(f"REQ FILES: {request.FILES}")
        #print(f"REQ RAW: {request}")
        #print()
        #print(f"FILENAME: {filename}")
#
        ## files_form = AnyFileForm(request.POST, request.FILES)
        ## print(f"FILE FORM: {files_form.data.get('title')}")
#
        ## print(f"REQ Username: {request.POST.get('username')}")
        ## print(f"REQ Password: {request.POST.get('password')}")
#
        ## print(f"REG/LOG TYPE: {request.POST.get('submit_data_button')}")
#
    #except AttributeError as e:
        #print(f"ERROR: {e}")
    ## return HttpResponseRedirect(reverse('catalog:registration_loin'))
    #print()
