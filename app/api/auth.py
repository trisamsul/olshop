import json

from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse


@csrf_exempt
def auth_login(request):
    rtype = "/auth/login"
    status = False
    message = "Invalid credentials"
    data = []

    if request.method == 'POST':
        if request.body:
            payloads = json.loads(request.body)

            print(payloads)

    return JsonResponse({
        'rtype': rtype,
        'status': status,
        'message': message,
        'data': data,
    })
