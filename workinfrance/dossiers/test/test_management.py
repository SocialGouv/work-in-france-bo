import io

from unittest import mock

from django.core.management import call_command
from django.test import TestCase

from workinfrance.dossiers.models import Dossier
from workinfrance.dossiers.test.raw_dossiers_json_fixture import RAW_DOSSIERS_JSON
from workinfrance.dossiers.test.raw_json_fixture import RAW_JSON_ANONYMIZED


def mocked_requests_get(*args, **kwargs):
    """
    Simple method to mock Requests.get and the response.
    """

    class MockResponse:

        def __init__(self, json_data, status_code):
            self.json_data = json_data
            self.status_code = status_code

        def json(self):
            return self.json_data

    endpoint = args[0]

    if endpoint == 'https://www.demarches-simplifiees.fr/api/v1/procedures/3272/dossiers':
        return MockResponse(RAW_DOSSIERS_JSON, 200)

    if endpoint == 'https://www.demarches-simplifiees.fr/api/v1/procedures/3272/dossiers/44950':
        return MockResponse(RAW_JSON_ANONYMIZED, 200)

    return MockResponse(None, 404)


class ManagementCommandTest(TestCase):

    @mock.patch('requests.get', side_effect=mocked_requests_get)
    def testSyncDossiersCommand(self, mock_get):
        """
        Test the django-admin command `sync_dossiers`.
        """
        out = io.StringIO()
        err = io.StringIO()
        call_command('sync_dossiers', stdout=out, stderr=err)

        expected_result = """--------------------------------------------------------------------------------
Fetching dossier 44950
Storing dossier 44950
--------------------------------------------------------------------------------
1 - number of dossiers checked
2 - number of HTTP queries performed
1 - number of dossiers processed
Done."""

        self.assertEqual(out.getvalue().strip(), expected_result)

        dossier = Dossier.objects.get(ds_id='44950')
        self.assertEqual(dossier.status, Dossier.STATUS_CLOSED)
        self.assertEqual(dossier.nom_de_lemployeur, 'Morane')
