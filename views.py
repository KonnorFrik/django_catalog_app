import django.http
from django.http import HttpResponseRedirect
from django.shortcuts import render, reverse, get_object_or_404
from django.contrib.auth import logout  # , login, authenticate
from django.contrib.auth.decorators import login_required  # ,  permission_required
# from django.views import generic
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned

from . import forms
from . import models
from . import logic

# TODO : Cancel the create operation on error


def index(req: django.http.HttpRequest):
    return render(request=req, template_name="info/index.html")


def registration_loin(req: django.http.HttpRequest):
    if req.method == "POST":
        form = forms.RegistrationLoginForm(req.POST)

        if form.is_valid():
            username = req.POST.get("username")
            password = req.POST.get("password")

            try:
                type_ = req.POST.get('submit_data_button')

            except AttributeError:
                context = {"form": form, 'message': "Unknown Error\nTry again"}
                return render(request=req, template_name="user/auth/reg_login_get_data.html", context=context)

            if type_ == "Registration":
                if logic.create_new_user(username=username, password=password):

                    if user := logic.auth_and_login(request=req, username=username, password=password):
                        return HttpResponseRedirect(reverse('catalog:user_home_page', args=(user.pk,)))  # GOOD

                    else:
                        context = {"form": form, 'message': "Can not to auto login\nTry again"}
                        return render(request=req, template_name="user/auth/reg_login_get_data.html", context=context)

                else:
                    context = {"form": form, 'message': "User already exists"}
                    return render(request=req, template_name="user/auth/reg_login_get_data.html", context=context)

            elif type_ == "Login":
                if user := logic.auth_and_login(request=req, username=username, password=password):
                    return HttpResponseRedirect(reverse('catalog:user_home_page', args=(user.pk,)))  # GOOD

                else:
                    context = {"form": form, 'message': "Can not login. Try again"}
                    return render(request=req, template_name="user/auth/reg_login_get_data.html", context=context)

            else:
                context = {"form": form, 'message': "Unknown Error\nTry again"}
                return render(request=req, template_name="user/auth/reg_login_get_data.html", context=context)

        else:
            context = {"form": form, 'message': "Invalid form"}
            return render(request=req, template_name="user/auth/reg_login_get_data.html", context=context)

    else:
        form = forms.RegistrationLoginForm()
        context = {"form": form, 'message': "Welcome"}
        return render(request=req, template_name="user/auth/reg_login_get_data.html", context=context)


@login_required(redirect_field_name="", login_url="/catalog/account/registration_login/")
def logout_user(req: django.http.HttpRequest):
    logout(request=req)
    return HttpResponseRedirect(reverse("catalog:registration_loin"))


@login_required(redirect_field_name="", login_url="/catalog/account/registration_login/")
def user_home_page(req: django.http.HttpRequest, pk: int):
    try:
        message = req.session['message']

    except Exception:
        message = ""

    user = get_object_or_404(models.IUser, pk=pk)
    context = {'user': user, 'message': message}
    return render(request=req, template_name="user/home_page.html", context=context)


@login_required(redirect_field_name="", login_url="/catalog/account/registration_login/")
def add_user_content(req: django.http.HttpRequest, pk: int):
    if req.method == "POST":
        form = forms.UserNoteForm(req.POST)
        # form.file_form = forms.AnyFileForm(req.POST, req.FILES)

        if form.is_valid():  # and form.file_form.is_valid():

            if logic.create_user_note(request=req):
                return HttpResponseRedirect(reverse('catalog:user_home_page', args=(req.user.pk,)))

            else:
                context = {'form': form, 'id': pk, 'message': "Unknown error\nPlease try again"}
                return render(request=req, template_name="file/add_user_content.html", context=context)

        else:
            context = {'form': form, 'id': pk, 'message': "Invalid form"}
            return render(request=req, template_name="file/add_user_content.html", context=context)

    else:
        form = forms.UserNoteForm()
        context = {'form': form, 'id': pk}
        return render(request=req, template_name="file/add_user_content.html", context=context)


@login_required(redirect_field_name="", login_url="/catalog/account/registration_login/")
def user_note_detail(req: django.http.HttpRequest, pk: int, note_id: int):
    try:
        user = req.user
        user_note = get_object_or_404(models.UserNote, pk=note_id)

        try:
            message = req.session['message']

        except KeyError:
            message = ""

    except ObjectDoesNotExist:
        message = "Unknown error :c"
        context = {'message': message}
        return render(request=req, template_name="user/user_note_detail.html", context=context)

    else:
        contex = {'note': user_note, 'user': user, 'message': message}
        return render(request=req, template_name="user/user_note_detail.html", context=contex)


@login_required(redirect_field_name="", login_url="/catalog/account/registration_login/")
def add_file_for_note(req: django.http.HttpRequest, pk: int, note_id: int):
    if req.method == "POST":
        # print(f"REQ FILES: {req.FILES}")
        try:
            user_note = get_object_or_404(models.UserNote, pk=note_id)

        except (ObjectDoesNotExist, MultipleObjectsReturned):
            message = "Unknown error :c"
            form = forms.AnyFileForm()
            user = req.user
            context = {'form': form, 'user': user, 'message': message}
            return render(request=req, template_name="file/add_file_for_note.html", context=context)

        else:
            if logic.add_file_for_note(req, user_note):
                return HttpResponseRedirect(reverse('catalog:user_note_detail', args=(req.user.pk, note_id)))  # GOOD

            else:
                message = "Can't add a file"
                user = req.user
                form = forms.AnyFileForm()
                context = {'note': user_note, 'form': form, 'user': user, 'message': message}
                return render(request=req, template_name="file/add_file_for_note.html", context=context)

    else:

        try:
            user = req.user
            user_note = get_object_or_404(models.UserNote, pk=note_id)
            form = forms.AnyFileForm()

        except django.http.Http404:
            user = req.user
            form = forms.AnyFileForm()
            message = "Unknown error :c"
            context = {'message': message, 'form': form, 'user': user}
            return render(request=req, template_name="file/add_file_for_note.html", context=context)

        else:
            contex = {'form': form, 'note': user_note, 'user': user}
            return render(request=req, template_name="file/add_file_for_note.html", context=contex)


@login_required(redirect_field_name="", login_url="/catalog/account/registration_login/")
def add_text_for_note(req: django.http.HttpRequest, pk: int, note_id: int):
    if req.method == "POST":
        try:
            user_note = get_object_or_404(models.UserNote, pk=note_id)

        except (ObjectDoesNotExist, MultipleObjectsReturned):
            message = "Unknown error :c"
            form = forms.TextNoteForm()
            user = req.user
            context = {'form': form, 'user': user, 'message': message}
            return render(request=req, template_name="file/add_text_for_note.html", context=context)

        else:
            if logic.add_text_for_note(req, user_note):
                return HttpResponseRedirect(reverse('catalog:user_note_detail', args=(req.user.pk, note_id)))  # GOOD

            else:
                message = "Can't add a text"
                user = req.user
                form = forms.TextNoteForm(req.POST)
                context = {'note': user_note, 'form': form, 'user': user, 'message': message}
                return render(request=req, template_name="file/add_text_for_note.html", context=context)

    else:
        try:
            user_note = get_object_or_404(models.UserNote, pk=note_id)
            form = forms.TextNoteForm()

        except django.http.Http404:
            form = forms.TextNoteForm()
            message = "Unknown error :c"
            context = {'message': message, 'form': form, 'user': req.user}
            return render(request=req, template_name="file/add_text_for_note.html", context=context)

        else:
            context = {'user': req.user, 'form': form, 'note': user_note}
            return render(request=req, template_name="file/add_text_for_note.html", context=context)


@login_required(redirect_field_name="", login_url="/catalog/account/registration_login/")
def show_user_text(req: django.http.HttpRequest, pk: int, note_id: int, text_id: int):
    try:
        text_obj = get_object_or_404(models.TextNote, id=text_id)

    except Exception as e:
        message = "Unknown Error :c"
        # context = {'user': req.user, 'message': message, }
        req.session['message'] = message
        return HttpResponseRedirect(reverse('catalog:user_note_detail', args=(req.user.pk, note_id)))

    else:
        context = {'user': req.user, 'text': text_obj}
        return render(request=req, template_name="user/user_text_full.html", context=context)


@login_required(redirect_field_name="", login_url="/catalog/account/registration_login/")
def download_user_file(req: django.http.HttpRequest, pk: int, file_id: int):
    if response := logic.get_download_file_response(file_id=file_id):
        return response

    else:
        return django.http.HttpResponseRedirect(reverse('catalog:user_home_page', args=(req.user.pk,)))


@login_required(redirect_field_name="", login_url="/catalog/account/registration_login/")
def delete_file_from_note(req: django.http.HttpRequest, pk: int, file_id: int):
    try:
        file_obj = models.AnyFile.objects.get(id=file_id)
        note_id = file_obj.user_note.id
        file_obj.delete()

    except Exception:
        req.session['message'] = "Error on delete file"
        return django.http.HttpResponseRedirect(reverse('catalog:user_home_page', args=(req.user.pk, )))

    else:
        return django.http.HttpResponseRedirect(reverse('catalog:user_note_detail', args=(req.user.pk, note_id,)))


@login_required(redirect_field_name="", login_url="/catalog/account/registration_login/")
def delete_text_from_note(req: django.http.HttpRequest, pk: int, text_id: int):
    try:
        text_obj = models.TextNote.objects.get(id=text_id)
        note_id = text_obj.user_note.id
        text_obj.delete()

    except Exception:
        req.session['message'] = "Error on delete file"
        return django.http.HttpResponseRedirect(reverse('catalog:user_home_page', args=(req.user.pk,)))

    else:
        return django.http.HttpResponseRedirect(reverse('catalog:user_note_detail', args=(req.user.pk, note_id,)))


@login_required(redirect_field_name="", login_url="/catalog/account/registration_login/")
def delete_user_note(req: django.http.HttpRequest, pk: int, note_id: int):
    try:
        note_obj = get_object_or_404(models.UserNote, id=note_id)
        note_obj.delete()

    except Exception:
        req.session['message'] = "Error on delete note"
        return django.http.HttpResponseRedirect(reverse('catalog:user_home_page', args=(req.user.id,)))

    else:
        return django.http.HttpResponseRedirect(reverse('catalog:user_home_page', args=(req.user.id,)))


def test_(req: django.http.HttpRequest, filename: str):

    try:
        print()
        print(f"REQ USER: {req.user}")
        print(f"REQ USER ID: {req.user.id}")
        print(f"REQ USER TYPE: {type(req.user)}")
        print()
        print(f"REQ METHOD: {req.method}")
        print(f"REQ POST: {req.POST}")
        print(f"REQ GET: {req.GET}")
        print(f"REQ FILES: {req.FILES}")
        print(f"REQ RAW: {req}")
        print()
        print(f"FILENAME: {filename}")

        # files_form = AnyFileForm(req.POST, req.FILES)
        # print(f"FILE FORM: {files_form.data.get('title')}")

        # print(f"REQ Username: {req.POST.get('username')}")
        # print(f"REQ Password: {req.POST.get('password')}")

        # print(f"REG/LOG TYPE: {req.POST.get('submit_data_button')}")

    except AttributeError as e:
        print(f"ERROR: {e}")
    # return HttpResponseRedirect(reverse('catalog:registration_loin'))
    print()
