from workinfrance.dossiers import utils
from workinfrance.dossiers.models import Dossier


def export_data_for_validity_check():
    """
    Return a list of closed Dossiers (i.e. accepted) to be used in the validity check UI.
    """
    closed_dossiers = Dossier.objects.filter(status=Dossier.STATUS_CLOSED)
    return [
        {
            'ds_id': dossier.ds_id,
            'siret': dossier.etablissement['siret'],
            'prenom': utils.obfuscate(dossier.prenom),
            'nom': utils.obfuscate(dossier.nom),
            'date_de_naissance': dossier.date_de_naissance,
            'has_expired': dossier.has_expired(),
            'date_de_debut_apt': dossier.date_de_debut_apt,
            'date_de_fin_apt': dossier.date_de_fin_apt,
        }
        for dossier in closed_dossiers
    ]
