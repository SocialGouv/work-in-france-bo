from datetime import datetime

from django.contrib.postgres.fields import JSONField
from django.db import models
from django.db.models.expressions import RawSQL, OrderBy
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _


# JSONField is subscriptable.
# pylint:disable=unsubscriptable-object


class CompletedDossierAPTManager(models.Manager):

    def get_queryset(self):
        return super().get_queryset().filter(status__in=self.model.STATUSES_COMPLETED)


class DossierAPT(models.Model):
    """
    Store "dossiers" from demarches-simplifiees.fr fetched via `django-admin sync_stats`.

    Look at `raw_json_fixture` to see the structure of the data stored in the `raw_json` field.
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

    ds_id = models.IntegerField(_("ID DS"), unique=True, db_index=True,
        help_text=_("ID sur demarches-simplifiees.fr"))
    status = models.CharField(_("Statut"), max_length=50, choices=STATUS_CHOICES, db_index=True)
    created_at = models.DateTimeField(_("Date de création"), db_index=True)
    updated_at = models.DateTimeField(_("Date de modification"), blank=True, null=True)
    department = models.CharField(_("Département"), max_length=255, db_index=True,
        help_text=_("Département qui figure sur le titre de séjour"))
    raw_json = JSONField(_("Résultat JSON brut"))
    # The raw_json field structure make it difficult to query the values of its `champs`
    # and `champs_private` subfields. The following field is used to facilitate queries.
    champs_json = JSONField(_("Champs et champs privés"),
        help_text=_("Champs et champs privés extraits de raw_json et reformatés"))

    objects = models.Manager()
    completed_objects = CompletedDossierAPTManager()

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
            setattr(self, property_name, self.raw_json['dossier'][property_name])

        for key in self.RAW_JSON_CHAMPS_MAPPING:
            try:
                # Try to convert JSON dates to Python dates.
                # This is useful e.g. when the attribute is used in Django admin.
                value = self.json_date_to_python(self.champs_json[key])
            except (TypeError, ValueError):
                value = self.champs_json[key]
            setattr(self, key, value)

    def __str__(self):
        return str(self.ds_id)

    @staticmethod
    def json_date_to_python(json_date):
        """Convert the given `json_date` to a date object."""
        return datetime.strptime(json_date, '%Y-%m-%d').date()

    @staticmethod
    def json_datetime_to_python(json_datetime):
        """Convert the given `json_datetime` to a datetime object."""
        dt = datetime.strptime(json_datetime, "%Y-%m-%dT%H:%M:%S.%fZ")
        return timezone.make_aware(dt, timezone.utc)

    @staticmethod
    def obfuscate(string):
        """Obfuscate a string by replacing all its characters except the second one."""
        obfuscation_char = '*'
        chars_to_ignore = [' ']
        return ''.join(
            char
            if i == 2 or char in chars_to_ignore else obfuscation_char
            for i, char in enumerate(string, start=1)
        )

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
            for property_name, champ_name in DossierAPT.RAW_JSON_CHAMPS_MAPPING.items()
        }

    # Explicit properties are required for values to be displayed in the Django admin.

    @property
    def admin_departement_titre_de_sejour(self):
        return self.departement_titre_de_sejour

    @property
    def admin_date_de_debut_apt(self):
        return self.date_de_debut_apt

    @property
    def admin_date_de_fin_apt(self):
        return self.date_de_fin_apt

    @property
    def admin_accompagnateurs(self):
        return self.accompagnateurs


# pylint:enable=unsubscriptable-object


def dossiers_to_watch_before_prefecture():
    """
    Return a list of 'Dossiers' to watch before a renew in 'préfecture'.
    Useful to verify whether a dossier was well inspected.
    """
    dossiers = (
        DossierAPT.objects
        .filter(champs_json__date_dexpiration_titre_sejour__gt=datetime.today().strftime("%Y-%m-%d"))
        .order_by(OrderBy(RawSQL("champs_json->>%s", ("date_dexpiration_titre_sejour",)), descending=True))
    )
    return [
        "{0} - {1} - {2} - {3} - {4} - {5}".format(
            dossier.date_dexpiration_titre_sejour.strftime("%d/%m/%Y"),
            dossier.ds_id,
            dossier.nationalite,
            dossier.prenom,
            dossier.nom,
            dossier.get_status_display(),
        ) for dossier in dossiers
    ]


def print_dossiers_to_watch_before_prefecture():
    for item in dossiers_to_watch_before_prefecture():
        print(item)


def export_data_for_validity_check():
    """
    Return a list of closed 'Dossiers' (i.e. accepted) to be used in the validity check UI.
    """
    closed_dossiers = DossierAPT.objects.filter(status=DossierAPT.STATUS_CLOSED)
    return [
        {
            'id': dossier.ds_id,
            'siret': dossier.etablissement['siret'],
            'prenom': DossierAPT.obfuscate(dossier.prenom),
            'nom': DossierAPT.obfuscate(dossier.nom),
        }
        for dossier in closed_dossiers
    ]
