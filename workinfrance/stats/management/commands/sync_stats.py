from datetime import datetime
import json

from django.conf import settings
from django.core.management.base import BaseCommand
from django.utils import timezone

import requests

from workinfrance.stats.models import DossierAPT


class Command(BaseCommand):

    help = 'Fetch dossiers from the demarches-simplifiees.fr API and store them in our DB.'

    API_BASE_URL = f'{settings.DS_API_BASE_URL}/procedures/{settings.DS_PROCEDURE_ID_APT}'
    API_PAYLOAD = {'token': settings.DS_API_TOKEN}
    API_HEADERS = {'content-type': 'application/json'}

    STATS = {
        'count_dossiers': 0,
        'count_http_queries': 0,
        'count_update_or_create': 0,
    }

    def handle(self, *args, **options):

        dossiers_ids = self.fetch_dossiers_ids()
        self.fetch_and_store_dossiers(dossiers_ids)

        self.stdout.write(f"""--------------------------------------------------------------------------------
{self.STATS['count_dossiers']} - number of dossiers checked
{self.STATS['count_http_queries']} - number of HTTP queries performed
{self.STATS['count_update_or_create']} - number of dossiers processed
Done.""")

    def fetch_dossiers_ids(self):
        """
        Fetch all dossiers IDs.
        """
        ALL_DOSSIERS_URL = f'{self.API_BASE_URL}/dossiers'
        page_current = 1
        data = {
            'page': page_current,
            'resultats_par_page': 1000,
        }
        r = requests.get(ALL_DOSSIERS_URL, params=self.API_PAYLOAD, headers=self.API_HEADERS, data=json.dumps(data))
        resp = r.json()
        self.STATS['count_http_queries'] += 1

        dossiers_ids = [item['id'] for item in resp['dossiers']]
        self.STATS['count_dossiers'] = len(dossiers_ids)

        # The list of all dossiers may have multiple pages. In this case, iterate over other pages.
        while page_current < resp['pagination']['nombre_de_page']:
            page_current += 1
            data['page'] = page_current

            r = requests.get(ALL_DOSSIERS_URL, params=self.API_PAYLOAD, headers=self.API_HEADERS, data=json.dumps(data))
            resp_json = r.json()
            self.STATS['count_http_queries'] += 1

            dossiers_ids.extend([item['id'] for item in resp_json['dossiers']])
            self.STATS['count_dossiers'] = len(dossiers_ids)

        return dossiers_ids

    def fetch_and_store_dossiers(self, dossiers_ids):
        """
        Fetch and store dossiers details.
        """
        for dossier_id in dossiers_ids:

            self.stdout.write('-' * 80)

            if DossierAPT.completed_objects.filter(ds_id=dossier_id).exists():
                # Don't process a dossier that is already completed.
                self.stdout.write(f'Dossier {dossier_id} already in a completed state')
                continue

            self.stdout.write(f'Fetching dossier {dossier_id}')
            DOSSIER_URL = f'{self.API_BASE_URL}/dossiers/{dossier_id}'
            r = requests.get(DOSSIER_URL, params=self.API_PAYLOAD, headers=self.API_HEADERS)
            resp_json = r.json()
            self.STATS['count_http_queries'] += 1

            data = self.format_for_model(resp_json)
            dossier = DossierAPT.objects.filter(ds_id=data['ds_id']).first()

            if not dossier or data['updated_at'] > dossier.updated_at:
                self.stdout.write(f'Storing dossier {dossier_id}')
                DossierAPT.objects.update_or_create(
                    ds_id=data['ds_id'],
                    defaults={
                        'status': data['status'],
                        'created_at': data['created_at'],
                        'updated_at': data['updated_at'],
                        'department': data['department'],
                        'raw_json': data['raw_json'],
                    },
                )
                self.STATS['count_update_or_create'] += 1

    def format_for_model(self, resp_json):
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
