from django.contrib import admin
from .models import Members
from django.contrib.sessions.models import Session

class SessionAdmin(admin.ModelAdmin):
    list_display = ['session_key', 'expire_date', 'get_decoded']

    def get_decoded(self, obj):
        return obj.get_decoded()
    get_decoded.short_description = 'Session Data'


class MembersAdmin(admin.ModelAdmin):
    list_display = ('email', 'firstname', 'lastname', 'auth_method', 'is_active', 'is_staff', 'is_verified')
    list_filter = ('is_active', 'is_staff', 'auth_method')
    search_fields = ('email', 'firstname', 'lastname')
    
admin.site.register(Members, MembersAdmin)
admin.site.register(Session, SessionAdmin)