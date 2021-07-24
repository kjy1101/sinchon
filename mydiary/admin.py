from django.contrib import admin
from .models import Content, Comment, Tag

# Register your models here.

admin.site.register(Content)
admin.site.register(Comment)
admin.site.register(Tag)