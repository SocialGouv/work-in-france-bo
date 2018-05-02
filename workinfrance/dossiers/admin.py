from django.contrib import admin
from django.contrib.postgres.fields import JSONField
from django.utils.translation import ugettext_lazy as _

from prettyjson import PrettyJSONWidget

from workinfrance.dossiers.models import Dossier, DossierPrefecture


@admin.register(Dossier)
class DossierAdmin(admin.ModelAdmin):

    list_display = (
        'ds_id',
        'status',
        'created',
        'department',
        'custom_date_de_debut_apt',
        'custom_date_de_fin_apt',
        'custom_accompagnateurs',
    )
    date_hierarchy = 'created_at'
    list_display_links = ['ds_id']
    list_filter = ['status', 'department']
    list_per_page = 100
    ordering = ('-created_at',)
    search_fields = ['ds_id']

    formfield_overrides = {
        JSONField: {'widget': PrettyJSONWidget}
    }

    def created(self, obj):
        return obj.created_at.strftime("%d/%m/%Y %H:%M")
    created.short_description = _("Créé le")

    # The following fields are custom list_display fields that have no DB field, they are not sortable etc.

    def custom_accompagnateurs(self, obj):
        return obj.accompagnateurs
    custom_accompagnateurs.short_description = _("Accompagnateurs")

    def custom_date_de_debut_apt(self, obj):
        if obj.date_de_debut_apt:
            return obj.date_de_debut_apt.strftime("%d/%m/%Y")
        return None
    custom_date_de_debut_apt.short_description = _("Début APT")

    def custom_date_de_fin_apt(self, obj):
        if obj.date_de_fin_apt:
            return obj.date_de_fin_apt.strftime("%d/%m/%Y")
        return None
    custom_date_de_fin_apt.short_description = _("Fin APT")


@admin.register(DossierPrefecture)
class DossierPrefectureAdmin(admin.ModelAdmin):
    """
    List of Dossiers to watch before a renewal in Prefecture.
    Useful to verify whether a dossier was well inspected.
    """

    list_display = (
        'custom_expiration_titre_sejour',
        'ds_id',
        'custom_nationalite',
        'custom_prenom',
        'custom_nom',
        'status',
    )
    actions = None
    list_display_links = ['ds_id']
    list_filter = ['status']
    list_per_page = 100

    formfield_overrides = {
        JSONField: {'widget': PrettyJSONWidget}
    }

    def get_queryset(self, request):
        return self.model.prefecture_objects.watch_before_renew()

    def has_add_permission(self, request):
        # Hide add buttons.
        return False

    def has_delete_permission(self, request, obj=None):
        # Hide delete buttons.
        return False

    def changelist_view(self, request, extra_context=None):
        return super().changelist_view(request, extra_context={
            'title': _("Suivi Préfecture : dossiers à surveiller pour cause de renouvellement proche en Préfecture"),
        })

    # The following fields are custom list_display fields that have no DB field, they are not sortable etc.

    def custom_expiration_titre_sejour(self, obj):
        return obj.date_dexpiration_titre_sejour.strftime("%d/%m/%Y")
    custom_expiration_titre_sejour.short_description = _("Date d'expiration du titre de sejour")
    # Allow to sort on custom list_display field.
    # https://stackoverflow.com/a/7448615
    custom_expiration_titre_sejour.admin_order_field = 'expiration_admin_order'

    def custom_nationalite(self, obj):
        return obj.nationalite.title()
    custom_nationalite.short_description = _("Nationalité")

    def custom_nom(self, obj):
        return obj.nom.title()
    custom_nom.short_description = _("Nom")

    def custom_prenom(self, obj):
        return obj.prenom.title()
    custom_prenom.short_description = _("Prénom")
