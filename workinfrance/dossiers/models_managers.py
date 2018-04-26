import datetime

from django.contrib.postgres.fields.jsonb import KeyTextTransform
from django.db import models
from django.db.models import Count, Sum
from django.db.models.expressions import F, ExpressionWrapper
from django.db.models.functions import TruncDate, TruncMonth
from django.utils import timezone


class CompletedManager(models.Manager):

    def get_queryset(self):
        return super().get_queryset().filter(status__in=self.model.STATUSES_COMPLETED)


class StatsQueries(models.QuerySet):

    def get_num_by_country(self):
        """
        Number of dossiers by country.
        """
        return (
            self
            .annotate(nationalite=KeyTextTransform('nationalite', 'champs_json'))
            .values('nationalite')
            .annotate(total=Count('nationalite'))
            .order_by('-total')
        )

    def get_num_by_day(self, from_datetime=None, to_datetime=None):
        """
        Number of dossiers by day (during the last 31 days by default).
        """
        if not from_datetime:
            from_datetime = timezone.now() - datetime.timedelta(days=31)
        if not to_datetime:
            to_datetime = timezone.now()
        return (
            self
            .filter(created_at__range=(from_datetime, to_datetime))
            .annotate(day=TruncDate('created_at'))
            .values('day')
            .annotate(total=Count('day'))
            .order_by('day')
        )

    def get_num_by_month(self, from_datetime=None, to_datetime=None):
        """
        Number of dossiers by day (during the last 365 days by default).
        """
        if not from_datetime:
            from_datetime = timezone.now() - datetime.timedelta(days=365)
        if not to_datetime:
            to_datetime = timezone.now()
        return (
            self
            .filter(created_at__range=(from_datetime, to_datetime))
            .annotate(month=TruncMonth('created_at'))
            .values('month')
            .annotate(total=Count('month'))
            .order_by('month')
        )

    def get_num_by_status(self):
        """
        Number of dossiers in each status.
        Note: 0 values are not included in GROUP BY => build and return a custom dict.
        """
        statuses_count = {
            item['status']: item['status_count']
            for item in self.model.objects.values('status').annotate(status_count=Count('status'))
        }
        for key in dict(self.model.STATUS_CHOICES):
            if key not in statuses_count:
                statuses_count[key] = 0
        return statuses_count

    def get_time_to_process(self):
        """
        Global average time to process a dossier.
        """
        q = (
            self
            .annotate(
                processing_duration=ExpressionWrapper(
                    F('updated_at') - F('created_at'), output_field=models.DurationField()
                )
            )
            .values_list('processing_duration', flat=True)
        )
        time_to_process = sum(q, datetime.timedelta()) / len(q)
        return time_to_process  # Return a timedelta object.

    def get_time_to_process_by_month(self, from_datetime=None, to_datetime=None):
        """
        Average time to process a dossier by month (during the last 365 days by default).
        """
        if not from_datetime:
            from_datetime = timezone.now() - datetime.timedelta(days=365)
        if not to_datetime:
            to_datetime = timezone.now()
        q = (
            self
            .filter(created_at__range=(from_datetime, to_datetime))
            .annotate(month=TruncMonth('created_at'))
            .values('month')
            .annotate(
                total_dossiers=Count('month'),
                processing_duration=Sum(ExpressionWrapper(
                    F('updated_at') - F('created_at'), output_field=models.DurationField()
                )
            ))
            .order_by('month')
        )
        return [
            {
                'time_to_process': item['processing_duration'] / item['total_dossiers'],
                'total_dossiers': item['total_dossiers'],
                'month': item['month'],
            }
            for item in q
        ]
