from django.contrib import admin
from .models import Record
# Register your models here.

@admin.register(Record)
class UserModel(admin.ModelAdmin):
    list_display = ['first_name','last_name']

