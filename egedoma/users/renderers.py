import json
from rest_framework.renderers import JSONRenderer
import jwt
from django.conf import settings


class UserJSONRenderer(JSONRenderer):
    charset = 'utf-8'

    def render(self, data, media_type=None, renderer_context=None):
        hash = data.pop('hash', {})
        return json.dumps({
            'user': data,
            'hash': hash
        })