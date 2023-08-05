#!/usr/bin/python
# -*- coding: UTF-8 -*-

import time

def gen_file(path, title, project):
    time_prefix = time.strftime("%Y-%m-%d", time.localtime()) 
    file_name = time_prefix + " " + title + ".md"
    fp = open(path + "/" + file_name, "w")
    
    fp.write("#" + time_prefix + " TODO LISTS"+"\n\n")
    fp.write("## " + project + "\n\n")
    fp.write("- [ ] \n")
    fp.close

# gen_file("/home/sun/PycharmProjects/gitlab/", "test", "gitlab_api")