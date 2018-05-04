"""
Add permissions for proxy models.

https://code.djangoproject.com/ticket/11154

When a permission is created for a proxy model, it actually creates it for it's
base model app_label.

What we need, however, is the permission to be created for the proxy model
itself, in order to have the proper entries displayed in the admin.
"""
from django.apps import apps
from django.contrib.auth.management import _get_all_permissions
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from django.core.management.base import BaseCommand


class Command(BaseCommand):

    help = 'Add permissions for proxy models in order to have the proper entries displayed in the admin.'

    def handle(self, *args, **options):

        for model in apps.get_models():

            opts = model._meta
            ctype, _ = ContentType.objects.get_or_create(
                app_label=opts.app_label,
                model=opts.object_name.lower()
            )

            for codename, name in _get_all_permissions(opts):
                perm, created = Permission.objects.get_or_create(
                    codename=codename,
                    content_type=ctype,
                    defaults={'name': name}
                )
                if created:
                    self.stdout.write(f'Adding permission {perm}')
