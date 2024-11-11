from django.contrib import admin
from django.contrib.auth.models import Permission
from django.core.exceptions import PermissionDenied

from .models import CustomUser, Categories, Application

admin.site.register(CustomUser)
admin.site.register(Categories)
@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = ('title', 'status', 'user', 'start_date', 'end_date')
    ordering = ('-start_date',)

    def get_queryset(self, request):
        qs=super(ApplicationAdmin, self).get_queryset(request)
        return qs

    def save_model(self, request, obj, form, change):
        if not request.user.is_staff:
            raise PermissionDenied('У вас нет прав для этого')
        super(ApplicationAdmin, self).save_model(request, obj, form, change)
# Register your models here.
