from django.contrib import admin
from .models import MyUser
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
@admin.register(MyUser)
class UserAdmin(BaseUserAdmin):
    list_display = ('last_name', 'first_name','email', 'is_admin')
    list_filter = ('is_admin','first_name', 'last_name')
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('first_name','last_name', 'phone', 'country', 'city')}),
        ('Permissions', {'fields': ('is_admin',)}),
       
    )
    add_fieldsets = (
        (None, {
            'fields': ('email', 'password1', 'password2'),
        }),
    )
    search_fields = ('email','first_name', 'last_name')
    ordering = ('last_name', 'first_name')
    filter_horizontal = ()
