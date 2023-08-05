import requests
import json

from django.http import HttpResponse


def validate_token(roles=None, scope=None):
    def outer_decorator(view_func):
        def wrapper(request, *args, **kwargs):
            payload = {}
            if type(roles) == list:
                str_roles = ','.join(roles)
            else:
                str_roles = roles

            if type(scope) == list:
                str_scope = ' '.join(scope)
            else:
                str_scope = scope

            payload.update({'accessToken': request.META.get("HTTP_ACCESS_TOKEN")})
            payload.update({'userId': 'null', 'clientID': 'null',
                            'ipAddress': '::1', 'requestURL': '/company/myprofile',
                            'requestedScopes': str_scope, 
                            'requestedRoles': str_roles,
                            'userAgent': request.META.get("HTTP_USER_AGENT")})

            headers = {'Content-Type': request.META.get("CONTENT_TYPE"),
                       'access_token': payload.get("accessToken")}

            resp = requests.post("https://dev.cidaas.de/token/userinfobytoken",
                                 data=json.dumps(payload), headers=headers,
                                 allow_redirects=False)
        
            if resp.status_code != 200:
                return HttpResponse(json.dumps(
                    {"error": "Access denied for this resource"}), status=401)
            else:
                return view_func(request, *args, **kwargs)
        return wrapper
    return outer_decorator
