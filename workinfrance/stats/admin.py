from django.contrib import admin
from django.contrib.postgres.fields import JSONField
from django.utils.translation import ugettext_lazy as _

from prettyjson import PrettyJSONWidget

from workinfrance.stats.models import DossierAPT


class DossierAPTAdmin(admin.ModelAdmin):

    list_display = (
        'id',
        'ds_id',
        'status',
        'created',
        'admin_departement_titre_de_sejour',
        'admin_date_de_debut_apt',
        'admin_date_de_fin_apt',
        'admin_accompagnateurs',
    )
    search_fields = ['ds_id']
    list_per_page = 100
    list_filter = ['status', 'department']
    ordering = ('-created_at',)
    list_display_links = ['id', 'ds_id']
    date_hierarchy = 'created_at'

    formfield_overrides = {
        JSONField: {'widget': PrettyJSONWidget}
    }

    def created(self, obj):
        return obj.created_at.strftime("%d/%m/%Y %H:%M")
    created.short_description = _("Créé le")

    def apt_start_date(self, obj):
        try:
            return obj.apt_start_date.strftime("%d/%m/%Y")
        except AttributeError:
            return obj.apt_start_date
    apt_start_date.short_description = _("Début APT")

    def apt_end_date(self, obj):
        try:
            return obj.apt_end_date.strftime("%d/%m/%Y")
        except AttributeError:
            return obj.apt_end_date
    apt_end_date.short_description = _("Fin APT")



admin.site.register(DossierAPT, DossierAPTAdmin)
