from django.conf import settings
from django.db import connections
import vertica_python
import requests



def hc_services():

    meta_status = {}
    status = {}

    if hasattr(settings,'CLARITY_HEALTHCHECK_URLS'):
        dep_servies = settings.CLARITY_HEALTHCHECK_URLS

        for service in dep_servies.keys():

            service_url = dep_servies.get(service)

            try:
                r = requests.get(service_url)
                if r.status_code == 200:
                    status[service] = "up"
                else:
                    status[service] = "down"

            except:
                status[service] = "down"

        meta_status["Dependent Services"] = status

    return meta_status


def hc_datasources():
    status_list = []

    if hasattr(settings, 'DATABASES'):
        status_list.append(hc_sql_databases(settings.DATABASES))
    # status_list.append(hc_lens(settings.LENS_HC_URL))

    if hasattr(settings, 'VERTICA_CONNECTION_INFO'):
        status_list.append(hc_vertica(settings.VERTICA_CONNECTION_INFO))
    # status_list.append(hc_druid(settings.DRUID_HC_URL))

    meta_status = {}
    meta_status["Data Sources"] = status_list
    return meta_status


def hc_sql_databases(databases):
    status = {}
    for db in databases:
        try:
            connections[db].introspection.table_names()
            status[db] = "up"
        except:
            status[db] = "down"

    meta_status = {}
    meta_status["SQL DBS"] = status
    return meta_status



def hc_lens(lens_hc):
    status = {}
    try:
        r = requests.get(lens_hc)

        if r.status_code == 200 :
            status["LENS"] = "up"
        else:
            status["LENS"] = "down"

    except:
        status["LENS"] = "down"

    return status


def hc_vertica(conn_info):
    status={}
    try:
        conn_info = settings.VERTICA_CONNECTION_INFO
        connection = vertica_python.connect(**conn_info)
        cur = connection.cursor()
        cur.execute("select table_id from columns limit 1")
        result = cur.fetchall()
        connection.close()

        if len(result) == 1:
            status["Vertica"] = "up"
        else:
            status["Vertica"] = "down"

    except:
        status["Vertica"] = "down"

    return status

def hc_druid(druid_hc):
    status = {}
    try:
        r = requests.get(druid_hc)

        if r.status_code == 200:
            status["DRUID"] = "up"
        else:
            status["DRUID"] = "down"

    except:
        status["DRUID"] = "down"

    return status

