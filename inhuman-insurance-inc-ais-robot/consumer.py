import requests
from robocorp import workitems
from robocorp.tasks import task
@task
def consume_traffic_data():
    """
    Inhuman Insurance, Inc. Artificial Intelligence System automation.
    Consumes traffic data work items.
    """
    for item in workitems.inputs:
        traffic_data = item.payload["traffic_data"]
        if len(traffic_data["country"]) == 3:                        #verkürzte if-Abfrage!
            status, return_json = post_traffic_data_to_sales_system(traffic_data) #wenn ja, dann mach das hier
            if status == 200:                                        #prüfe das RESPONSE, ob es 200 ist
                item.done()                                          #wenn ja, ist das item done
            else:                                                    #bei einem anderen status, gehe hierhin    
                item.fail(                                           #item fällt durch
                    exception_type="APPLICATION",
                    code="TRAFFIC_DATA_POST_FAILED",
                    message=return_json["message"],
                )
        else:                                                       #wenn country_code länger/kürzer als 3 zeichen, dann fällt item durch
            item.fail(
                exception_type = "BUSINESS",
                code = "INVALID_TRAFFIC_DATA",
                message = item.payload,
            )

#def validate_traffic_data(traffic_data):
#    return len(traffic_data["country"]) == 3            #verkürzte if-Abfrage!

#    country = traffic_data["country"]                   #längere if-Abfrage
#    if len(country) == 3:
#        return True
#    else:
#        return False

def post_traffic_data_to_sales_system(traffic_data):
    url = "https://robocorp.com/inhuman-insurance-inc/sales-system-api"         #in der variablen wird diese url gespeichert
    response = requests.post(url, json = traffic_data)                           #"post" schickt die traffic_data an die angegebene url unter der variablen "json"
    return response.status_code, response.json()