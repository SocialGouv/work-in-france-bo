from datetime import datetime
import json

from django.conf import settings
from django.core.management.base import BaseCommand
from django.utils import timezone

import requests

from workinfrance.stats.models import DossierAPT


class Command(BaseCommand):

    help = 'Fetch and store locally all dossiers available on demarches-simplifiees.fr'

    def handle(self, *args, **options):

        count_http_queries = 0
        count_update_or_create = 0

        API_BASE_URL = f'{settings.DS_API_BASE_URL}/procedures/{settings.DS_PROCEDURE_ID_APT}'
        API_PAYLOAD = {'token': settings.DS_API_TOKEN}
        API_HEADERS = {'content-type': 'application/json'}

        ALL_DOSSIERS_URL = f'{API_BASE_URL}/dossiers'
        page_current = 1
        data = {
            'page': page_current,
            'resultats_par_page': 1000,
        }

        # Get the list of all dossiers IDs of a procedure.
        r = requests.get(ALL_DOSSIERS_URL, params=API_PAYLOAD, headers=API_HEADERS, data=json.dumps(data))
        resp = r.json()
        count_http_queries += 1

        dossiers_ids = [item['id'] for item in resp['dossiers']]

        # The list of all dossiers may have multiple pages. In this case, iterate over other pages.
        while page_current < resp['pagination']['nombre_de_page']:

            page_current += 1

            data['page'] = page_current
            r = requests.get(ALL_DOSSIERS_URL, params=API_PAYLOAD, headers=API_HEADERS, data=json.dumps(data))
            resp_json = r.json()
            count_http_queries += 1

            dossiers_ids.extend([item['id'] for item in resp_json['dossiers']])

        # Get and store the details of each dossier.
        for dossier_id in dossiers_ids:

            self.stdout.write('-' * 80)
            self.stdout.write(f'Fetching dossier {dossier_id}')

            DOSSIER_URL = f'{API_BASE_URL}/dossiers/{dossier_id}'
            r = requests.get(DOSSIER_URL, params=API_PAYLOAD, headers=API_HEADERS)
            resp_json = r.json()
            count_http_queries += 1

            data = self.format_data_for_model(resp_json)
            dossier = DossierAPT.objects.filter(ds_id=data['ds_id']).first()

            if not dossier or data['updated_at'] > dossier.updated_at:
                self.stdout.write(f'Processing dossier {dossier_id}')
                _, _ = DossierAPT.objects.update_or_create(
                    ds_id=data['ds_id'],
                    defaults={
                        'status': data['status'],
                        'created_at': data['created_at'],
                        'updated_at': data['updated_at'],
                        'department': data['department'],
                        'raw_json': data['raw_json'],
                    },
                )
                count_update_or_create += 1

        self.stdout.write('-' * 80)
        self.stdout.write(f'{len(dossiers_ids)} dossiers were checked')
        if count_update_or_create:
            self.stdout.write(f'Successfully processed {count_update_or_create} dossier(s)')
        else:
            self.stdout.write(f'No dossier needed to be processed')
        self.stdout.write(f'{count_http_queries} HTTP queries were performed')
        self.stdout.write(f'Done.')

    def format_data_for_model(self, resp_json):
        """
        Convert the raw JSON response to a format that we can store in the DossierAPT model.
        """
        created_at = datetime.strptime(resp_json['dossier']['created_at'], "%Y-%m-%dT%H:%M:%S.%fZ")

        updated_at = None
        if resp_json['dossier']['updated_at']:
            updated_at = datetime.strptime(resp_json['dossier']['updated_at'], "%Y-%m-%dT%H:%M:%S.%fZ")

        department = next(
            item['value'] for item in resp_json['dossier']['champs']
            if item['type_de_champ']['libelle'] == "Département qui figure sur le titre de séjour"
        )

        return {
            'ds_id': resp_json['dossier']['id'],
            'status': resp_json['dossier']['state'],
            'created_at': timezone.make_aware(created_at, timezone.utc),
            'updated_at': timezone.make_aware(updated_at, timezone.utc) if updated_at else None,
            'department': department,
            'raw_json': resp_json,
        }
