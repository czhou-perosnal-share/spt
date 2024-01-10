# https://jira.readthedocs.io/

from re import S
from jira import JIRA
from conf import account
from core.EpicOptions import EpicOptions 
from core.Planner import Planner
import argparse


    
def main():
    args = arg_conf()

    jiraOptions = {'server': account.server} 
    jira = JIRA(options=jiraOptions, basic_auth=(account.user, account.token)) 

    if args.command == 'copy':
        copy_epic_options(jira, args.src, args.dest)
    elif args.command == 'make':
        make_epics(jira, args.project, args.release.split(','), args.update)

def arg_conf():
    parser = argparse.ArgumentParser(description='Seismic Planning Tookit')
    sub_parser = parser.add_subparsers(dest='command')
    sub_parser.required = True
    
    make_parser = sub_parser.add_parser('make', help='make epics')
    make_parser.add_argument('-r', '--release', help='release keys')
    make_parser.add_argument('-p', '--project', help='project key')
    make_parser.add_argument('-u', '--update', help='update existed epic', action='store_true')
    
    copy_parser = sub_parser.add_parser('copy', help='copy epic options')
    copy_parser.add_argument('-s', '--src', help='source issue key')
    copy_parser.add_argument('-d', '--dest', help='destination issue key')
    #copy_parser.add_argument('-f', '--fields', help='fields to copy')
    
    args = parser.parse_args()
    return args
    
 

def copy_epic_options(jira, src, dest):
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

    src_issue = jira.issue(src)
    print('Retriving Source Info... Key:{}  Summary:{}'.format(src_issue.key, src_issue.fields.summary))    
    issue_opts = options.get_epic_options_from_issue(src_issue, fields)
    jiraPlanner = Planner(jira)
    jiraPlanner.update_child_epic(dest, issue_opts)
    


    
def make_epics(jira, project, release_list, update):
    # project = "SEAR"
    # release_list = ['RDSP-5311','RDSP-5306']

    jiraPlanner = Planner(jira)
    jiraPlanner.make_multiple_epics(project, release_list, update)

    
if __name__ == "__main__":
   main()


