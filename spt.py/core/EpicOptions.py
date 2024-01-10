from core.Fields import Fields
import jira


class EpicOptions(object):    
    
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

            