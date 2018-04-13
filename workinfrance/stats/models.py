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

    def __str__(self):
        return str(self.ds_id)

    # Below are some methods and properties that act as shortcuts for quick access to some `raw_json` info.

    def get_champs(self):
        """
        Returns a dict of `champs` and `champs_private` from the `raw_json`, e.g.:
        {
            # ---------------------- Items in champs_private
            'Date de début APT': '2018-04-03',
            'Date de fin APT': '2018-05-20',
            "Cadre réservé à l'administration": '',
            # ---------------------- Items in champs
            'Délivré par': 'Préfecture de Paris',
            'Salaire brut': '28824 euros/an',
            "Nombre d'heures": '1607 heures/an',
            'Date de fin': '2018-08-03',
            'Date de début': '2018-05-07',
            'Type de contrat': 'contrat à durée déterminée (CDD)',
            "Adresse ou l'étudiant va travailler": '16 rue de John Doe 75002',
            'Emploi occupé': 'Compliance Officier',
            "Téléphone de l'employeur": '0101010101',
            "E-mail de l'employeur": 'john@doe.com',
            "Prénom de l'employeur": 'John',
            "Nom de l'employeur": 'Doe',
            'Département qui figure sur le titre de séjour': '75 - Paris',
            'Numéro': '1234567890',
            'Référence de l’ancienne autorisation de travail': '',
            'Demande': 'Première demande',
            'Téléphone': '0601010101',
            'E-mail': 'john@doe.com',
            'Lieu de naissance': 'Tizi-Ouzou',
            'Date de naissance': '1992-01-01',
            'Nationalité': 'ALGERIE',
            'Prénom': 'John',
            'Nom': 'Doe',
            'Civilité': 'M.',
            'Code postal de résidence en France': '75015',
            'Commune de résidence en France': 'Paris',
            "À propos de l'employeur": None,
            'Informations sur le contrat': None,
            'Employeur': None,
            'Date d’expiration': '2018-11-12',
            'Salarié': None,
            'Document autorisant le séjour en France': None,
        }
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
        Returns the value for the given TPS's 'libelle'.
        Warning: sometimes typographic apostrophe can be used in a TPS's 'libelle'.
        """
        return self.get_champs().get(champ_name)

    @property
    def email(self):
        """
        Return the email of the applicant.
        """
        return self.raw_json['dossier']['email']

    @property
    def accompagnateurs(self):
        """
        Return an array of all "accompagnateurs".
        """
        return self.raw_json['dossier']['accompagnateurs']

    @property
    def entreprise(self):
        return self.raw_json['dossier']['entreprise']

    @property
    def etablissement(self):
        return self.raw_json['dossier']['etablissement']

    @property
    def pieces_justificatives(self):
        return self.raw_json['dossier']['pieces_justificatives']

    @property
    def apt_start_date(self):
        start_date = self.get_value_of_champ("Date de début APT")
        if start_date:
            start_date = datetime.strptime(start_date, '%Y-%m-%d')
        return start_date

    @property
    def apt_end_date(self):
        end_date = self.get_value_of_champ("Date de fin APT")
        if end_date:
            end_date = datetime.strptime(end_date, '%Y-%m-%d')
        return end_date

    @property
    def expiration_titre_sejour_date(self):
        expiration_date = self.get_value_of_champ("Date d’expiration")
        if expiration_date:
            expiration_date = datetime.strptime(expiration_date, '%Y-%m-%d')
        return expiration_date


# pylint:enable=unsubscriptable-object


def dossiers_to_watch_before_prefecture():
    """
    Print a list of 'Dossiers' to watch before a renew in 'préfecture'.
    Useful to verify whether a dossier was well inspected.
    """
    dossiers = DossierAPT.objects.all()

    dossiers_to_check = {}
    for d in dossiers:

        if not d.expiration_titre_sejour_date or (d.expiration_titre_sejour_date < datetime.now()):
            continue

        dossiers_to_check[d.expiration_titre_sejour_date] = {
            'expiration_titre_sejour_date': d.expiration_titre_sejour_date,
            'ds_id': d.ds_id,
            'nationality': d.get_value_of_champ('Nationalité'),
            'first_name': d.get_value_of_champ('Prénom'),
            'last_name': d.get_value_of_champ('Nom'),
            'status': d.get_status_display(),
        }

    # Sort dict by the expiration_titre_sejour_date key.
    dossiers_to_check = sorted(dossiers_to_check.items(), key=lambda x: x[0])

    for _, item in dossiers_to_check:
        print(
            item['expiration_titre_sejour_date'].strftime("%d/%m/%Y"),
            item['ds_id'],
            item['nationality'],
            item['first_name'],
            item['last_name'],
            item['status'],
        )
