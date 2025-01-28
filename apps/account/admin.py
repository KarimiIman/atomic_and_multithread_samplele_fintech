from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from apps.account.models import UserProfile,Wallet
from django.contrib.auth import get_user_model
User = get_user_model()

class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = 'Profile'
    fk_name = 'user'


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'is_active', 'groups')


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = User
        fields = (
        'username', 'email', 'first_name', 'last_name', 'is_staff', 'is_active', 'is_superuser', 'groups', 'last_login')


class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    inlines = [UserProfileInline]
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'is_active', 'is_superuser')
    search_fields = ('username', 'email', 'first_name', 'last_name')
    ordering = ('username',)
    list_filter = ('is_staff', 'is_active', 'is_superuser')

    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'email')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login',)}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
            'username', 'email', 'password1', 'password2', 'first_name', 'last_name', 'is_staff', 'is_active',
            'groups'),
        }),
    )

    def get_inline_instances(self, request, obj=None):
        if not obj:
            return []
        return super(CustomUserAdmin, self).get_inline_instances(request, obj)


# admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)


class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('fullname', 'phone_number', 'is_email_verified', 'is_phone_number_verified', 'create_time')
    search_fields = ('user__username', 'phone_number', 'user__email')
    list_filter = ('is_email_verified', 'is_phone_number_verified')
    ordering = ('create_time',)


admin.site.register(UserProfile, UserProfileAdmin)


class WalletAdmin(admin.ModelAdmin):
    list_display = ('user__username', 'rial_balance', 'gold_balance')
    search_fields = ('user__username','rial_balance', 'gold_balance', 'user__email')
    ordering = ('create_time',)


admin.site.register(Wallet, WalletAdmin)