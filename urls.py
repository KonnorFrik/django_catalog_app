from django.urls import path, include
from . import views
from . import drf_views

from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r"usernote", drf_views.UserNoteViewSet, basename='usernote')
router.register(r"textnote", drf_views.TextNoteViewSet)
router.register(r"file", drf_views.AnyFileViewSet, basename='file')
router.register(r"users", drf_views.UserViewSet, basename='user')

app_name = "catalog"

urlpatterns = [
    path('rest/', include(router.urls), name=app_name),

    path('', views.index, name='home_page'),

    path("account/login/", views.login, name="login"),
    path("account/registration/", views.registration, name="registration"),
    path("account/logout/", views.logout_user, name="logout"),

    path("id<int:user_id>/home/", views.user_home_page, name='user_home_page'),
    path("id<int:user_id>/note/add/", views.add_user_content, name='add_user_content'),
    path("id<int:user_id>/note/<int:note_id>/view/", views.user_note_detail, name="user_note_detail"),

    path("id<int:user_id>/note/<int:note_id>/add_file/", views.add_file_for_note, name='add_file_for_note'),
    path("id<int:user_id>/note/<int:note_id>/add_text/", views.add_text_for_note, name='add_text_for_note'),

    path("id<int:user_id>/download/<int:file_id>/", views.download_user_file, name='download_user_file'),
    path("id<int:user_id>/note/<int:note_id>/file/<int:text_id>/view", views.show_user_text, name='show_user_text'),

    path("id<int:user_id>/note/<int:note_id>/file/<int:file_id>/delete/", views.delete_file_from_note, name='delete_file_from_note'),
    path("id<int:user_id>/note/<int:note_id>/delete/", views.delete_user_note, name='delete_user_note'),
    path("id<int:user_id>/note/<int:note_id>/text/<int:text_id>/delete/", views.delete_text_from_note, name='delete_text_from_note'),

    path("id<int:user_id>/note/<int:note_id>/text/<int:text_id>/edit/", views.edit_text_from_note, name='edit_text_from_note'),
    path("id<int:user_id>/note/<int:note_id>/file/<int:file_id>/edit/", views.edit_file_from_note, name='edit_file_from_note'),

    #path("test/", views.test_, name="test"),
]
