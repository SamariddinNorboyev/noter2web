from django.contrib import admin
from .models import List, Note
# Register your models here.
admin.site.register(List)
admin.site.register(Note)
# admin.site.register(Subnote)