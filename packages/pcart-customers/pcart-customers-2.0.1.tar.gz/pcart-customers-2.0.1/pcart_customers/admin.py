from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import (
    User,
    Customer,
    PasswordResetLink,
)
from .forms import UserChangeForm, UserCreationForm


class UserAdmin(BaseUserAdmin):
    add_form_template = 'customers/admin/auth/user/add_form.html'
    fieldsets = (
        (None, {
            'fields': (
                'email', 'phone', 'data',
                'password',
            )}),
        (_('Permissions'), {
            'fields': (
                'is_active', 'is_staff',
                'is_superuser',
                'groups',
                'user_permissions',
            )}),
        (_('Important dates'), {
            'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'phone', 'password1', 'password2')
        }),
    )

    list_display = (
        'email', 'phone', 'is_staff', 'is_superuser', 'is_active',
        'date_joined', 'last_login', 'has_usable_password',
    )
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'groups')
    search_fields = ('email', 'phone')
    ordering = ('email',)
    date_hierarchy = 'date_joined'
    filter_horizontal = ('groups', 'user_permissions',)

    form = UserChangeForm
    add_form = UserCreationForm
    actions = [
        'activate',
        'deactivate',
        'set_unusable_password',
    ]

    def get_urls(self):
        from django.conf.urls import url
        return [
            url(
                r'^(.+)/change/password/$',
                self.admin_site.admin_view(self.user_change_password),
                name='auth_user_password_change',
            ),
        ] + super().get_urls()

    def activate(self, request, queryset):
        queryset.update(is_active=True)
    activate.short_description = \
        _('Activate')

    def deactivate(self, request, queryset):
        queryset.update(is_active=False)
    deactivate.short_description = \
        _('Deactivate')

    def set_unusable_password(self, request, queryset):
        for q in queryset:
            q.set_unusable_password()
            q.save()
    set_unusable_password.short_description = \
        _('Set unusable password')


admin.site.register(User, UserAdmin)


class CustomerAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'session_id', 'name', 'added', 'changed')
    raw_id_fields = ('user',)
    search_fields = ['user', 'session_id', 'name']


admin.site.register(Customer, CustomerAdmin)


class PasswordResetLinkAdmin(admin.ModelAdmin):
    list_display = ('user', 'slug', 'active', 'added', 'expiration_date')
    raw_id_fields = ('user',)
    search_fields = ('user', 'slug')


admin.site.register(PasswordResetLink, PasswordResetLinkAdmin)
