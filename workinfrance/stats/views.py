import datetime

from django.db.models.expressions import RawSQL, OrderBy

from workinfrance.stats import utils
from workinfrance.stats.models import DossierAPT


def dossiers_to_watch_before_prefecture():
    """
    Return a list of 'Dossiers' to watch before a renew in 'préfecture'.
    Useful to verify whether a dossier was well inspected.
    """
    dossiers = (
        DossierAPT.objects
        .filter(champs_json__date_dexpiration_titre_sejour__gt=datetime.date.today().strftime("%Y-%m-%d"))
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
            'prenom': utils.obfuscate(dossier.prenom),
            'nom': utils.obfuscate(dossier.nom),
        }
        for dossier in closed_dossiers
    ]
