from django.contrib import admin
from import_export.admin import ImportExportModelAdmin


class ReporterAdminMixin(admin.ModelAdmin):
    def get_queryset(self, request):
        queryset = super().get_queryset(request)

        if request.user.has_perm('reporting.delete_mood'):
            return queryset
        else:
            return queryset.filter(reporter=request.user)

    def save_model(self, request, obj, form, change):
        obj.reporter = request.user
        super().save_model(request, obj, form, change)


class BaseAdmin(ImportExportModelAdmin):
    change_list_template = 'admin/change_list_import_export.html'
    change_list_filter_template = 'admin/filter_listing.html'
    ordering = ['-modified']


class BaseTabularInline(admin.TabularInline):
    pass


class BaseStackedInline(admin.StackedInline):
    pass
