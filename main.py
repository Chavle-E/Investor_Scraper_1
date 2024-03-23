import requests
from dataclasses import dataclass, asdict
from typing import Optional
import pandas as pd


@dataclass
class Investor:
    name: str
    website: str
    location: str
    Sector_Focus: str = None
    Current_Fund: str = None
    other_offices: Optional[list[str]] = None
    Type: list[str] = None
    Stage_Focus: list[str] = None


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


def get_hq_location_choices(data_arg):
    location_choices = {}
    city_name = {}
    for column in data_arg['data']['table']['columns']:
        if column['id'] == 'fld9SupEDjIjazlaA':
            location_choices = column['typeOptions']['choices']
            for loc_id, loc_info in location_choices.items():
                city_name[loc_id] = loc_info['name']
            break

    return city_name


def office_location_choices(data_arg):
    locations_choices = {}
    city_name = {}
    for column in data_arg['data']['table']['columns']:
        if column['id'] == 'fldNfzOQ6JtYjwu5P':
            locations_choices = column['typeOptions']['choices']
            for loc_id, loc_info in locations_choices.items():
                city_name[loc_id] = loc_info['name']
            break
    return city_name


def get_investor_type(data_arg):
    type_choices = {}
    types_def = {}
    for column in data_arg['data']['table']['columns']:
        if column['id'] == 'fldVhpJJoBVVtf1Xv':
            type_choices = column['typeOptions']['choices']
            for typeID, type_info in type_choices.items():
                types_def[typeID] = type_info['name']
            break
    return types_def


def get_stage_focus(data_arg):
    results = {}
    stage_focus_def = {}
    for column in data_arg['data']['table']['columns']:
        if column['id'] == 'fldbMm6H1J4mUxgwb':
            results = column['typeOptions']['choices']
            for StageFocID, StageFocInfo in results.items():
                stage_focus_def[StageFocID] = StageFocInfo['name']
            break
    return stage_focus_def


data = get_data()
names = []

rows = data['data']['table']['rows']
hq_locations_dict = get_hq_location_choices(data)
office_location_dict = office_location_choices(data)
type_id_dict = get_investor_type(data)
stage_focus_dict = get_stage_focus(data)

investors = []
for row in rows:
    # Get Cell Values
    cell_values = row.get('cellValuesByColumnId', {})
    # Get Name and Website
    name = cell_values.get('fldlT73kC6ZX8xm9U')
    website = cell_values.get('fldcAWLaMSTa8swPK')
    # Get Hq_location and Other offices
    hq_location_id = cell_values.get('fld9SupEDjIjazlaA')
    hq_location = hq_locations_dict.get(hq_location_id, 'None')

    offices = []
    office_location_ids = cell_values.get('fldNfzOQ6JtYjwu5P')
    if office_location_ids:
        for office_location_id in office_location_ids:
            offices.append(office_location_dict.get(office_location_id, 'None'))
    # Get types of investor
    types = []
    type_id = cell_values.get('fldVhpJJoBVVtf1Xv')
    if type_id:
        types.append(type_id_dict.get(type_id, 'None'))
    # Get Stage focuses of each Investor
    stage_focuses = []
    stage_focus_ids = cell_values.get('fldbMm6H1J4mUxgwb')
    if stage_focus_ids:
        for stage_focus_id in stage_focus_ids:
            stage_focuses.append(stage_focus_dict.get(stage_focus_id, 'None'))

    # Get Sector Focus
    sector_focus = cell_values.get('fldAodaUWkwpSTq4G')

    # Get Current Funding
    current_fund = cell_values.get('fldw5XW3xV0VzXP0j')
    # Get Year fund closed
    year_fund_closed = cell_values.get('fldZzIdZyZ380oWH2')
    # Create Investor dataclass and add it to
    Investor_item = Investor(name, website, hq_location, sector_focus, current_fund, offices, types, stage_focuses)
    investors.append(Investor_item)

investors_dicts = [asdict(investor) for investor in investors]

df = pd.DataFrame(investors_dicts)

df.to_csv('Investor.csv')
