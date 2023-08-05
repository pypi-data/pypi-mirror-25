from django.http import HttpResponse
from django.views.decorators.http import require_http_methods

from .enums import JobState
from .models import Job
from .responses import InvalidTokenHttpResponse403, \
    JobUpdatedJsonResponse200, InvalidJobHttpResponse404, \
    InvalidJobStatusHttpResponse422
from .utils import get_metadata


@require_http_methods(['POST'])
def accept_payload(request) -> HttpResponse:
    """Endpoint for accepting json payloads via http post. This endpoint is
    meant to be utilized by human clients.

    :example:
    >>> request.POST = {
    ...    "auth": "...",
    ...    "rows": [{"...": "..."}]
    ... }
    """

    token: str = request.POST.get('token')
    rows: list = request.POST.get('rows')

    try:
        meta = get_metadata(token)
    except ValueError:
        return InvalidTokenHttpResponse403(token)

    job: Job = Job.objects.create(
        ds_name=meta.name,
        ds_table_name=meta.slug,
        ds_fields=meta.ds_fields,
        ds_contributor_email=meta.contributor,
        payload=rows,
        token=token
    )

    return JobUpdatedJsonResponse200(job.id)


@require_http_methods(['POST'])
def accept_job_status(request) -> HttpResponse:
    """Endpoint for accepting job results. This endpoint is meant to be
    utilized by stream consumers.

    request.POST = {
        'id': 0,
        'status': 'received' (or 'error', 'success')
    }
    """

    job_id: int = request.POST.get('id')
    job_status: str = request.POST.get('status')

    try:
        job: Job = Job.objects.get(id=job_id)
    except (Job.DoesNotExist, ValueError):
        return InvalidJobHttpResponse404(job_id)

    try:
        job_state = JobState.from_string(job_status)
    except ValueError:
        return InvalidJobStatusHttpResponse422(job_status)

    if job_state == JobState.Queued:
        job.mark_queued()
    elif job_state == JobState.Received:
        job.mark_received()
    elif job_state == JobState.Success:
        job.handle_success()
    else:
        job.handle_error()
    job.save()

    return JobUpdatedJsonResponse200(job.id)
