from django.http import HttpResponse, JsonResponse


def InvalidTokenHttpResponse403(token: str) -> HttpResponse:
    message = 'Invalid token: {}'.format(token)
    return HttpResponse(message, status=403)


def InvalidJobHttpResponse404(id: int) -> HttpResponse:
    message = 'Invalid job id: {}'.format(id)
    return HttpResponse(message, status=404)


def InvalidJobStatusHttpResponse422(status: str) -> HttpResponse:
    message = 'Invalid job status: {}'.format(status)
    return HttpResponse(message, status=422)


def JobUpdatedJsonResponse200(job_id: int) -> HttpResponse:
    return JsonResponse({
        'job_id': job_id
    })
