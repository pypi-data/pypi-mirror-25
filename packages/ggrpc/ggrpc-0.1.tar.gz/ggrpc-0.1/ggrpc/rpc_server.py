import json

from django.http import HttpResponse
from django.views import View


class RPCView(View):
    # TODO: for django only, can support other framework in the future
    def post(self, request, method):
        # TODO: add async / batch mode
        # A simple RPC implementation, may switch to gRPC in the future
        method = getattr(self, method)
        params = json.loads(request.POST.get('params'))
        result = method(*params['args'], **params['kwargs'])

        return HttpResponse(json.dumps(result))
