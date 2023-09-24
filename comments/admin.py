from django.contrib import admin
from django.contrib.auth.models import User

from .models import Comment, HTMLTag

# Register your models here.
admin.site.register(Comment)
admin.site.register(HTMLTag)
admin.site.register(User)
