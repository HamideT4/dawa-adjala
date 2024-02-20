from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _
from .forms import CustomUserCreationForm
from .models import Doctor, Patient, User, Consultation

class UserAdmin(BaseUserAdmin):
    ordering = ['first_name']
    add_form = CustomUserCreationForm
    model = User
    list_display = ['first_name', 'last_name', 'email', 'address', 'gender', 'avatar', 'phone_number', 'is_doctor', 'is_patient', 'is_staff', 'is_active']
    list_display_links = ['first_name', 'last_name']
    list_filter = ['first_name', 'is_active']
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
                'fields': ('first_name', 'last_name', 'address', 'gender', 'phone_number', 'avatar',)
            },
        ),
        (
            _('Permissions and Groups'),
            {
                'fields': ('is_doctor', 'is_patient', 'is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions',)
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
            'fields': ('first_name', 'last_name', 'address', 'gender', 'phone_number', 'password1', 'password2', 'is_staff', 'is_active'),
        },),
    )

admin.site.register(User, UserAdmin)
admin.site.register(Doctor)
admin.site.register(Patient)
admin.site.register(Consultation)