from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin
from django.utils.translation import ugettext_lazy as _
from . import forms


class EmailUserAdmin(DjangoUserAdmin):
    form = forms.EmailUserChangeForm
    add_form = forms.EmailUserCreationForm

    list_display = ('email', 'first_name', 'last_name', 'is_staff')
    fieldsets = (
        (None, {'fields': ('email', 'password',)}),
        (_('Personal info'), {'fields': ('first_name', 'last_name',)}),
        (_('Permissions'), {'fields': (
            'is_active', 'is_staff', 'is_superuser',
            'groups', 'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (
            None, {
                'classes': ('wide',),
                'fields': (
                    'email', 'first_name', 'last_name',
                    'password1', 'password2',
                )
            }
        ),
    )
    search_fields = ('email', 'first_name', 'last_name')

