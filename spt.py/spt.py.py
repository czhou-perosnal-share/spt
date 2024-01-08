# https://jira.readthedocs.io/

from jira import JIRA
import account
import planner


jiraOptions = {'server': account.server} 
jira = JIRA(options=jiraOptions, basic_auth=(account.user, account.token)) 

project = "SEAR"
release_list = ['RDSP-5041','RDSP-5032']

planner.make_epics(jira, project, release_list, update=True)



