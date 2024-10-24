from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Account

class AccountAdmin(UserAdmin):
    list_display = ('email', 'first_name', 'last_name', 'username', 'last_login', 'date_joined', 'is_active')
    list_display_links = ('email', 'first_name', 'last_name')
    search_fields = ('email', 'username', 'first_name', 'last_name')
    readonly_fields = ('last_login', 'date_joined')
    ordering = ('-date_joined', )
    list_filter = ('is_active',)  # Removed 'is_superuser', 'groups'
    fieldsets = ()

    # Removed 'filter_horizontal' since 'groups' and 'user_permissions' are not part of Account
    filter_horizontal = ()  # Can be removed or left empty

admin.site.register(Account, AccountAdmin)
