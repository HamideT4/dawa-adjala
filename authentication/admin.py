from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _
from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import User, Coupon, Payment, Recharge, Rechargebook, Notification, Account
from django.urls import path, reverse
from django.shortcuts import redirect
from django.utils.html import format_html


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
@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    list_display = ('account_unique_identifier', 'owner', 'balance',)
    ordering = ('account_unique_identifier',)
    search_fields = ('owner',)
#admin.site.register(Account)
admin.site.register(Recharge)
admin.site.register(Notification)
#admin.site.register(Rechargebook)
admin.site.register(Coupon)
admin.site.register(Payment)

class RechargebookAdmin(admin.ModelAdmin):
    list_display = ('owner', 'date', 'view_on_site_link')

    def view_on_site_link(self, obj):
        return format_html('<a href="{}" target="_blank">Voir le livret</a>', reverse('authentication:print_rechargebook', args=[obj.pk]))
    view_on_site_link.short_description = 'Lien pour imprimer'

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('<int:pk>/print/', self.admin_site.admin_view(self.print_rechargebook), name='print_rechargebook'),
        ]
        return custom_urls + urls

    def print_rechargebook(self, request, pk):
        return redirect('authentication:print_rechargebook', pk=pk)
    
admin.site.register(Rechargebook, RechargebookAdmin)
