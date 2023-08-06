from django.db import connections
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.conf import settings

# Create your views here.
from ClarityHealthCheck.hc_utils import hc_datasources, hc_services


def check_status(request):

    status_list = []

    #Health status for dependent services
    status= hc_services()
    status_list.append(status)

    # Health status for datasources
    status = hc_datasources()
    status_list.append(status)

    return JsonResponse(status_list, safe=False)
