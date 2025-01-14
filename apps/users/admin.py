from .models import User
from django.contrib import admin
from django.utils.translation import gettext_lazy as _

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'first_name', 'phone', 'is_active', 'code')
    search_fields = ('phone', 'first_name')
    exclude = ('password',)
    list_display_links = 'id', 'first_name', 'phone'

    def code(self, obj):
        return obj.verify_code.code

    def is_active_(self, obj):
        return obj.auth_status == 'code_verified'

    code.short_description = _("Code")
    is_active_.short_description = _("Is Active")

    def get_queryset(self, request):
        return super().get_queryset(request).prefetch_related('verify_code')

