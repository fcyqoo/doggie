from django.http import HttpResponse
from django.shortcuts import render_to_response, redirect
from django.views.decorators.csrf import csrf_exempt

VERSION = "1.0.1"


@csrf_exempt
def version_view(request):
    return HttpResponse(content=VERSION)


@csrf_exempt
def index_view(request):
    from mydoggie import settings_prod
    print(">>>>:", settings_prod.BASE_DIR, settings_prod.STATIC_ROOT)
    template_name = 'index.html'

    return render_to_response(template_name, dict())


@csrf_exempt
def silian(request):
    response = render_to_response('silian_doggiedoc.xml', dict())
    response['Content-Type'] = 'application/xml;'
    return response
