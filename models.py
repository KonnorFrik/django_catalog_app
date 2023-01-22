from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class UserNote(models.Model):
    note_title = models.CharField(max_length=100)
    note_description = models.CharField(max_length=300, blank=True, default="")
    #pub_date = models.DateTimeField("upload date", default=timezone.now)

    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.note_title


class AnyFile(models.Model):
    title = models.CharField(max_length=25)
    file = models.FileField(upload_to="catalog/any_files/")
    pub_date = models.DateTimeField("upload date", default=timezone.now)

    user_note = models.ForeignKey(UserNote, on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return self.title


class TextNote(models.Model):
    txt_title = models.CharField(max_length=25, default="", null=True)
    txt_text = models.CharField(max_length=250)
    pub_date = models.DateTimeField("upload date", default=timezone.now)

    user_note = models.ForeignKey(UserNote, on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return self.txt_title

