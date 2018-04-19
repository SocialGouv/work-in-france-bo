# Work in France - Back office

> Back office de la plateforme de demande d'autorisations provisoires de travail.

Ce dépôt de code contient le back office de Work in France.

## Installation de l'environnement de développement

### Création de l'environnement Python isolé

Avec Python 3.6 et [`pipenv (>=11.8.3)`](https://github.com/pypa/pipenv) :

```bash
$ pipenv --python 3.6
$ pipenv install
$ pipenv install --dev
```

### Création d'une base de donnée PostgreSQL (>= 9.5.12)

```shell
$ psql -U postgres
postgres=# create database work_in_france_bo;
```

### Paramétrage du fichier `.env`

Pour utiliser la commande `django-admin`, le répertoire `work-in-france-bo` doit figurer dans votre `PYTHONPATH`.

    PYTHONPATH=/your/path/to/work-in-france-bo

    DJANGO_SETTINGS_MODULE='workinfrance.settings'

    WIF_SECRET_KEY='<SECRET>'

    WIF_DEBUG=True

    WIF_DATABASE_NAME='work_in_france_bo'
    WIF_DATABASE_USER='postgres'
    WIF_DATABASE_PASSWORD=''
    WIF_DATABASE_HOST='localhost'
    WIF_DATABASE_PORT='5432'

    DEMARCHES_SIMPLIFIEES_API_TOKEN='<SECRET>'
    DEMARCHES_SIMPLIFIEES_PROCEDURE_ID_APT='<SECRET>'

### Initialisation du projet

```shell
$ pipenv run django-admin migrate
$ pipenv run django-admin createsuperuser
```

## Récupération des dossiers depuis demarches-simplifiees.fr

```shell
$ pipenv run django-admin sync_dossiers
```

## Exporter le fichier JSON du *validity check*

```shell
pipenv run django-admin export_validity_check_data
```

## Lancement du serveur de développement

```shell
$ pipenv run django-admin runserver
```

## Lancement des tests unitaires

```shell
$ pipenv run django-admin test
```

## Vérification de la syntaxe du code

```shell
$ make pylint
```
