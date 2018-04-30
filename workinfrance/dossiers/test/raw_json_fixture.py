"""
The data structure returned by the demarches-simplifiees.fr API endpoint:
https://www.demarches-simplifiees.fr/api/v1/procedures/3272/dossiers/44950
"""

# Yes, lines are long.
# pylint:disable=line-too-long

RAW_JSON_ANONYMIZED = {
    'dossier': {
        'id': 44950,
        'cerfa': [],
        'email': 'john@doe.com',
        'state': 'closed',
        'champs': [{
            'value': '0102030405',
            'type_de_champ': {
                'id': 98307,
                'libelle': "Téléphone de l'employeur",
                'type_champ': 'phone',
                'description': '',
                'order_place': 23
            }
        }, {
            'value': 'employeur@doe.com',
            'type_de_champ': {
                'id': 98308,
                'libelle': "E-mail de l'employeur",
                'type_champ': 'email',
                'description': '',
                'order_place': 22
            }
        }, {
            'value': None,
            'type_de_champ': {
                'id': 98311,
                'libelle': "À propos de l'employeur",
                'type_champ': 'explication',
                'description': "L'employeur doit être un représentant légal de la société : il doit pouvoir agir au nom et pour le compte de la société.",
                'order_place': 19
            }
        }, {
            'value': 'john@doe.com',
            'type_de_champ': {
                'id': 98289,
                'libelle': 'E-mail',
                'type_champ': 'email',
                'description': '',
                'order_place': 9
            }
        }, {
            'value': 'M.',
            'type_de_champ': {
                'id': 98282,
                'libelle': 'Civilité',
                'type_champ': 'civilite',
                'description': '',
                'order_place': 3
            }
        }, {
            'value': 'Doe',
            'type_de_champ': {
                'id': 98283,
                'libelle': 'Nom',
                'type_champ': 'text',
                'description': '',
                'order_place': 4
            }
        }, {
            'value': 'John',
            'type_de_champ': {
                'id': 98284,
                'libelle': 'Prénom',
                'type_champ': 'text',
                'description': '',
                'order_place': 5
            }
        }, {
            'value': 'FRANCE',
            'type_de_champ': {
                'id': 98285,
                'libelle': 'Nationalité',
                'type_champ': 'pays',
                'description': '',
                'order_place': 6
            }
        }, {
            'value': '75010',
            'type_de_champ': {
                'id': 98286,
                'libelle': 'Code postal de résidence en France',
                'type_champ': 'text',
                'description': 'Par exemple : 75010',
                'order_place': 2
            }
        }, {
            'value': '1978-12-20',
            'type_de_champ': {
                'id': 98287,
                'libelle': 'Date de naissance',
                'type_champ': 'date',
                'description': '',
                'order_place': 7
            }
        }, {
            'value': 'Colmar',
            'type_de_champ': {
                'id': 98288,
                'libelle': 'Lieu de naissance',
                'type_champ': 'text',
                'description': '',
                'order_place': 8
            }
        }, {
            'value': '0601020304',
            'type_de_champ': {
                'id': 98290,
                'libelle': 'Téléphone',
                'type_champ': 'phone',
                'description': '',
                'order_place': 10
            }
        }, {
            'value': 'Première demande',
            'type_de_champ': {
                'id': 98291,
                'libelle': 'Demande',
                'type_champ': 'drop_down_list',
                'description': '',
                'order_place': 11
            }
        }, {
            'value': '',
            'type_de_champ': {
                'id': 98292,
                'libelle': 'Référence de l’ancienne autorisation de travail',
                'type_champ': 'text',
                'description': 'En cas de renouvellement, précisez le "N° de Dossier" de votre ancienne autorisation de travail au format papier ou numérique',
                'order_place': 12
            }
        }, {
            'value': None,
            'type_de_champ': {
                'id': 98293,
                'libelle': 'Document autorisant le séjour en France',
                'type_champ': 'header_section',
                'description': '',
                'order_place': 13
            }
        }, {
            'value': None,
            'type_de_champ': {
                'id': 98294,
                'libelle': 'Salarié',
                'type_champ': 'header_section',
                'description': '',
                'order_place': 0
            }
        }, {
            'value': 'Paris',
            'type_de_champ': {
                'id': 98295,
                'libelle': 'Commune de résidence en France',
                'type_champ': 'text',
                'description': 'Par exemple : Paris',
                'order_place': 1
            }
        }, {
            'value': '123456789',
            'type_de_champ': {
                'id': 98296,
                'libelle': 'Numéro',
                'type_champ': 'text',
                'description': "Il s'agit du numéro inscrit sur :\r\n- carte de séjour en cours de validité\r\n- ou VLSTS (Visa de Long Séjour valant Titre de Séjour) en cours de validité\r\n- ou récépissé de nouvelle demande de titre de séjour en cours de validité",
                'order_place': 14
            }
        }, {
            'value': '2018-05-10',
            'type_de_champ': {
                'id': 98297,
                'libelle': 'Date d’expiration',
                'type_champ': 'date',
                'description': '',
                'order_place': 15
            }
        }, {
            'value': '75 - Paris',
            'type_de_champ': {
                'id': 98298,
                'libelle': 'Département qui figure sur le titre de séjour',
                'type_champ': 'drop_down_list',
                'description': '',
                'order_place': 16
            }
        }, {
            'value': 'Préfecture de Paris',
            'type_de_champ': {
                'id': 98299,
                'libelle': 'Délivré par',
                'type_champ': 'text',
                'description': 'Par exemple : Préfecture de Paris',
                'order_place': 17
            }
        }, {
            'value': None,
            'type_de_champ': {
                'id': 98300,
                'libelle': 'Employeur',
                'type_champ': 'header_section',
                'description': '',
                'order_place': 18
            }
        }, {
            'value': '2018-08-28',
            'type_de_champ': {
                'id': 98301,
                'libelle': 'Date de fin',
                'type_champ': 'date',
                'description': '',
                'order_place': 29
            }
        }, {
            'value': '2018-03-28',
            'type_de_champ': {
                'id': 98302,
                'libelle': 'Date de début',
                'type_champ': 'date',
                'description': '',
                'order_place': 28
            }
        }, {
            'value': None,
            'type_de_champ': {
                'id': 98306,
                'libelle': 'Informations sur le contrat',
                'type_champ': 'header_section',
                'description': '',
                'order_place': 24
            }
        }, {
            'value': 'Bob',
            'type_de_champ': {
                'id': 98309,
                'libelle': "Prénom de l'employeur",
                'type_champ': 'text',
                'description': '',
                'order_place': 21
            }
        }, {
            'value': 'Morane',
            'type_de_champ': {
                'id': 98310,
                'libelle': "Nom de l'employeur",
                'type_champ': 'text',
                'description': '',
                'order_place': 20
            }
        }, {
            'value': '1485 euros/mois',
            'type_de_champ': {
                'id': 98312,
                'libelle': 'Salaire brut',
                'type_champ': 'text',
                'description': 'Au format : salaire brut en euros / fréquence. Par exemple : 1485 euros/mois, ou 9,88 euros/semaine etc.',
                'order_place': 31
            }
        }, {
            'value': '35 heures/semaine',
            'type_de_champ': {
                'id': 98313,
                'libelle': "Nombre d'heures",
                'type_champ': 'text',
                'description': 'Au format : heures / fréquence. Par exemple : 35 heures/semaine, ou 144 heures/mois etc.',
                'order_place': 30
            }
        }, {
            'value': 'contrat à durée déterminée (CDD)',
            'type_de_champ': {
                'id': 98303,
                'libelle': 'Type de contrat',
                'type_champ': 'drop_down_list',
                'description': '',
                'order_place': 27
            }
        }, {
            'value': "16 passage de l'Industrie\r\n75010 PARIS",
            'type_de_champ': {
                'id': 98304,
                'libelle': "Adresse ou l'étudiant va travailler",
                'type_champ': 'textarea',
                'description': '',
                'order_place': 26
            }
        }, {
            'value': 'Caissier',
            'type_de_champ': {
                'id': 98305,
                'libelle': 'Emploi occupé',
                'type_champ': 'text',
                'description': '',
                'order_place': 25
            }
        }],
        'invites': [],
        'archived': False,
        'created_at': '2018-03-27T08:49:51.491Z',
        'entreprise': {
            'nom': None,
            'siren': '528783921',
            'prenom': None,
            'date_creation': '2010-12-05T23:00:00.000Z',
            'capital_social': 3000,
            'nom_commercial': '',
            'raison_sociale': 'MEGACORP',
            'forme_juridique': 'SARL unipersonnelle ',
            'siret_siege_social': '52222222222222',
            'forme_juridique_code': '5498',
            'code_effectif_entreprise': '00',
            'numero_tva_intracommunautaire': 'FR22222222222'
        },
        'individual': None,
        'motivation': None,
        'updated_at': '2018-03-27T09:15:10.780Z',
        'received_at': '2018-03-27T09:10:38.231Z',
        'commentaires': [{
            'body': '[Votre dossier WorkInFrance nº\xa044950 a bien été reçu]<br><br><div>Bonjour,</div><div><br></div><div>Le service de la main d\'œuvre étrangère vous confirme la bonne réception de votre dossier nº 44950 de demande d\'autorisation provisoire de travail en faveur de M. Doe John.</div><div><br></div><div>A tout moment, vous pouvez consulter le contenu de vos dossiers et les éventuels commentaires de l\'administration à cette adresse : <a target="_blank" href="https://www.demarches-simplifiees.fr/users/dossiers/44950/recapitulatif">https://www.demarches-simplifiees.fr/users/dossiers/44950/recapitulatif</a></div><div><br></div><div>Bonne journée,</div><div><br></div><div>L\'équipe WorkInFrance</div><div><br></div><div>— </div><div><br></div><div>Merci de ne pas répondre à cet email. Postez directement vos questions dans votre dossier sur la plateforme.<br><br>Le texte du présent e-mail n\'a aucune valeur d\'autorisation provisoire. Seule l\'attestation d\'autorisation provisoire de travail au format PDF, si délivrée, fera foi.<br></div>',
            'email': 'contact@demarches-simplifiees.fr',
            'created_at': '2018-03-27T08:54:07.937Z'
        }, {
            'body': "[Votre dossier WorkInFrance nº\xa044950 va être instruit]<br><br><div>Bonjour,</div><div><br></div><div>Votre dossier nº 44950 de demande d'autorisation provisoire de travail en faveur de M. Doe John passe en instruction. Il sera traité dans le délai légal.</div><div><br></div><div>Bonne journée,</div><div><br></div><div>L'équipe WorkInFrance</div><div><br></div><div>— </div><div><br></div><div>Merci de ne pas répondre à cet email. Postez directement vos questions dans votre dossier sur la plateforme.</div><div><br></div><div>Le texte du présent e-mail n'a aucune valeur d'autorisation provisoire. Seule l'attestation d'autorisation provisoire de travail au format PDF, si délivrée, fera foi.</div><div><br></div>",
            'email': 'contact@demarches-simplifiees.fr',
            'created_at': '2018-03-27T09:10:42.513Z'
        }, {
            'body': "[Votre dossier WorkInFrance nº\xa044950 a été accepté]<br><br><div>Bonjour,</div><div><br></div><div>Le service de la main d'œuvre étrangère vous annonce que votre demande nº 44950 a été acceptée le 27/03/2018.</div><div><br></div><div>Vous trouverez ci-joint l'attestation d'autorisation provisoire de travail. Elle est également disponible au téléchargement sur votre espace personnel.<br><br>Si vous êtes l'employeur, merci de transmettre cette attestation à l'étudiant.<br></div><div><br></div><div>Bonne journée, </div><div><br></div><div>L'équipe WorkInFrance </div><div><br></div><div>— </div><div><br></div><div>Merci de ne pas répondre à cet email. Postez directement vos questions dans votre dossier sur la plateforme.</div><div><br></div><div>Pour toute question concernant votre attestation contactez-nous à contact@workinfrance.beta.gouv.fr</div><div><br></div><div>Le texte du présent e-mail n'a aucune valeur d'autorisation provisoire. Seule l'attestation d'autorisation provisoire de travail au format PDF ci-jointe fait foi.</div>",
            'email': 'contact@demarches-simplifiees.fr',
            'created_at': '2018-03-27T09:15:10.778Z'
        }],
        'initiated_at': '2018-03-27T08:54:07.829Z',
        'processed_at': '2018-03-27T09:15:08.829Z',
        'etablissement': {
            'naf': '6201Z',
            'siret': '52222222222222',
            'adresse': 'MEGACORP\r\n16 PASSAGE DE L INDUSTRIE\r\n75010 PARIS\r\nFRANCE',
            'localite': 'PARIS 10',
            'nom_voie': 'DE L INDUSTRIE',
            'type_voie': 'PAS',
            'code_postal': '75010',
            'libelle_naf': 'Programmation informatique',
            'numero_voie': '16',
            'siege_social': True,
            'complement_adresse': None,
            'code_insee_localite': '75110'
        },
        'champs_private': [{
            'value': '2018-03-27',
            'type_de_champ': {
                'id': 98315,
                'libelle': 'Date de début APT',
                'type_champ': 'date',
                'description': "Saisissez la date de début de validité de l'autorisation provisoire de travail. Elle sera utilisée dans l'attestation délivrée au demandeur.",
                'order_place': 0
            }
        }, {
            'value': '2018-05-10',
            'type_de_champ': {
                'id': 98317,
                'libelle': 'Date de fin APT',
                'type_champ': 'date',
                'description': "Saisissez la date de fin de validité de l'autorisation provisoire de travail. Elle sera utilisée dans l'attestation délivrée au demandeur.",
                'order_place': 1
            }
        }, {
            'value': '',
            'type_de_champ': {
                'id': 98318,
                'libelle': "Cadre réservé à l'administration",
                'type_champ': 'textarea',
                'description': "Ce cadre n'est pas visible par les usagers",
                'order_place': 2
            }
        }],
        'accompagnateurs': ['accompagnateur@direccte.gouv.fr'],
        'simplified_state': 'Accepté',
        'pieces_justificatives': [{
            'user': {
                'email': 'john@doe.com'
            },
            'created_at': '2018-03-27T08:54:07.397Z',
            'content_url': 'https://storage.apientreprise.fr/tps/piece_justificative-6d9d582c-a1b6-4ed7-a82f-b73ba507c222.jpg',
            'type_de_piece_justificative_id': 16016
        }, {
            'user': {
                'email': 'john@doe.com'
            },
            'created_at': '2018-03-27T08:54:07.015Z',
            'content_url': 'https://storage.apientreprise.fr/tps/piece_justificative-ccfb8898-c9f4-4320-8ca8-1f48253bfd26.jpg',
            'type_de_piece_justificative_id': 16015
        }, {
            'user': {
                'email': 'john@doe.com'
            },
            'created_at': '2018-03-27T08:54:06.481Z',
            'content_url': 'https://storage.apientreprise.fr/tps/piece_justificative-94b0b58b-9a31-43c3-8f57-d1e4d421c655.jpg',
            'type_de_piece_justificative_id': 16014
        }, {
            'user': {
                'email': 'john@doe.com'
            },
            'created_at': '2018-03-27T08:54:05.772Z',
            'content_url': 'https://storage.apientreprise.fr/tps/piece_justificative-631558ee-31e8-45a7-a38d-8182ba23875a.jpg',
            'type_de_piece_justificative_id': 16013
        }],
        'types_de_piece_justificative': [{
            'id': 16758,
            'libelle': 'Si vous êtes étudiant, le mandat',
            'description': 'vous autorisant à accomplir les démarches administratives au nom et pour le compte de votre employeur.',
            'order_place': 0,
            'lien_demarche': ''
        }, {
            'id': 16013,
            'libelle': 'Document(s) autorisant le séjour en France (recto-verso)',
            'description': 'Carte de séjour en cours de validité ou VLSTS (Visa de Long Séjour valant Titre de Séjour) en cours de validité ou en cas de renouvellement du titre de séjour : titre de séjour + récépissé de nouvelle demande de titre de séjour + Convocation à la Préfecture ou Sous-Préfecture',
            'order_place': 1,
            'lien_demarche': ''
        }, {
            'id': 16014,
            'libelle': 'Passeport',
            'description': '',
            'order_place': 2,
            'lien_demarche': ''
        }, {
            'id': 16015,
            'libelle': 'Carte d’étudiant en cours de validité',
            'description': 'ou certificat de scolarité en cours de validité',
            'order_place': 3,
            'lien_demarche': ''
        }, {
            'id': 16016,
            'libelle': 'Contrat de travail',
            'description': 'ou contrat d’apprentissage ou contrat de professionnalisation ou contrat doctoral',
            'order_place': 4,
            'lien_demarche': ''
        }, {
            'id': 16017,
            'libelle': 'En cas de profession réglementée, un justificatif',
            'description': "L'exercice de certaines activités est soumis à une autorisation ou un agrément préalable.",
            'order_place': 5,
            'lien_demarche': ''
        }, {
            'id': 16012,
            'libelle': "En cas de renouvellement d'autorisation provisoire de travail",
            'description': 'votre ancienne autorisation de travail + vos 3 dernières fiches de paie (1 seul document contenant plusieurs pages)',
            'order_place': 6,
            'lien_demarche': ''
        }]
    }
}

# pylint:enable=line-too-long
