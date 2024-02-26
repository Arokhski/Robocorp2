from robocorp.tasks import task
from robocorp import workitems
from RPA.HTTP import HTTP
from RPA.JSON import JSON
from RPA.Tables import Tables

http = HTTP()
json = JSON()
table = Tables()

TRAFFIC_JSON_FILE_PATH = "output/traffic.json"

# JSON data keys
COUNTRY_KEY = "SpatialDim"
YEAR_KEY = "TimeDim"
RATE_KEY = "NumericValue"
GENDER_KEY = "Dim1"

@task
def produce_traffic_data():
    """
    Inhuman Insurance, Inc. Artificial Intelligence System automation.
    Produces traffic data work items.
    """
    http.download(
        url="https://github.com/robocorp/inhuman-insurance-inc/raw/main/RS_198.json",
        target_file=TRAFFIC_JSON_FILE_PATH,
        overwrite=True,
    )
    traffic_data = load_traffic_data_as_table()
    filtered_data = filter_and_sort_traffic_data(traffic_data)  #erzeugt gefilterte Daten aus der Tabelle
    filtered_data = get_latest_data_by_country(filtered_data)   #nutzt die gefiltrerten Daten in einer neuen Funktion
    payloads = create_work_item_payloads(filtered_data)         #nutzt die ERNEUT gefilterten daten (zweite variable)
    save_work_item_payloads(payloads)

def load_traffic_data_as_table():
    json_data = json.load_json_from_file(TRAFFIC_JSON_FILE_PATH)
    return table.create_table(json_data["value"])

def filter_and_sort_traffic_data(data):
    max_rate = 5.0
    both_genders = "BTSX"
    table.filter_table_by_column(data, RATE_KEY, "<", max_rate)
    table.filter_table_by_column(data, GENDER_KEY, "==", both_genders)
    table.sort_table_by_column(data, YEAR_KEY, False)
    return data

def get_latest_data_by_country(data):
    data = table.group_table_by_column(data, COUNTRY_KEY)   #tabelle wird nach der spalte "SpatialDim" geordnet
    latest_data_by_country = []                             #generiert noch leere variable
    for group in data:
        first_row = table.get_table_row(group, 0)           #entfernt erste spalte aus "data" aus, das zuvor nach SpatialDim sortiert wurde
        latest_data_by_country.append(first_row)            #fügt diese daten der variablen hinzu (append)
    return latest_data_by_country                           #ende der funktion, inhalt der variablen steht zur nutzung bereit

def create_work_item_payloads(traffic_data):
    payloads = []                                           #leere Variable
    for row in traffic_data:
        payload = dict(                                     #dict-Funktion (dictionary, jede Row ist ein neues dict) wird in Variable payload gespeichert
            country = row[COUNTRY_KEY],                    #dictionary namens "country" enthaelt die zeile SpatialDim komplett
            year = row[YEAR_KEY],                           #...
            rate = row[RATE_KEY]        
        )
        payloads.append(payload)                            #Variable payloads erhält den inhalt von payload aus jedem durchlauf (hintenangehängt)
    return payloads

def save_work_item_payloads(payloads):
    for payload in payloads:
        variables = dict(traffic_data = payload)
        workitems.outputs.create(variables)