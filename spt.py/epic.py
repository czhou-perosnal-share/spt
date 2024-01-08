EPIC_HEAD = '[SPT]'

def get_epic_options(project, release):
    epic_options = {
        'project': {'key': project},
        'summary': EPIC_HEAD + ' ' + release.fields.summary,
        'description': 'built from seismic planing tools',
        'issuetype': {'name': 'Epic'},
        'customfield_12394': {'id':'12486'},   # Strategy Area: 'ContentDiscovery'
        'customfield_12481': {'id':'12562'},   # GroupTeam: 'Search'
        'customfield_12395': {'id':'12244'},   # ScrumTeam: 'Search'        
        'customfield_12491': [{'id':'12662'}], # WorkingPeriod: 'FY25Spring'
        'customfield_12492': {'id':'12699'},   # DeliveryType: 'Driving'
        'customfield_12127': '2024-02-01',     # StartDate: '2024-05-31'
        'customfield_12423': '2024-05-31',     # EndDate: '2024-05-31'
    }
    return epic_options   