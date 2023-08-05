import requests
import json
import os

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
                            'ipAddress': '::1',
                            'requestURL': request.get_full_path(),
                            'requestedScopes': str_scope, 
                            'requestedRoles': str_roles,
                            'userAgent': request.META.get("HTTP_USER_AGENT")})

            headers = {'Content-Type': request.META.get("CONTENT_TYPE"),
                       'access_token': payload.get("accessToken")}

            try:
                settings_data = json.loads(open(os.environ['URL_INFO']).read())
                url = settings_data['user_info_by_token']
            except Exception as ex:
                return HttpResponse(json.dumps(
                    {"error": ex.message}))

            resp = requests.post(url, data=json.dumps(payload), headers=headers,
                                 allow_redirects=False)
        
            if resp.status_code != 200:
                return HttpResponse(json.dumps(
                    {"error": "Access denied for this resource"}), status=401)
            else:
                return view_func(request, *args, **kwargs)
        return wrapper
    return outer_decorator


# Will permit for all the request even if there is no access_token
def permit_all(view_func):
    def wrapper(request, *args, **kwargs):
        return view_func(request, *args, **kwargs)
    return wrapper


# deny for all the requests
def deny_all(view_func):
    def wrapper(request, *args, **kwargs):
        return HttpResponse(json.dumps(
            {"error": "Access denied for this resource"}), status=401)
    return wrapper

