from django.db import models


class CompletedManager(models.Manager):

    def get_queryset(self):
        return super().get_queryset().filter(status__in=self.model.STATUSES_COMPLETED)
