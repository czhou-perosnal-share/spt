


class Fields(object):
    def __init__(self,jira):
        self.jira = jira
        self.fields = self.jira.fields()
    
    def get_fields(self, field_names):
        fields = []
        for field in self.fields:
            if field['name'] in field_names:
                fields.append(field)
        return fields
    
    def get_field(self, field_name):
        for field in self.fields:
            if field['name'] == field_name:
                return field
        return None
    
    def get_field_type(self, field_name):
        field = self.get_field(field_name)
        if field:
            return field['schema']['type']
        return None
    
