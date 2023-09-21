import json
import time

from django.core.handlers.wsgi import WSGIRequest
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from .redis import redis_instance
from .services import get_domain_from_url


@csrf_exempt
def visited_links(request: WSGIRequest) -> JsonResponse:
    """View for adding visited links to Redis."""
    if request.method != 'POST':
        return JsonResponse({"status": "only POST method allowed"}, status=405)

    links = json.loads(request.body).get('links')
    epoch_time_now = int(time.time())

    pipeline = redis_instance.pipeline()
    try:
        for link in links:
            if not get_domain_from_url(link):
                raise ValueError(f"bad link: {link} (doesn't contain a domain)")
            redis_instance.zadd('links', {link: epoch_time_now})
        pipeline.execute()
    except ValueError as e:
        return JsonResponse({"status": str(e)}, status=400)

    return JsonResponse({"status": "ok"})


@csrf_exempt
def visited_domains(request: WSGIRequest) -> JsonResponse:
    """View for retrieving unique domains visited within a specified time interval."""

    if request.method != 'GET':
        return JsonResponse({"status": "only GET method allowed"}, status=405)

    try:
        from_timestamp = int(request.GET.get('from', 0))
    except ValueError:
        return JsonResponse({"status": "'from' must be integer"}, status=400)

    try:
        to_timestamp = int(request.GET.get('to', int(time.time())))
    except ValueError:
        return JsonResponse({"status": "'to' must be integer"}, status=400)

    links = redis_instance.zrangebyscore('links', from_timestamp, to_timestamp)
    domains = set([get_domain_from_url(link.decode('utf-8')) for link in links])

    return JsonResponse({
        "domains": list(domains),
        "status": "ok"
    }, status=200)
