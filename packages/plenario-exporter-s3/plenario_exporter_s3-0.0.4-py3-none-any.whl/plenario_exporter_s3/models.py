import logging
from datetime import datetime
from typing import List, Union
from uuid import uuid4

import arrow
from channels import Channel
from django.contrib.gis.db.models import PolygonField
from django.contrib.gis.geos import Polygon
from django.contrib.postgres.fields import DateTimeRangeField, JSONField
from django.db import models
from django.utils.translation import ugettext as _
from django_fsm import ConcurrentTransitionMixin, FSMField, transition
from psycopg2.extras import DateTimeTZRange

from plenario_exporter_s3.enums import State


logger = logging.getLogger(__name__)


class ExportJob(ConcurrentTransitionMixin, models.Model):

    # random, non-integer identifier
    id: str = models.UUIDField(
        primary_key=True,
        editable=False,
        default=uuid4,
        blank=True,
        help_text=_('The job identifier'))
    requestor: str = models.EmailField(
        help_text=_('The email address of the requestor'))
    state: State = FSMField(
        default=State.New.value,
        protected=True,
        help_text=_('The job state'))

    # track errors locally
    error_dump: Union[str, None] = models.TextField(
        null=True,
        default=None,
        help_text=_('Processing error trace'))

    # job run times
    date_started: datetime = models.DateTimeField(
        null=True,
        default=None,
        editable=False,
        blank=True,
        help_text=_('The date time the job started'))
    date_completed: datetime = models.DateTimeField(
        null=True,
        default=None,
        editable=False,
        blank=True,
        help_text=_('The date time the job completed'))

    # s3 information
    bucket: str = models.URLField(
        null=True,
        default=None,
        editable=False,
        blank=True,
        help_text=_('The URL to the S3 bucket with the exported file'))
    date_expires: datetime = models.DateTimeField(
        null=True,
        default=None,
        editable=False,
        blank=True,
        help_text=_('The expiration date of the exported file (TTL)'))

    def __str__(self) -> str:
        return str(self.pk)

    @transition(
        field=state,
        source=State.New.value,
        target=State.Processing.value)
    def start_job(self) -> None:
        Channel('async-export').send({'pk': str(self.pk)})
        self.date_started = arrow.utcnow().datetime
        logger.info(f'Started job {self.pk}')

    @transition(
        field=state,
        source=State.Processing.value,
        target=State.Completed.value)
    def mark_completed(self) -> None:
        # TODO: send an email with the bucket link and ttl to the requestor
        self.date_completed = arrow.utcnow().datetime
        logger.info(f'Completed job {self.pk}')

    @transition(
        field=state,
        source='*',
        target=State.Erred.value)
    def mark_erred(self, dump: str) -> None:
        self.error_dump = dump
        logger.error(f'Job {self.pk} encountered an error: {dump}')
        # TODO: send an email to the admins and the requestor


class DataSetInfo(models.Model):

    job: 'ExportJob' = models.ForeignKey(
        to='ExportJob',
        related_name='data_sets',
        help_text=_('The job this data set info is related to'))

    # data set info
    meta_model_app_label: str = models.TextField(
        help_text=_('The app label of the meta model'))
    meta_model_class_name: str = models.TextField(
        help_text=_('The class name of the meta model'))
    meta_model_pk: str = models.TextField(
        help_text=_('The primary key of the meta model instance')
    )

    # restrictions
    fields: List[str] = JSONField(
        null=True,
        default=None,
        help_text=_('A list of fields to include'))
    point_field: str = models.TextField(
        help_text=_('Name of point field to filter by'))
    date_field: str = models.TextField(
        help_text=_('Name of date field to filter by'))
    timerange: DateTimeTZRange = DateTimeRangeField(
        help_text=_('The time range to limit exported rows'))
    bbox: Polygon = PolygonField(
        help_text=_('The bounding box to limit exported rows'))

    def __str__(self) -> str:
        return f'{self.job}: ' \
               f'{self.meta_model_app_label}.{self.meta_model_class_name}'
