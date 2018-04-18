import datetime

from django.test import TestCase

from workinfrance.stats import utils
from workinfrance.stats.models import DossierAPT
from workinfrance.stats.test.raw_json_fixture import RAW_JSON_ANONYMIZED


class DossierAPTTest(TestCase):
    """
    Tests on DossierAPT that require data to exist in DB.
    """

    def setUp(self):
        super().setUp()
        self.dossier = DossierAPT.objects.create(
            ds_id=RAW_JSON_ANONYMIZED['dossier']['id'],
            status=RAW_JSON_ANONYMIZED['dossier']['state'],
            created_at=utils.json_datetime_to_python(RAW_JSON_ANONYMIZED['dossier']['created_at']),
            updated_at=utils.json_datetime_to_python(RAW_JSON_ANONYMIZED['dossier']['updated_at']),
            department='75 - Paris',
            raw_json=RAW_JSON_ANONYMIZED,
            champs_json=DossierAPT.reformat_json_champs(RAW_JSON_ANONYMIZED),
        )

    def test_attributes(self):
        """
        Test instance attributes.
        """
        # Test "real" model fields.
        self.assertEqual(self.dossier.status, DossierAPT.STATUS_CLOSED)

        # Test attributes that are dynamically set to facilitate access to data stored in raw_json.
        self.assertEqual(self.dossier.email, 'john@doe.com')
        self.assertEqual(self.dossier.accompagnateurs, ['accompagnateur@direccte.gouv.fr'])
        # print(self.dossier.entreprise)
        # print(self.dossier.etablissement)
        # print(self.dossier.pieces_justificatives)
        self.assertEqual(self.dossier.date_de_debut_apt, datetime.date(2018, 3, 27))
        self.assertEqual(self.dossier.date_de_fin_apt, datetime.date(2018, 5, 10))
        self.assertEqual(self.dossier.cadre_reserve_a_ladministration, '')
        self.assertEqual(self.dossier.delivre_par, 'Préfecture de Paris')
        self.assertEqual(self.dossier.salaire_brut, '1485 euros/mois')
        self.assertEqual(self.dossier.nombre_dheures, '35 heures/semaine')
        self.assertEqual(self.dossier.date_de_fin, datetime.date(2018, 8, 28))
        self.assertEqual(self.dossier.date_de_debut, datetime.date(2018, 3, 28))
        self.assertEqual(self.dossier.type_de_contrat, 'contrat à durée déterminée (CDD)')
        self.assertEqual(self.dossier.adresse_ou_letudiant_va_travailler, "16 passage de l'Industrie\r\n75010 PARIS")
        self.assertEqual(self.dossier.emploi_occupe, 'Caissier')
        self.assertEqual(self.dossier.telephone_de_lemployeur, '0102030405')
        self.assertEqual(self.dossier.e_mail_de_lemployeur, 'employeur@doe.com')
        self.assertEqual(self.dossier.prenom_de_lemployeur, 'Bob')
        self.assertEqual(self.dossier.nom_de_lemployeur, 'Morane')
        self.assertEqual(self.dossier.departement_titre_de_sejour, '75 - Paris')
        self.assertEqual(self.dossier.numero, '123456789')
        self.assertEqual(self.dossier.reference_de_lancienne_autorisation_de_travail, '')
        self.assertEqual(self.dossier.demande, 'Première demande')
        self.assertEqual(self.dossier.telephone, '0601020304')
        self.assertEqual(self.dossier.e_mail, 'john@doe.com')
        self.assertEqual(self.dossier.lieu_de_naissance, 'Colmar')
        self.assertEqual(self.dossier.date_de_naissance, datetime.date(1978, 12, 20))
        self.assertEqual(self.dossier.nationalite, 'FRANCE')
        self.assertEqual(self.dossier.prenom, 'John')
        self.assertEqual(self.dossier.nom, 'Doe')
        self.assertEqual(self.dossier.civilite, 'M.')
        self.assertEqual(self.dossier.code_postal_de_residence_en_france, '75010')
        self.assertEqual(self.dossier.commune_de_residence_en_france, 'Paris')
        self.assertEqual(self.dossier.a_propos_de_lemployeur, None)
        self.assertEqual(self.dossier.informations_sur_le_contrat, None)
        self.assertEqual(self.dossier.employeur, None)
        self.assertEqual(self.dossier.date_dexpiration_titre_sejour, datetime.date(2018, 5, 10))
        self.assertEqual(self.dossier.salarie, None)
        self.assertEqual(self.dossier.document_autorisant_le_sejour_en_france, None)


class DossierAPTStaticTest(TestCase):
    """
    Tests on DossierAPT that do not require data in DB.
    """

    def test_reformat_json_champs(self):
        reformated_json = DossierAPT.reformat_json_champs(RAW_JSON_ANONYMIZED)
        expected_result = {
            'date_de_debut_apt': '2018-03-27',
            'date_de_fin_apt': '2018-05-10',
            'cadre_reserve_a_ladministration': '',
            'delivre_par': 'Préfecture de Paris',
            'salaire_brut': '1485 euros/mois',
            'nombre_dheures': '35 heures/semaine',
            'date_de_fin': '2018-08-28',
            'date_de_debut': '2018-03-28',
            'type_de_contrat': 'contrat à durée déterminée (CDD)',
            'adresse_ou_letudiant_va_travailler': "16 passage de l'Industrie\r\n75010 PARIS",
            'emploi_occupe': 'Caissier',
            'telephone_de_lemployeur': '0102030405',
            'e_mail_de_lemployeur': 'employeur@doe.com',
            'prenom_de_lemployeur': 'Bob',
            'nom_de_lemployeur': 'Morane',
            'departement_titre_de_sejour': '75 - Paris',
            'numero': '123456789',
            'reference_de_lancienne_autorisation_de_travail': '',
            'demande': 'Première demande',
            'telephone': '0601020304',
            'e_mail': 'john@doe.com',
            'lieu_de_naissance': 'Colmar',
            'date_de_naissance': '1978-12-20',
            'nationalite': 'FRANCE',
            'prenom': 'John',
            'nom': 'Doe',
            'civilite': 'M.',
            'code_postal_de_residence_en_france': '75010',
            'commune_de_residence_en_france': 'Paris',
            'a_propos_de_lemployeur': None,
            'informations_sur_le_contrat': None,
            'employeur': None,
            'date_dexpiration_titre_sejour': '2018-05-10',
            'salarie': None,
            'document_autorisant_le_sejour_en_france': None
        }
        self.assertEqual(reformated_json, expected_result)
