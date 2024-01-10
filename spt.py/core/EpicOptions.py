from core.Fields import Fields
import jira


class EpicOptions(object):
    EPIC_HEAD = '[SPT]'
    DefaultEpicOptions = {
            'description': 'built from seismic planing tools',
            'issuetype': {'name': 'Epic'},
            'customfield_12394': {'id':'12486'},   # Strategy Area: 'ContentDiscovery'
            'customfield_12481': {'id':'12562'},   # GroupTeam: 'Search'
            'customfield_12395': {'id':'12244'},   # ScrumTeam: 'Search'        
            'customfield_12496': {'id':'14162'},   # TargetReleaseSeason: 'FY25Spring'
            'customfield_12491': [{'id':'12662'}], # WorkingPeriod: 'FY25Spring'
            'customfield_12492': {'id':'12699'},   # DeliveryType: 'Driving'
            'customfield_12127': '2024-02-01',     # StartDate: '2024-02-01'
            'customfield_12423': '2024-05-31',     # EndDate: '2024-05-31'
        }

    @staticmethod
    def get_epic_options(project, release):
        epic_options = {
            'project': {'key': project},
            'summary': EpicOptions.EPIC_HEAD + ' ' + release.fields.summary,
        }

        #copy default options
        for key in EpicOptions.DefaultEpicOptions:
            epic_options[key] = EpicOptions.DefaultEpicOptions[key]
        
        return epic_options   
    
    def __init__(self,jira):
        self.jira = jira
    
    def get_epic_options_from_issue(self, issue, display_names):
        epic_options = {}
        fields = Fields(self.jira)
        for name in display_names:
            field = fields.get_field(name)
            if field:
                fid = field['id']
                value = issue.fields.__dict__[fid]
                epic_options[fid] = self.__get_json_value(value)        
        return epic_options
    
    def __get_json_value(self, value):
        if isinstance(value,jira.resources.CustomFieldOption):
            return value.raw
        elif (     isinstance(value,list) 
               and len(value) > 0 
               and isinstance(value[0],jira.resources.CustomFieldOption)
             ):
            return [ v.raw for v in value ]
        else:
            return value

            