from django.contrib import admin

from .models import Comment, HTMLTag

# Register your models here.
admin.site.register(Comment)
admin.site.register(HTMLTag)
