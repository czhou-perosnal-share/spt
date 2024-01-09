# https://jira.readthedocs.io/

from jira import JIRA
import account
from lib.Planner import Planner


jiraOptions = {'server': account.server} 
jira = JIRA(options=jiraOptions, basic_auth=(account.user, account.token)) 

project = "SEAR"
release_list = ['RDSP-5041','RDSP-5032']

jiraPlanner = Planner(jira)

jiraPlanner.make_multiple_epics(project, release_list, update=False)




