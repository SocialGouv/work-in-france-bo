import datetime

from django.test import TestCase

from workinfrance.dossiers import utils
from workinfrance.dossiers.models import Dossier
from workinfrance.dossiers import views
from workinfrance.dossiers.test.raw_dossier_fixture import RAW_DOSSIER


class ViewsTest(TestCase):

    def setUp(self):
        super().setUp()
        self.dossier = Dossier.objects.create(
            ds_id=RAW_DOSSIER['dossier']['id'],
            status=RAW_DOSSIER['dossier']['state'],
            created_at=utils.json_datetime_to_python(RAW_DOSSIER['dossier']['created_at']),
            updated_at=utils.json_datetime_to_python(RAW_DOSSIER['dossier']['updated_at']),
            department='75 - Paris',
            raw_json=RAW_DOSSIER,
        )

    def test_export_data_for_validity_check(self):
        export_data = views.export_data_for_validity_check()
        expected_result = [
            {
                'ds_id': 44950,
                'siret': '52222222222222',
                'prenom': '*o**',
                'nom': '*o*',
                'date_de_naissance': datetime.date(1978, 12, 20),
                'date_de_debut_apt': datetime.date(2018, 3, 27),
                'date_de_fin_apt': datetime.date(2018, 5, 10),
                'has_expired': self.dossier.has_expired(),
            },
        ]
        self.assertEqual(export_data, expected_result)
