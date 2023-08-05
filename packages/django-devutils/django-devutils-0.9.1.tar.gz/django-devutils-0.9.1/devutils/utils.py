from django.utils.translation import ugettext_lazy as _


class VerificationAction:
    def mark_unverified(modeladmin, request, queryset):
        queryset.update(verified=False)
    mark_unverified.short_description = _('Mark as not verified')

    def mark_verified(modeladmin, request, queryset):
        queryset.update(verified=True)
    mark_verified.short_description = _('Mark as verified')


def upload_path(instance, filename):
    extension = filename.split('.')[-1]
    return f'products/{instance.category}/{instance.slug}.{extension}'
