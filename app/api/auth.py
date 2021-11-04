import json

from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.contrib.auth import authenticate, logout
from rest_framework.decorators import api_view

from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token


@csrf_exempt
def auth_login(request):
    rtype = "/auth/login"
    status = False
    message = "Invalid credentials"
    data = []

    if request.method == 'POST':
        if request.body:
            payloads = json.loads(request.body)

            if 'username' in payloads and 'password' in payloads and payloads['username'] and payloads['password']:
                username = payloads['username']
                user = authenticate(username=username, password=payloads['password'])

                if user:
                    token = Token.objects.filter(user=user).first()

                    if not token:
                        token = Token.objects.create(user=user)

                    status = True
                    message = "Login successfully"
                    data = {
                        'username': user.username,
                        'email': user.email,
                        'token': token.key,
                    }
                else:
                    message = "Invalid credentials"
            else:
                return JsonResponse({
                    'type': '/auth/login',
                    'status': False,
                    'message': 'Credentials not provided',
                    'data': [],
                })
        else:
            message = "Empty parameters"
    else:
        message = "Method not allowed"

    return JsonResponse({
        'rtype': rtype,
        'status': status,
        'message': message,
        'data': data,
    })


@api_view(['GET'])
def auth_logout(request):
    token = Token.objects.filter(user=request.user).first()
    if token:
        token.delete()

    logout(request)

    return JsonResponse({
        'type': '/auth/logout',
        'status': True,
        'message': 'Logged out',
    })
