import json
import os
import math

from django.conf import settings
from django.core.management.base import BaseCommand
from django.core.serializers.json import DjangoJSONEncoder
from django.utils import timezone

from workinfrance.dossiers.models import Dossier


class Command(BaseCommand):
    """
    Export a JSON file containing the stats data.

    The format is adapted to 'Frappe Charts':
    https://frappe.github.io/charts/
    """

    help = 'Export a JSON file containing the stats data.'

    def handle(self, *args, **options):

        num_dossiers_day = Dossier.stats_objects.get_num_by_day()
        data_num_dossiers_day = {
            'labels': [d.strftime("%d/%m/%y") for d in num_dossiers_day.keys()],
            'datasets': [
                {
                    'name': "Nombre de dossiers par jour",
                    'values': list(num_dossiers_day.values()),
                },
            ],
        }

        num_dossiers_month = Dossier.stats_objects.get_num_by_month()
        data_num_dossiers_month = {
            'labels': [d.strftime("%m/%y") for d in num_dossiers_month.keys()],
            'datasets': [
                {
                    'name': "Nombre de dossiers par mois",
                    'values': list(num_dossiers_month.values()),
                },
            ],
        }

        num_by_status = Dossier.stats_objects.get_num_by_status()
        data_num_by_status = {
            'labels': [dict(Dossier.STATUS_CHOICES)[item] for item in num_by_status.keys()],
            'datasets': [
                {
                    'name': "Nombre de dossiers par statut",
                    'values': list(num_by_status.values()),
                },
            ],
        }

        num_by_contry = Dossier.stats_objects.get_num_by_country()
        data_num_by_contry = {
            'labels': [country_name.title() for country_name in num_by_contry.keys()],
            'datasets': [
                {
                    'name': "Nombre de dossiers par pays",
                    'values': list(num_by_contry.values()),
                },
            ],
        }

        time_to_process_by_month = (
            Dossier.stats_objects.filter(status=Dossier.STATUS_CLOSED)
            .get_time_to_process_by_month()
        )
        data_time_to_process_by_month = {
            'labels': [
                f'{dt.strftime("%m/%Y")} - {delta.days} jour(s)'
                for dt, delta in time_to_process_by_month.items()
            ],
            'datasets': [
                {
                    'name': "Temps de traitement moyen par mois (en jours)",
                    'values': [delta.days for delta in time_to_process_by_month.values()],
                },
            ],
        }

        time_to_process = Dossier.stats_objects.filter(status=Dossier.STATUS_CLOSED).get_time_to_process()
        time_to_process = math.floor(time_to_process.total_seconds() / 60 / 60 / 24)

        data = {
            'data': {
                'last_update': timezone.now(),
                'time_to_process': time_to_process,
                'total_dossiers_closed': Dossier.objects.filter(status=Dossier.STATUS_CLOSED).count(),
                'total_dossiers': Dossier.objects.all().count(),
            },
            'data_num_dossiers_day': data_num_dossiers_day,
            'data_num_dossiers_month': data_num_dossiers_month,
            'data_num_by_status': data_num_by_status,
            'data_num_by_contry': data_num_by_contry,
            'data_time_to_process_by_month': data_time_to_process_by_month,
        }

        file_path = os.path.join(settings.MEDIA_ROOT, 'stats.json')
        with open(file_path, 'w') as outfile:
            json.dump(data, outfile, cls=DjangoJSONEncoder)

        self.stdout.write("Done.")
