from django.contrib import admin
from django.contrib.postgres.fields import JSONField
from django.utils.translation import ugettext_lazy as _

from prettyjson import PrettyJSONWidget

from workinfrance.dossiers.models import Dossier


class DossierAdmin(admin.ModelAdmin):

    list_display = (
        'ds_id',
        'status',
        'created',
        'department',
        'date_de_debut_apt',
        'date_de_fin_apt',
        'accompagnateurs',
    )
    search_fields = ['ds_id']
    list_per_page = 100
    list_filter = ['status', 'department']
    ordering = ('-created_at',)
    list_display_links = ['ds_id']
    date_hierarchy = 'created_at'

    formfield_overrides = {
        JSONField: {'widget': PrettyJSONWidget}
    }

    def created(self, obj):
        return obj.created_at.strftime("%d/%m/%Y %H:%M")
    created.short_description = _("Créé le")

    def date_de_debut_apt(self, obj):
        if obj.date_de_debut_apt:
            return obj.date_de_debut_apt.strftime("%d/%m/%Y")
        return None
    date_de_debut_apt.short_description = _("Début APT")

    def date_de_fin_apt(self, obj):
        if obj.date_de_fin_apt:
            return obj.date_de_fin_apt.strftime("%d/%m/%Y")
        return None
    date_de_fin_apt.short_description = _("Fin APT")

    def accompagnateurs(self, obj):
        return obj.accompagnateurs
    accompagnateurs.short_description = _("Accompagnateurs")

admin.site.register(Dossier, DossierAdmin)
