import requests
from dataclasses import dataclass
from typing import Optional


@dataclass
class Investor:
    name: str
    website: str
    location: str
    other_offices: Optional[list[str]] = None


def get_data():
    url = "https://airtable.com/v0.3/view/viwfsO8ZANVPNwMWB/readSharedViewData"

    querystring = {"stringifiedObjectParams": "{\"shouldUseNestedResponseFormat\":true}",
                   "requestId": "reqlaapQ2H0Taz08I",
                   "accessPolicy": "{\"allowedActions\":[{\"modelClassName\":\"view\",\"modelIdSelector\":\"viwfsO8ZANVPNwMWB\",\"action\":\"readSharedViewData\"},{\"modelClassName\":\"view\",\"modelIdSelector\":\"viwfsO8ZANVPNwMWB\",\"action\":\"getMetadataForPrinting\"},{\"modelClassName\":\"view\",\"modelIdSelector\":\"viwfsO8ZANVPNwMWB\",\"action\":\"readSignedAttachmentUrls\"},{\"modelClassName\":\"row\",\"modelIdSelector\":\"rows *[displayedInView=viwfsO8ZANVPNwMWB]\",\"action\":\"createDocumentPreviewSession\"}],\"shareId\":\"shrSHRMum8oJmDjFJ\",\"applicationId\":\"apph9tTMHZwV2BwWX\",\"generationNumber\":0,\"expires\":\"2024-04-11T00:00:00.000Z\",\"signature\":\"15c53f9ec4b1e01cf7fd24bf80701aef1512e8e680df4d1b47e3a7bf1409cd84\"}"}

    headers = {
        'Content-Type': "application/json",
        'authority': "airtable.com",
        'accept-language': "en-GB,en;q=0.9,ka-GE;q=0.8,ka;q=0.7,en-US;q=0.6",
        'user-agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
        'x-airtable-accept-msgpack': "true",
        'x-airtable-application-id': "apph9tTMHZwV2BwWX",
        'x-airtable-inter-service-client': "webClient",
        'x-airtable-page-load-id': "pglhP7LmbFq97SrLX",
        'x-early-prefetch': "true",
        'x-requested-with': "XMLHttpRequest",
        'x-time-zone': "Asia/Tbilisi",
        'x-user-locale': "en"
    }

    response = requests.request("GET", url, headers=headers, params=querystring)

    result = response.json()
    return result


def get_location_choices(data_arg):
    location_choices = {}
    city_name = {}
    for column in data_arg['data']['table']['columns']:
        if column['id'] == 'fld9SupEDjIjazlaA':
            location_choices = column['typeOptions']['choices']
            for loc_id, loc_info in location_choices.items():
                city_name[loc_id] = loc_info['name']
            break

    return city_name


data = get_data()

names = []
rows = data['data']['table']['rows']
locations_dict = get_location_choices(data)
investors = []
for row in rows:
    # Get Cell Values
    cell_values = row.get('cellValuesByColumnId', {})
    # Get Name and Website
    name = cell_values.get('fldlT73kC6ZX8xm9U')
    website = cell_values.get('fldcAWLaMSTa8swPK')
    # Get Hq_location and Other offices
    hq_location_id = cell_values.get('fld9SupEDjIjazlaA')
    hq_location = locations_dict.get(hq_location_id, 'None')

    # Create Investor dataclass and add it to
    Investor_item = Investor(name, website, hq_location)
    investors.append(Investor_item)

print(investors)
