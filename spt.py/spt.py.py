# https://jira.readthedocs.io/

from jira import JIRA
from conf import account
from core.EpicOptions import EpicOptions 
from core.Planner import Planner



    
def main():
    jiraOptions = {'server': account.server} 
    jira = JIRA(options=jiraOptions, basic_auth=(account.user, account.token)) 
    
    copy_epic_options(jira)
    #make_epics(jira)

 

def copy_epic_options(jira):
    options = EpicOptions(jira)
    fields = [
        'Target Release Season',
        'Strategic Area', 
        'Group Team', 
        'Scrum Team', 
        'Working Period(s)',
        'Start date',
        'End date'
        ]

    issue_opts = options.get_epic_options_from_issue('SEAR-10184', fields)

    jiraPlanner = Planner(jira)
    jiraPlanner.update_child_epic('SEAR-9197', issue_opts)
    


    
def make_epics(jira):
    project = "SEAR"
    release_list = ['RDSP-5311','RDSP-5306']

    jiraPlanner = Planner(jira)
    jiraPlanner.make_multiple_epics(project, release_list, update=False)

if __name__ == "__main__":
    main()


