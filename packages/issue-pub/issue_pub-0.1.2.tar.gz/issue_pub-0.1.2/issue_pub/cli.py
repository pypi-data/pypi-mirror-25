# -*- coding: utf-8 -*-
import sys, getopt
import os
import linecache
import gitlab
import yaml
"""Console script for issue_pub."""

import click


opts, args = getopt.getopt(sys.argv[1:], "hi:o:")
print opts, args

filename = args[0]

print filename
line_len = len(open(filename,'rU').readlines())
todo_prefix = '- [ ]'

print os.environ['HOME']


# git init
fy = open(os.environ['HOME']+"/.gitlab_pub.yaml")
gitlab_yaml = yaml.load(fy)
print gitlab_yaml
gitlab_host = gitlab_yaml['url']
private_token = gitlab_yaml['token']
project_name = gitlab_yaml['project']
project_id = gitlab_yaml['project_id']

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


