from django.contrib import admin

from .models import User, UserProfile, AccountTier


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['email', 'first_name', 'last_name', 'is_active', 'account_tier']
    list_filter = ['first_name', 'last_name']
    search_fields = ['email']

    def account_tier(self, obj):
        return obj.userprofile.account_tier.name.upper()


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user_email', 'account_tier']
    list_filter = []
    search_fields = ['user__email']

    def account_tier(self, obj):
        return obj.account_tier.name.upper()

    def user_email(self, obj):
        return obj.user.email


@admin.register(AccountTier)
class AccountTierAdmin(admin.ModelAdmin):
    list_display = ['name', 'size', 'has_original', 'has_expiring_link']
    list_filter = ['size', 'has_original', 'has_expiring_link']
    list_editable = ['size', 'has_original', 'has_expiring_link']