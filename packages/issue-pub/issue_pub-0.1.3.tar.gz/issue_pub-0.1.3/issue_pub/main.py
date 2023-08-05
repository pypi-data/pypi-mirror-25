import linecache
import gitlab

# todo init
filename = "/home/sun/PycharmProjects/gitlab_api/todo_md/2017-09-14 test.md"
line_len = len(open(filename,'rU').readlines())
todo_prefix = '- [ ]'

# git init
gitlab_host = "http://112.74.81.51:10088/"
private_token = 'W1GXs8KrxBF33zLrDEzq'
project_name = "gitlab_api"
project_id = 208
git = gitlab.Gitlab(gitlab_host, token=private_token)

for line in range(line_len):
    line_content = linecache.getline(filename, line)
    # print line_content
    if todo_prefix in line_content:
        line_content.replace(todo_prefix, ' ')
        print line_content[6:]
        git.createissue(project_id, line_content[6:])
    else:
        pass