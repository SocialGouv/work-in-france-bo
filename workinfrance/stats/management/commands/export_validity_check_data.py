import json
import os

from django.conf import settings
from django.core.management.base import BaseCommand
from django.core.serializers.json import DjangoJSONEncoder

from workinfrance.stats.views import export_data_for_validity_check


class Command(BaseCommand):

    help = 'Export a JSON file containing the validity check data.'

    def handle(self, *args, **options):
        file_path = os.path.join(settings.MEDIA_ROOT, 'validity_check.json')
        data = export_data_for_validity_check()
        with open(file_path, 'w') as outfile:
            json.dump(data, outfile, cls=DjangoJSONEncoder)
        self.stdout.write(f"{len(data)} dossiers exported.")
        self.stdout.write("Done.")
