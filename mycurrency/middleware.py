import json
from django.utils.deprecation import MiddlewareMixin
from django.http import JsonResponse

class ProcessBodyMiddleware(MiddlewareMixin):
    def process_request(self, request):
        if request.content_type == 'application/json':
            try:
                body_unicode = request.body.decode('utf-8')
                body = json.loads(body_unicode)
                request.data = body

            except (json.JSONDecodeError, KeyError) as e:
                return JsonResponse({'error': 'Invalid request body or missing content'}, status=400)
