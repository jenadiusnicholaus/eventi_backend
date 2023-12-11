from django.contrib import admin
from .models import User

class UserAdmin(admin.ModelAdmin):
    list_display = ['phone_number', 'email_id']
    search_fields = ['username']

admin.site.register(User, UserAdmin)
