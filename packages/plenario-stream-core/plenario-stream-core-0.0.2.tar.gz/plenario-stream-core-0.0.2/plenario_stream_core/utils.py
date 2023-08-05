from typing import List

import boto3
from django.db.models import Max, Min
from django.contrib.gis.db.models import Extent
from django.contrib.gis.gdal import Envelope
from plenario_core.mixins import StreamingDataMixin
from plenario_core.utils.dynamic_models import get_subclasses

from .defaults import EMAIL_ADDRESS, USE_AWS_CREDENTIALS
from .stubs import SESStub


if USE_AWS_CREDENTIALS:  # NOQA
    SES = boto3.client('ses')
else:
    SES = SESStub()


def get_bbox(meta: StreamingDataMixin) -> str:
    """Calculate the bounding box of all point fields for a given dataset
    described by a provided meta object.
    """
    model = meta.get_ds_model()
    envelope = None
    for field in meta.ds_geo_field_names:
        queryset = model.objects.aggregate(Extent(field))
        extent = queryset[field + '__extent']
        if envelope:
            envelope.expand_to_include(Envelope(extent))
        else:
            envelope = Envelope(extent)
    if envelope:
        return envelope.wkt


def get_timerange(meta: StreamingDataMixin):
    """Calculate the bounding datetimes of all date fields for a given dataset
    described by a provided meta object.
    """
    model = meta.get_ds_model()
    daterange = None
    for field in meta.ds_date_field_names:
        queryset = model.objects.aggregate(Min(field), Max(field))
        min_dt = queryset[field + '__min']
        max_dt = queryset[field + '__max']
        if daterange:
            daterange[0] = min(daterange[0], min_dt)
            daterange[1] = max(daterange[1], max_dt)
        else:
            daterange = [min_dt, max_dt]
    return daterange


def get_metadata(token: str) -> StreamingDataMixin:
    """Iterate through the metadata types for metadata classes that make
    use of the StreamingDataMixin. If the token can't be found for any of
    the subclasses then the dataset must not exist.
    """
    for subclass in get_subclasses(StreamingDataMixin):
        try:
            meta: StreamingDataMixin = subclass.objects.get(_token=token)
            return meta
        except subclass.DoesNotExist:
            pass
    raise ValueError('Invalid token {}'.format(token))


def send_email(addresses: List[str], subject: str, body: str) -> dict:
    """This is a helper to reduce the amount of boilerplate needed to send an
    email with the AWS SES client.
    """
    return SES.send_email(
        Source=EMAIL_ADDRESS,
        Destination={
            'ToAddresses': addresses
        },
        Message={
            'Subject': {
                'Data': subject,
                'Charset': 'utf-8'
            },
            'Body': {
                'Text': {
                    'Data': body,
                    'Charset': 'utf-8'
                }
            }
        }
    )
