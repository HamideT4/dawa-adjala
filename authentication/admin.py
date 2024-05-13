from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _
from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import User

class UserAdmin(BaseUserAdmin):
    ordering = ['email']
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = User
    list_display = ['email', 'first_name', 'last_name', 'address', 'gender', 'avatar', 'phone_number', 'is_staff', 'is_active']
    list_display_links = ["email"]
    list_filter = ["email", "is_staff", "is_active"]
    search_fields = ['first_name']
    fieldsets = (
        (
            _('Login Credentials'), 
            {
                'fields': ('email', 'password',)
            },
        ),
        (
            _('Personnal Information'),
            {
                'fields': ('first_name', 'last_name', 'address', 'gender', 'birth_date', 'phone_number', 'avatar',)
            },
        ),
        (
            _('Permissions and Groups'),
            {
                'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions',)
            },
        ),
        (
            _('Important Dates'),
            {
                'fields': ('last_login',)
            },
        ),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'first_name', 'last_name', 'address', 'birth_date', 'gender', 'avatar', 'phone_number', 'password1', 'password2', 'is_staff', 'is_active'),
        },),
    )
    

admin.site.register(User, UserAdmin)
