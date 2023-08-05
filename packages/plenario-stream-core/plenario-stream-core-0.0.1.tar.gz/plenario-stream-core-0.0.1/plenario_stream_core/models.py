from datetime import datetime
from typing import List

from django.db.models import DateTimeField, Model, TextField
from django.contrib.postgres.fields import JSONField
from django_fsm import FSMField, transition

from .enums import JobState
from .signals import job_created
from .utils import get_bbox, get_metadata, get_timerange, send_email


class Job(Model):
    """Instances of this class represent the status of work being performed
    by stream consumers.

    :attr token: uniquely identifies a dataset

    :attr ds_name: human readable name of the target dataset
    :attr ds_table_name: name of the dataset in the database
    :attr ds_fields: mapping of dataset field names to db types
    :attr ds_contributor_email: email address of the dataset contributor

    :attr dt_received: time at which job was received
    :attr dt_queued: time at which job was submitted to kinesis
    :attr dt_exit: time at which the job exited due to success or error

    :attr payload: a copy of the payload to be used by producers
    :attr errors: list of errors, if any
    :attr status: queued, received, error, success
    """

    token: str = TextField()

    ds_name: str = TextField()
    ds_table_name: str = TextField()
    ds_fields: dict = JSONField(default={})
    ds_contributor_email: str = TextField()

    dt_received: datetime = DateTimeField(default=None, null=True)
    dt_queued: datetime = DateTimeField(default=None, null=True)
    dt_exit: datetime = DateTimeField(default=None, null=True)

    payload: List[dict] = JSONField(default=None, null=True)
    errors: list = JSONField(default=None, null=True)
    state: str = FSMField(default=JobState.New.value, protected=True)

    def save(self, *args, **kwargs):
        """Sends a `job_created` signal after an instance has been saved.
        """
        super().save(*args, **kwargs)
        job_created.send(sender=self.__class__, instance=self)

    @transition(
        field=state,
        source=JobState.New.value,
        target=JobState.Queued.value,
        on_error=JobState.Error.value)
    def mark_queued(self):
        pass

    @transition(
        field=state,
        source=JobState.Queued.value,
        target=JobState.Received.value,
        on_error=JobState.Error.value)
    def mark_received(self):
        pass

    @transition(
        field=state,
        source=JobState.Received.value,
        target=JobState.Success.value,
        on_error=JobState.Error.value)
    def handle_success(self):
        """Encompasses all the actions that need to be taken when a 'success'
        state is reported by a worker.

        1) Set the job state to 'success'
        2) Update the metadata location and time bounds
        """
        meta = get_metadata(self.token)
        meta.ds_bbox = get_bbox(meta)
        meta.ds_timerange = get_timerange(meta)
        meta.save()

    @transition(field=state, source='*', target=JobState.Error)
    def handle_error(self) -> dict:
        """Encompasses all the actions that need to be taken when an 'error'
        state is reported by a worker.

        1) Set the job state to 'error'
        2) Send an email to notify the payload contributor
        """
        send_email(
            addresses=[self.ds_contributor_email],
            subject='Plenario ETL Error',
            body='Your most recent payload failed to be ingested.'
        )
