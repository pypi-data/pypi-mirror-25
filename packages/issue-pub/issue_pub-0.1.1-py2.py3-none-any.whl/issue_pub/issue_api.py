import requests

def List_issues(token, api_url):
    print "List issues"
    header = {"PRIVATE-TOKEN": token}
    print api_url
    req = requests.get(api_url, headers=header, verify=False)
    return req.text

def List_group_issues(token, api_url):
    print "List group issues"
    header = {"PRIVATE-TOKEN": token}
    req = requests.get(api_url, headers=header, verify=False)
    return req.text

def List_project_issues(token, api_url):
    header = {"PRIVATE-TOKEN": token}
    req = requests.get(api_url, headers=header, verify=False)
    return req.text

def Single_project_issue(token, api_url):
    header = {"PRIVATE-TOKEN": token}
    req = requests.get(api_url, headers=header, verify=False)
    return req.text

def New_issue():
    print "New_issue"
    

gitlab_host = "http://112.74.81.51:10088/"
private_token = 'W1GXs8KrxBF33zLrDEzq'

project_name = "test_sun"
project_id = 206

TOKEN = 'W1GXs8KrxBF33zLrDEzq'
# print List_issues(TOKEN, 'http://112.74.81.51:10088/api/v4/issues')
# print List_group_issues(TOKEN, 'http://112.74.81.51:10088/api/v4/groups/4/issues')
# print List_group_issues(TOKEN, 'http://112.74.81.51:10088/api/v4/projects/4/issues')
print List_group_issues(TOKEN, 'http://112.74.81.51:10088/api/v4/projects/4/issues/'+'1')