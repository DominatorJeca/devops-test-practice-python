from django.db import connection
from django.http import JsonResponse

def liveness(request):
    """Pod saludable"""
    return JsonResponse({'status': 'ok'})

def readiness(request):
    try:
        with connection.cursor() as cursor:
            cursor.execute('SELECT 1')
    except Exception:
        return JsonResponse({'status': 'unavailable', 'database': 'down'}, status=503)
    return JsonResponse({'status': 'ready', 'database': 'up'})