from core.EpicOptions import EpicOptions

class Planner(object):
    def __init__(self, jira):
        self.jira = jira
   

    def make_multiple_epics(self, project, release_list, update = False):
        for key in release_list:
            release = self.jira.issue(key)
            print('Checking Release... Key:{}  Summary:{}'.format(release.key, release.fields.summary)) 
            self.make_single_epic(project, release, update)
            print('') 


    def make_single_epic(self, project, release, update = False):
        
        epic_options = EpicOptions.get_epic_options(project,release)
    
        for link in release.fields.issuelinks:
            if hasattr(link,'outwardIssue') and EpicOptions.EPIC_HEAD in link.outwardIssue.fields.summary:
                issue = link.outwardIssue
                print('Child Epic is existed. Key:{}  Summary:{}'.format(issue.key, issue.fields.summary))    
                     
                if update:
                    print('Try to update Child Epic. Key:{}  Summary:{}'.format(issue.key, issue.fields.summary))    
                    self.update_child_epic(issue.key, epic_options)
                    return
                else:
                    return
                
        self.create_child_epic(release, epic_options)


    def create_child_epic(self, release, epic_options):   
        new_epic = self.jira.create_issue(fields = epic_options)
        self.jira.create_issue_link('is parent of', release, new_epic)
    
        print('Child Epic is created. Key:{}  Summary:{}'.format(new_epic.key, new_epic.fields.summary)) 

    def update_child_epic(self, key, epic_options):    
        epic = self.jira.issue(key)
        epic.update(fields = epic_options)
    
        print('Child Epic is updated. Key:{}  Summary:{}'.format(epic.key, epic.fields.summary))
    
    