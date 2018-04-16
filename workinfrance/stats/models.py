from datetime import datetime

from django.contrib.postgres.fields import JSONField
from django.db import models
from django.utils.translation import ugettext_lazy as _


# JSONField is subscriptable.
# pylint:disable=unsubscriptable-object


class CompletedDossierAPTManager(models.Manager):

    def get_queryset(self):
        return super().get_queryset().filter(status__in=self.model.STATUSES_COMPLETED)


class DossierAPT(models.Model):

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

    objects = models.Manager()
    completed_objects = CompletedDossierAPTManager()

    def __init__(self, *args, **kwargs):
        """
        Set some attributes that act as shortcuts for quick access to `raw_json` subfields.
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
        for property_name, champ_name in RAW_JSON_CHAMPS_MAPPING.items():
            setattr(self, property_name, self.get_value_of_champ(champ_name))

    def __str__(self):
        return str(self.ds_id)

    def get_champs(self):
        """
        Returns a dict of `champs` and `champs_private` from the `raw_json`.
        """
        champs = {
            item['type_de_champ']['libelle']: item['value']
            for item in self.raw_json['dossier']['champs']
        }
        champs_private = {
            item['type_de_champ']['libelle']: item['value']
            for item in self.raw_json['dossier']['champs_private']
        }
        champs.update(champs_private)
        return champs

    def get_value_of_champ(self, champ_name):
        """
        Returns the value for the given TPS's `champ_name` ('libelle').
        Warning: sometimes typographic apostrophe can be used in a TPS's 'libelle'.
        """
        value = self.get_champs().get(champ_name)
        try:
            # Convert the value to a date object.
            value = datetime.strptime(value, '%Y-%m-%d').date()
        except (TypeError, ValueError):
            pass
        return value

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
    Print a list of 'Dossiers' to watch before a renew in 'préfecture'.
    Useful to verify whether a dossier was well inspected.
    """
    dossiers = DossierAPT.objects.all()

    dossiers_to_check = {}
    for d in dossiers:

        if not d.date_dexpiration_titre_sejour or (d.date_dexpiration_titre_sejour < datetime.now().date()):
            continue

        dossiers_to_check[d.date_dexpiration_titre_sejour] = {
            'date_dexpiration_titre_sejour': d.date_dexpiration_titre_sejour,
            'ds_id': d.ds_id,
            'nationality': d.nationalite,
            'first_name': d.prenom,
            'last_name': d.nom,
            'status': d.get_status_display(),
        }

    # Sort dict by the date_dexpiration_titre_sejour key.
    dossiers_to_check = sorted(dossiers_to_check.items(), key=lambda x: x[0])

    for _, item in dossiers_to_check:
        print(
            item['date_dexpiration_titre_sejour'].strftime("%d/%m/%Y"),
            item['ds_id'],
            item['nationality'],
            item['first_name'],
            item['last_name'],
            item['status'],
        )
