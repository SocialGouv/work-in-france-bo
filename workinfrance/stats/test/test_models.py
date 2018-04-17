import datetime

from django.test import TestCase

from workinfrance.stats.models import DossierAPT
from workinfrance.stats.test.raw_json_fixture import RAW_JSON_ANONYMIZED


class DossierAPTTest(TestCase):

    def test_attributes(self):
        """
        Test instance attributes.
        """
        dossier = DossierAPT.objects.create(
            ds_id=RAW_JSON_ANONYMIZED['dossier']['id'],
            status=RAW_JSON_ANONYMIZED['dossier']['state'],
            created_at=DossierAPT.json_datetime_to_python(RAW_JSON_ANONYMIZED['dossier']['created_at']),
            updated_at=DossierAPT.json_datetime_to_python(RAW_JSON_ANONYMIZED['dossier']['updated_at']),
            department='75 - Paris',
            raw_json=RAW_JSON_ANONYMIZED,
        )

        # Test "real" model fields.
        self.assertEqual(dossier.status, DossierAPT.STATUS_CLOSED)

        # Test attributes that are dynamically set to facilitate access to data stored in raw_json.
        self.assertEqual(dossier.email, 'john@doe.com')
        self.assertEqual(dossier.accompagnateurs, ['accompagnateur@direccte.gouv.fr'])
        # print(dossier.entreprise)
        # print(dossier.etablissement)
        # print(dossier.pieces_justificatives)
        self.assertEqual(dossier.date_de_debut_apt, datetime.date(2018, 3, 27))
        self.assertEqual(dossier.date_de_fin_apt, datetime.date(2018, 5, 10))
        self.assertEqual(dossier.cadre_reserve_a_ladministration, '')
        self.assertEqual(dossier.delivre_par, 'Préfecture de Paris')
        self.assertEqual(dossier.salaire_brut, '1485 euros/mois')
        self.assertEqual(dossier.nombre_dheures, '35 heures/semaine')
        self.assertEqual(dossier.date_de_fin, datetime.date(2018, 8, 28))
        self.assertEqual(dossier.date_de_debut, datetime.date(2018, 3, 28))
        self.assertEqual(dossier.type_de_contrat, 'contrat à durée déterminée (CDD)')
        self.assertEqual(dossier.adresse_ou_letudiant_va_travailler, "16 passage de l'Industrie\r\n75010 PARIS")
        self.assertEqual(dossier.emploi_occupe, 'Caissier')
        self.assertEqual(dossier.telephone_de_lemployeur, '0102030405')
        self.assertEqual(dossier.e_mail_de_lemployeur, 'employeur@doe.com')
        self.assertEqual(dossier.prenom_de_lemployeur, 'Bob')
        self.assertEqual(dossier.nom_de_lemployeur, 'Morane')
        self.assertEqual(dossier.departement_titre_de_sejour, '75 - Paris')
        self.assertEqual(dossier.numero, '123456789')
        self.assertEqual(dossier.reference_de_lancienne_autorisation_de_travail, '')
        self.assertEqual(dossier.demande, 'Première demande')
        self.assertEqual(dossier.telephone, '0601020304')
        self.assertEqual(dossier.e_mail, 'john@doe.com')
        self.assertEqual(dossier.lieu_de_naissance, 'Colmar')
        self.assertEqual(dossier.date_de_naissance, datetime.date(1978, 12, 20))
        self.assertEqual(dossier.nationalite, 'FRANCE')
        self.assertEqual(dossier.prenom, 'John')
        self.assertEqual(dossier.nom, 'Doe')
        self.assertEqual(dossier.civilite, 'M.')
        self.assertEqual(dossier.code_postal_de_residence_en_france, '75010')
        self.assertEqual(dossier.commune_de_residence_en_france, 'Paris')
        self.assertEqual(dossier.a_propos_de_lemployeur, None)
        self.assertEqual(dossier.informations_sur_le_contrat, None)
        self.assertEqual(dossier.employeur, None)
        self.assertEqual(dossier.date_dexpiration_titre_sejour, datetime.date(2018, 5, 10))
        self.assertEqual(dossier.salarie, None)
        self.assertEqual(dossier.document_autorisant_le_sejour_en_france, None)

    def test_json_date_to_python(self):
        d = DossierAPT.json_date_to_python('2018-03-27')
        self.assertEqual(d.year, 2018)
        self.assertEqual(d.month, 3)
        self.assertEqual(d.day, 27)

    def test_json_datetime_to_python(self):
        dt = DossierAPT.json_datetime_to_python('2018-03-27T08:49:51.491Z')
        self.assertEqual(dt.year, 2018)
        self.assertEqual(dt.month, 3)
        self.assertEqual(dt.day, 27)
        self.assertEqual(dt.hour, 8)
        self.assertEqual(dt.minute, 49)
        self.assertEqual(dt.second, 51)
        self.assertEqual(dt.microsecond, 491000)
        self.assertEqual(str(dt.tzinfo), 'UTC')
