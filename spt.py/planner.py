from epic import EPIC_HEAD, get_epic_options


def make_epics(jira, project, release_list, update = False):
    for key in release_list:
        release = jira.issue(key)
        print('Checking Release... Key:{}  Summary:{}'.format(release.key, release.fields.summary)) 
        make_single_epic(jira, project, release, update)
        print('') 

def make_single_epic(jira, project, release, update = False):
    no_child_epic = True
    
    epic_options = get_epic_options(project,release)
    
    for link in release.fields.issuelinks:
        if hasattr(link,'outwardIssue') and EPIC_HEAD in link.outwardIssue.fields.summary:
            no_child_epic = False 
            
            issue = link.outwardIssue
            print('Child Epic is existed. Key:{}  Summary:{}'.format(issue.key, issue.fields.summary))    
                     
            if update:
                print('Epic is updating... Key:{}  Summary:{}'.format(issue.key, issue.fields.summary))    
                update_child_epic(jira, issue.key, epic_options)

    if no_child_epic:
        create_child_epic(jira, release, epic_options)
        pass
    
def create_child_epic(jira, release, epic_options):   
    new_epic = jira.create_issue(fields = epic_options)
    jira.create_issue_link('is parent of', release, new_epic)
    
    print('Child Epic is created. Key:{}  Summary:{}'.format(new_epic.key, new_epic.fields.summary)) 

def update_child_epic(jira, key, epic_options):    
    epic = jira.issue(key)
    epic.update(fields = epic_options)
    
    print('Child Epic is updated. Key:{}  Summary:{}'.format(epic.key, epic.fields.summary))