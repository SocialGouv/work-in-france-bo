import datetime

from django.db.models.expressions import RawSQL, OrderBy

from workinfrance.dossiers import utils
from workinfrance.dossiers.models import Dossier


def dossiers_to_watch_before_prefecture():
    '''
    Return a list of 'Dossiers' to watch before a renew in 'préfecture'.
    Useful to verify whether a dossier was well inspected.
    '''
    dossiers = (
        Dossier.objects
        .filter(champs_json__date_dexpiration_titre_sejour__gt=datetime.date.today().strftime('%Y-%m-%d'))
        .order_by(OrderBy(RawSQL('champs_json->>%s', ('date_dexpiration_titre_sejour',)), descending=True))
    )
    return [
        '{0} - {1} - {2} - {3} - {4} - {5}'.format(
            dossier.date_dexpiration_titre_sejour.strftime('%d/%m/%Y'),
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
    '''
    Return a list of closed 'Dossiers' (i.e. accepted) to be used in the validity check UI.
    '''
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


def stats():

    from django.contrib.postgres.fields.jsonb import KeyTextTransform
    from django.db.models import Count, Case, When, Sum
    from django.db.models.functions import Coalesce
    from django.db.models.functions import TruncDate
    from django.utils import timezone

    # Number of dossiers by country.
    Dossier.objects
        .annotate(nationalite=KeyTextTransform('nationalite', 'champs_json'))
        .values('nationalite')
        .annotate(total=Count('nationalite'))
        .order_by('-total')

    # Number of dossiers by day.
    Dossier.objects
        .annotate(date=TruncDate('created_at'))
        .values('date')
        .annotate(total=Count('date'))
        .order_by('date')

    # Filter dossiers by date range.
    now = timezone.now()
    start_date = now - datetime.timedelta(days=2)
    end_date = now
    Dossier.objects.filter(created_at__range=(start_date, end_date))

    # Number in each status.
    # TODO: 0 values are not included.
    # Build a custom objects
    Dossier.objects.values('status').annotate(total=Count('status'))

    # Dossier.objects.all().count()
    # # En construction.
    # Dossier.objects.filter(status=Dossier.STATUS_INITIATED).count()
    # # En instruction.
    # Dossier.objects.filter(status=Dossier.STATUS_RECEIVED).count()
    # # Accepté.
    # Dossier.objects.filter(status=Dossier.STATUS_CLOSED).count()
    # # Refusé.
    # Dossier.objects.filter(status=Dossier.STATUS_REFUSED).count()
    # # Sans suite.
    # Dossier.objects.filter(status=Dossier.STATUS_WITHOUT_CONTINUATION).count()
