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

    # Below are some properties that act as shortcuts for quick access to some `raw_json` info.

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
    def champs(self):
        return [
            (item['type_de_champ']['libelle'], item['value'])
            for item in self.raw_json['dossier']['champs']
        ]

    @property
    def champs_private(self):
        """
        [('Date de début APT', '2018-03-29'), ('Date de fin APT', '2018-06-29'), ...]
        """
        return [
            (item['type_de_champ']['libelle'], item['value'])
            for item in self.raw_json['dossier']['champs_private']
        ]

    @property
    def apt_start_date(self):
        start_date = next(item[1] for item in self.champs_private if item[0] == "Date de début APT")
        if start_date:
            start_date = datetime.strptime(start_date, "%Y-%m-%d")
        return start_date

    @property
    def apt_end_date(self):
        end_date = next(item[1] for item in self.champs_private if item[0] == "Date de fin APT")
        if end_date:
            end_date = datetime.strptime(end_date, "%Y-%m-%d")
        return end_date


# pylint:enable=unsubscriptable-object
