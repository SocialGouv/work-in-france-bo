# Work in France - Back office

> Back office de la plateforme de demande d'autorisations provisoires de travail.

Ce dépôt de code contient le back office de Work in France.

## Installation de l'environnement de développement

### Paramétrage du fichier `.env` (utilisé par Docker)

    PYTHONPATH=.

    DJANGO_SETTINGS_MODULE='workinfrance.settings'

    WIF_SECRET_KEY='<SECRET>'

    WIF_DEBUG=True

    POSTGRES_USER=postgres
    POSTGRES_PASSWORD=dev_password

    WIF_DATABASE_NAME=work_in_france_bo
    WIF_DATABASE_USER=work_in_france
    WIF_DATABASE_PASSWORD=dev_password
    WIF_DATABASE_HOST=db
    WIF_DATABASE_PORT=5432

    DEMARCHES_SIMPLIFIEES_API_TOKEN='<SECRET>'
    DEMARCHES_SIMPLIFIEES_PROCEDURE_ID_APT='<SECRET>'

### Création des instances Docker

```bash
$ docker-compose up
```

### Initialisation du projet

```shell
$ docker exec -t wif_django python manage.py migrate
$ docker exec -ti wif_django python manage.py createsuperuser
```

## Exécution des commandes django-admin

```shell
# Récupération des dossiers depuis demarches-simplifiees.fr
$ docker exec -t wif_django python manage.py sync_dossiers

# Exporter le fichier JSON du *validity check*
$ docker exec -t wif_django python manage.py export_validity_check_data

# Lancement des tests unitaires
$ docker exec -t wif_django python manage.py test
```

## Vérification de la syntaxe du code

```shell
$ make pylint
```

## Mémo (en environnement de développement)

```shell
# Ouvrir un shell dans l'instance Docker.
$ docker exec -ti wif_django /bin/sh

# Ouvrir un shell Django dans l'instance Docker.
$ docker exec -ti wif_django python manage.py shell

# Se connecter au PostgreSQL de l'instance Docker.
$ psql -U postgres --host=0.0.0.0 --port=5433
```

## Mécanisme du *validity check*

Le *validity check* est un mécanisme permettant de vérifier l'authenticité d'une attestation délivrée par Work in France.

Ce mécanisme est composé :

- d'une interface publique sur un site web ([`work-in-france`](https://github.com/SocialGouv/work-in-france)) qui interroge une API du back-office public
- d'un back-office public ([`work-in-france-bo-public`](https://github.com/SocialGouv/work-in-france-bo-public)) comprenant une API qui expose des données anonymisées fournies par un back-office privé
- d'un back-office privé (ce dépôt de code) qui récupère et traite les données depuis l'API de demarches-simplifiees.fr

Le back-office privé génère un fichier `validity_check.json` via la commande django-admin `export_validity_check_data`. Ce fichier est ensuite passé au back-office public.

Cette tâche est automatisée via un CRON sur la machine de production.

Rappel : les deux back-offices sont lancés avec `docker` et `docker-compose` et **un volume** est utilisé pour pouvoir mettre à jour le fichier `validity_check.json` :

```shell
# Lancement du back-office privé.
$ cd work-in-france-bo && sudo docker-compose up -d

# Lancement du back-office public.
$ sudo docker run --restart=always -d -p 1337:1337 -v $PWD/validity_check.json:/app/src/server/apt/validity_check.json wif-bo-public
```

Paramétrage du CRON pour mettre à jour et fournir `validity_check.json` au back-office public :

```shell
# Ajouter un CRON en root.
$ sudo crontab -e

# https://crontab.guru/#0_*_9-19_*_1-5
# At minute 0 on every day-of-month from 9 through 19 and on every day-of-week from Monday through Friday.
0 * 9-19 * 1-5 /usr/bin/docker exec -t wif_django python manage.py sync_dossiers && /usr/bin/docker exec -t wif_django python manage.py export_validity_check_data && cp /home/mitech/work-in-france-bo/workinfrance/media/validity_check.json /home/mitech/work-in-france-bo-public/validity_check.json && chown mitech:mitech /home/mitech/work-in-france-bo-public/validity_check.json && chmod 664 /home/mitech/work-in-france-bo-public/validity_check.json

# Voir les CRON.
$ sudo crontab -l

# Voir les logs.
$ grep CRON /var/log/syslog | grep WorkInFrance
```
