import datetime

from django.contrib.postgres.fields.jsonb import KeyTextTransform
from django.db import models
from django.db.models import Count, Sum
from django.db.models.expressions import F, ExpressionWrapper
from django.db.models.functions import TruncDate, TruncMonth
from django.utils import timezone

from workinfrance.dossiers import utils


class StatsQueries(models.QuerySet):

    def get_num_by_country(self):
        """
        Number of dossiers by country.

        Returns a dict:
            {
                'ALGERIE': 63,
                'MAROC': 6,
                …
            }
        """
        return dict(
            self
            .annotate(nationalite=KeyTextTransform('nationalite', 'champs_json'))
            .values('nationalite')
            .annotate(total=Count('nationalite'))
            .order_by('-total')
            .values_list('nationalite', 'total')
        )

    def get_num_by_day(self, from_datetime=None, to_datetime=None):
        """
        Number of dossiers by day (during the last 31 days by default).

        Returns a dict:
            {
                datetime.date(2018, 3, 26): 0,
                datetime.date(2018, 3, 27): 5,
                …
            }
        """
        if not all([from_datetime, to_datetime]):
            to_datetime = timezone.now()
            from_datetime = to_datetime - datetime.timedelta(days=31)
        q = dict(
            self
            .filter(created_at__range=(from_datetime, to_datetime))
            .annotate(day=TruncDate('created_at'))
            .values('day')
            .annotate(total=Count('day'))
            .order_by('day')
            .values_list('day', 'total')
        )
        return {
            # Include days with 0 dossiers (because they are not included in the queryset result).
            date: q.get(date, 0)
            for date in utils.daterange(from_datetime, to_datetime)
        }

    def get_num_by_month(self, from_datetime=None, to_datetime=None):
        """
        Number of dossiers by month (during the last 365 days by default).

        Returns a dict:
            {
                datetime.datetime(2018, 3, 1, 0, 0, tzinfo=<UTC>): 11,
                datetime.datetime(2018, 4, 1, 0, 0, tzinfo=<UTC>): 80,
                …
            }
        """
        if not all([from_datetime, to_datetime]):
            to_datetime = timezone.now()
            from_datetime = to_datetime - datetime.timedelta(days=365)
        return dict(
            self
            .filter(created_at__range=(from_datetime, to_datetime))
            .annotate(month=TruncMonth('created_at'))
            .values('month')
            .annotate(total=Count('month'))
            .order_by('month')
            .values_list('month', 'total')
        )

    def get_num_by_status(self):
        """
        Number of dossiers in each status.

        Returns a dict:
            {
                'initiated': 15,
                'closed': 74,
                …
            }
        """
        statuses_count = {
            item['status']: item['status_count']
            for item in self.model.objects.values('status').annotate(status_count=Count('status'))
        }
        # 0 values are not included in GROUP BY => build and return a custom dict.
        for key in dict(self.model.STATUS_CHOICES):
            if key not in statuses_count:
                statuses_count[key] = 0
        return statuses_count

    def get_time_to_process(self):
        """
        Global average time to process a dossier.

        Returns a datetime.timedelta object.
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

        Returns a dict:
            {
                datetime.datetime(2018, 3, 1, 0, 0, tzinfo=<UTC>): datetime.timedelta(4, 26541, 816444),
                datetime.datetime(2018, 4, 1, 0, 0, tzinfo=<UTC>): datetime.timedelta(1, 48285, 414538),
                …
            }
        """
        if not all([from_datetime, to_datetime]):
            to_datetime = timezone.now()
            from_datetime = to_datetime - datetime.timedelta(days=365)
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
        return {
            item['month']: item['processing_duration'] / item['total_dossiers']
            for item in q
        }
