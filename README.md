# Work in France - Back office

> Back office privé de la plateforme de demande d'autorisations provisoires de travail.

Ce dépôt de code contient le back office privé de Work in France. Les données qu'il contient ne sont jamais exposées directement.

## Installation de l'environnement de développement

### Paramétrage du fichier `.env` (utilisé par Docker)

    PYTHONPATH=.

    DJANGO_SETTINGS_MODULE=workinfrance.settings

    WIF_SECRET_KEY=<SECRET>

    WIF_DEBUG=True

    POSTGRES_USER=postgres
    POSTGRES_PASSWORD=dev_password

    WIF_DATABASE_NAME=work_in_france_bo
    WIF_DATABASE_USER=work_in_france
    WIF_DATABASE_PASSWORD=dev_password
    WIF_DATABASE_HOST=db
    WIF_DATABASE_PORT=5432

    DEMARCHES_SIMPLIFIEES_API_TOKEN=<SECRET>
    DEMARCHES_SIMPLIFIEES_PROCEDURE_ID_APT=<SECRET>

### Création des instances Docker

```bash
$ docker-compose up
```

### Initialisation du projet

```shell
$ docker exec -t wif_django pipenv run python manage.py migrate
$ docker exec -ti wif_django pipenv run python manage.py createsuperuser
```

## Workflow de mise à jour des dépendances du projet :

```shell
# Voir la liste de ce qui a changé upstream
$ docker exec -t wif_django pipenv update --dev --outdated

# Mise à jour de toutes les dépendances
$ docker exec -t wif_django pipenv update

# Mise à jour par paquet
$ docker exec -t wif_django pipenv update <pkg>
```

## Exécution des commandes django-admin

```shell
# Récupération des dossiers depuis demarches-simplifiees.fr
$ docker exec -t wif_django pipenv run python manage.py sync_dossiers

# Exporter le fichier JSON du *validity check*
$ docker exec -t wif_django pipenv run python manage.py export_validity_check_data

# Exporter le fichier JSON des statistiques
$ docker exec -t wif_django pipenv run python manage.py export_stats_data

# Lancement des tests unitaires
$ docker exec -t wif_django pipenv run python manage.py test
```

## Vérification de la syntaxe du code

```shell
$ make pylint
```

## Mémo (environnement de développement)

```shell
# Ouvrir un shell dans l'instance Docker.
$ docker exec -ti wif_django /bin/sh

# Ouvrir un shell Django dans l'instance Docker.
$ docker exec -ti wif_django pipenv run python manage.py shell

# Se connecter au PostgreSQL de l'instance Docker.
$ psql -U postgres --host=0.0.0.0 --port=5433
```

## Export et partage de fichiers JSON entre les back-offices

Les deux back-offices (celui-ci et [`work-in-france-bo-public`](https://github.com/SocialGouv/work-in-france-bo-public)) sont lancés en production avec `docker-compose` et `docker`. Des volumes sont utilisés pour pouvoir mettre à jour et partager des fichiers JSON :

```shell
# Lancement du back-office privé.
$ cd work-in-france-bo && sudo docker-compose up -d

# Lancement du back-office public.
$ sudo docker run --restart=always -d -p 1337:1337 -v $PWD/validity_check.json:/app/src/server/apt/validity_check.json -v $PWD/stats.json:/app/src/server/public/stats.json wif-bo-public
```

### Partage du fichier JSON du *validity check*

Le *validity check* est un mécanisme permettant de vérifier l'authenticité d'une attestation délivrée par Work in France.

Fonctionnement du mécanisme :

- une page du site web ([`work-in-france`](https://github.com/SocialGouv/work-in-france)) interroge une API du back-office public
- l'API du back-office public ([`work-in-france-bo-public`](https://github.com/SocialGouv/work-in-france-bo-public)) parse un fichier JSON contenant des données anonymisées
- ce ficher JSON est généré par le back-office privé (ce dépôt de code) via la commande django-admin `export_validity_check_data`
- une tâche CRON déclenche la génération de ce fichier JSON et en fait une copie dans un dossier monté en tant que volume dans l'instance Docker du back-office public

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

### Partage du fichier JSON des statistiques

Une page publique de statistiques est disponible sur le site web ([`work-in-france`](https://github.com/SocialGouv/work-in-france)) :

- cette page charge ses données depuis un fichier JSON
- ce fichier JSON est un fichier statique servi par le back-office public ([`work-in-france-bo-public`](https://github.com/SocialGouv/work-in-france-bo-public))
- c'est le back-office privé (ce dépôt de code) qui génère ce fichier JSON via la commande django-admin `export_stats_data`
- une tâche CRON déclenche la génération de ce fichier JSON et en fait une copie dans un dossier monté en tant que volume dans l'instance Docker du back-office public

Paramétrage du CRON pour mettre à jour et fournir `stats.json` au back-office public :

```shell
# https://crontab.guru/#0_9_*_*_*
# Every day at 09:00.
0 9 * * * /usr/bin/docker exec -t wif_django python manage.py export_stats_data && cp /home/mitech/work-in-france-bo/workinfrance/media/stats.json /home/mitech/work-in-france-bo-public/stats.json && chown mitech:mitech /home/mitech/work-in-france-bo-public/stats.json && chmod 664 /home/mitech/work-in-france-bo-public/stats.json
```
