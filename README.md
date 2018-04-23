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

## Récupération des dossiers depuis demarches-simplifiees.fr

```shell
$ docker exec -t wif_django python manage.py sync_dossiers
```

## Exporter le fichier JSON du *validity check*

```shell
$ docker exec -t wif_django python manage.py export_validity_check_data
```

## Lancement des tests unitaires

```shell
$ docker exec -t wif_django python manage.py test
```

## Vérification de la syntaxe du code

```shell
$ make pylint
```

## Mémo

```shell
$ docker exec -ti wif_django /bin/sh
$ psql -U postgres --host=0.0.0.0 --port=5433
```
