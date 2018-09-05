import datetime

from django.contrib.postgres.fields import JSONField
from django.db import models
from django.utils.translation import ugettext_lazy as _

from workinfrance.dossiers import models_managers
from workinfrance.dossiers import models_queries
from workinfrance.dossiers import utils


# JSONField is subscriptable.
# pylint:disable=unsubscriptable-object


class Dossier(models.Model):
    """
    Store "dossiers" fetched from demarches-simplifiees.fr.

    Look at `raw_dossier_fixture` to see the structure of the data stored in the `raw_json` field.
    Look at `test_reformat_json_champs` to see the structure of the data stored in the `champs_json` field.
    """

    # TPS status names are different between the model and the API.
    # https://github.com/betagouv/tps/blob/58ce66/app/models/dossier.rb#L2-L9
    # https://github.com/betagouv/tps/blob/58ce66/app/serializers/dossier_serializer.rb#L38-L53
    STATUS_DRAFT = 'draft'
    STATUS_INITIATED = 'initiated'  # en_construction
    STATUS_RECEIVED = 'received'  # en_instruction
    STATUS_CLOSED = 'closed'  # accepte
    STATUS_REFUSED = 'refused'  # refuse
    STATUS_WITHOUT_CONTINUATION = 'without_continuation'  # sans_suite

    STATUS_CHOICES = (
        (STATUS_DRAFT, _('Brouillon')),
        (STATUS_INITIATED, _('En construction')),
        (STATUS_RECEIVED, _('En instruction')),
        (STATUS_CLOSED, _('Accepté')),
        (STATUS_REFUSED, _('Refusé')),
        (STATUS_WITHOUT_CONTINUATION, _('Sans suite')),
    )

    # https://github.com/betagouv/tps/blob/c7f5ca/app/models/dossier.rb#L12
    STATUSES_COMPLETED = [STATUS_CLOSED, STATUS_REFUSED, STATUS_WITHOUT_CONTINUATION]

    RAW_JSON_CHAMPS_MAPPING = {
        # Items in champs_private
        'date_de_debut_apt': 'Date de début APT',
        'date_de_fin_apt': 'Date de fin APT',
        'cadre_reserve_a_ladministration': "Cadre réservé à l'administration",
        # Items in champs
        'delivre_par': 'Délivré par',
        'salaire_brut': 'Salaire brut',
        'nombre_dheures': "Nombre d'heures",
        'date_de_fin': 'Date de fin',
        'date_de_debut': 'Date de début',
        'type_de_contrat': 'Type de contrat',
        'adresse_ou_letudiant_va_travailler': "Adresse ou l'étudiant va travailler",
        'emploi_occupe': 'Emploi occupé',
        'telephone_de_lemployeur': "Téléphone de l'employeur",
        'e_mail_de_lemployeur': "E-mail de l'employeur",
        'prenom_de_lemployeur': "Prénom de l'employeur",
        'nom_de_lemployeur': "Nom de l'employeur",
        'departement_titre_de_sejour': 'Département qui figure sur le titre de séjour',
        'numero': 'Numéro',
        'reference_de_lancienne_autorisation_de_travail': 'Référence de l’ancienne autorisation de travail',
        'demande': 'Demande',
        'telephone': 'Téléphone',
        'e_mail': 'E-mail',
        'lieu_de_naissance': 'Lieu de naissance',
        'date_de_naissance': 'Date de naissance',
        'nationalite': 'Nationalité',
        'prenom': 'Prénom',
        'nom': 'Nom',
        'civilite': 'Civilité',
        'code_postal_de_residence_en_france': 'Code postal de résidence en France',
        'commune_de_residence_en_france': 'Commune de résidence en France',
        'a_propos_de_lemployeur': "À propos de l'employeur",
        'informations_sur_le_contrat': 'Informations sur le contrat',
        'employeur': 'Employeur',
        'date_dexpiration_titre_sejour': 'Date d’expiration',
        'salarie': 'Salarié',
        'document_autorisant_le_sejour_en_france': 'Document autorisant le séjour en France',
    }

    ds_id = models.IntegerField(_("ID DS"), unique=True, db_index=True,
        help_text=_("ID sur demarches-simplifiees.fr"))
    status = models.CharField(_("Statut"), max_length=50, choices=STATUS_CHOICES, db_index=True)
    created_at = models.DateTimeField(_("Date de création"), db_index=True)
    updated_at = models.DateTimeField(_("Date de modification"), blank=True, null=True)
    department = models.CharField(_("Département titre de séjour"), max_length=255, db_index=True,
        help_text=_("Département qui figure sur le titre de séjour"))
    raw_json = JSONField(_("Résultat JSON brut"))
    # The raw_json field structure make it difficult to query the values of its `champs`
    # and `champs_private` subfields. The following field is used to facilitate queries.
    champs_json = JSONField(_("Champs et champs privés"),
        help_text=_("Champs et champs privés extraits de raw_json et reformatés"))

    objects = models.Manager()
    completed_objects = models_managers.CompletedManager()
    stats_objects = models_queries.StatsQueries.as_manager()
    prefecture_objects = models_queries.PrefectureQueries.as_manager()

    def __init__(self, *args, **kwargs):
        """
        Make some JSONField subfields of raw_json accessible as direct attributes of the instance, e.g.:
            self.email
            self.accompagnateurs
            self.date_de_debut_apt
            self.date_de_fin_apt
            etc.
        """
        super().__init__(*args, **kwargs)

        RAW_JSON_MAPPING = [
            'email',  # Email of the applicant.
            'accompagnateurs',  # Array of all "accompagnateurs".
            'entreprise',
            'etablissement',
            'pieces_justificatives'
        ]
        for property_name in RAW_JSON_MAPPING:
            if property_name in self.raw_json['dossier']:
              setattr(self, property_name, self.raw_json['dossier'][property_name])

        # No pk means that the object is being created: champs_json has not been populated
        # because save() has not yet been called.
        if not self.pk:
            self.champs_json = self.reformat_json_champs(self.raw_json)

        for key in self.RAW_JSON_CHAMPS_MAPPING:
            try:
                # Try to convert JSON dates to Python dates.
                # This is useful e.g. when the attribute is used in Django admin.
                value = utils.json_date_to_python(self.champs_json[key])
            except (TypeError, ValueError):
                value = self.champs_json[key]
            setattr(self, key, value)

    def __str__(self):
        return str(self.ds_id)

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        self.champs_json = self.reformat_json_champs(self.raw_json)
        super().save(force_insert=force_insert, force_update=force_update, using=using, update_fields=update_fields)

    @staticmethod
    def reformat_json_champs(raw_json):
        """
        Extract `champs` and `champs_private` from the given `raw_json` and create
        a new dict where values are easily identified by a slugified key.
        It's used to populate `self.champs_json`.
        """
        all_champs = {
            item['type_de_champ']['libelle']: item
            for item in raw_json['dossier']['champs'] + raw_json['dossier']['champs_private']
        }
        return {
            property_name: all_champs[champ_name]['value']
            for property_name, champ_name in Dossier.RAW_JSON_CHAMPS_MAPPING.items()
        }

    def has_expired(self):
        """Return True if an 'autorisation' has expired, False otherwise."""
        return self.date_de_fin_apt and self.date_de_fin_apt < datetime.date.today()


class DossierPrefecture(Dossier):
    """
    Use a proxy model to customize the Django admin.
    https://lincolnloop.com/blog/using-proxy-models-customize-django-admin/
    """

    class Meta:
        proxy = True
        verbose_name = _("Dossier (suivi Préfecture)")
        verbose_name_plural = _("Dossiers (suivi Préfecture)")


# pylint:enable=unsubscriptable-object
