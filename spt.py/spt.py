# https://jira.readthedocs.io/

from genericpath import exists
from jira import JIRA
from conf import account
from core import Planner, EpicOptions, Fields
import argparse
import json


    
def main():
    args = arg_conf()

    jiraOptions = {'server': account.server} 
    jira = JIRA(options=jiraOptions, basic_auth=(account.user, account.token)) 

    if not exists('./data/options.json'):
       if args.command != 'options' or not args.imp:
        print('[Error] Cannot find options data !')
        print('Please run "spt options --import <key>" to import epic options first!')
        return


    if args.command == 'copy':
        copy_epic_options(jira, args.src, args.dest)
    elif args.command == 'make':
        make_epics(jira, args.project, args.release.split(','), args.update)
    elif args.command == 'fields':
        print(list_fields())
    elif args.command == 'options':
        if args.imp:
            options = read_epic_options(jira,args.imp)
            save_epic_options(options)
        elif args.pretty:
            options = load_epic_options()
            print(json.dumps(options, indent=4))
        elif args.list:
            options = load_epic_options()
            print(options)
        
        
            

def arg_conf():
    parser = argparse.ArgumentParser(description='Seismic Planning Tookit')
    sub_parser = parser.add_subparsers(dest='command')
    sub_parser.required = True
    
    make_parser = sub_parser.add_parser('make', help='make child epics')
    make_parser.add_argument('-r', '--release', help='release keys')
    make_parser.add_argument('-p', '--project', help='project key')
    make_parser.add_argument('-u', '--update', help='update existed epic', action='store_true')
    
    copy_parser = sub_parser.add_parser('copy', help='copy epic options')
    copy_parser.add_argument('-s', '--src', help='source issue key')
    copy_parser.add_argument('-d', '--dest', help='destination issue key')
    #copy_parser.add_argument('-f', '--fields', help='fields to copy')
    
    fields_parser = sub_parser.add_parser('fields', help='list all fields')
    
    options_parser = sub_parser.add_parser('options', help='list/import epic options')
    options_parser.add_argument('-i', '--import', dest='imp', help='import epic options by issue key')
    options_parser.add_argument('-l', '--list', help='list epic options', action='store_true')
    options_parser.add_argument('-p', '--pretty', help='pretty print', action='store_true')

    args = parser.parse_args()
    return args
    
def list_fields():
    file = open('./conf/fields.txt', 'r')
    fields = [line.strip() for line in file.readlines() if line.strip() != '']
    return fields

def load_epic_options():
    file = open('./data/options.json', 'r')
    options = json.load(file)
    return options

def save_epic_options(options):
    file = open('./data/options.json', 'w')
    json.dump(options, file, indent=4)
    file.close()
    print('Options are saved to {}'.format('./data/options.json')) 

def read_epic_options(jira, src):
    fields = list_fields()  
    src_issue = jira.issue(src)
    options = EpicOptions(jira)
    
    print('Retriving Source Info... Key:{}  Summary:{}'.format(src_issue.key, src_issue.fields.summary))  
    issue_opts = options.get_epic_options_from_issue(src_issue, fields)
    return issue_opts
    

def copy_epic_options(jira, src, dest):     
    issue_opts = load_epic_options(jira, src)
 
    jiraPlanner = Planner(jira)
    jiraPlanner.update_child_epic(dest, issue_opts)
    
    
def make_epics(jira, project, release_list, update):
    # project = "SEAR"
    # release_list = ['RDSP-5311','RDSP-5306']

    jiraPlanner = Planner(jira)
    jiraPlanner.make_multiple_epics(project, release_list, update)

    
if __name__ == "__main__":
   main()


