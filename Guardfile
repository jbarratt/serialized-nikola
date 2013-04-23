#!/usr/bin/env python
from livereload.task import Task
from livereload.compiler import shell

for path in ['conf.py', 'files/', 'galleries/', 'plugins/', 'posts/', 'stories/', 'themes/']:
    Task.add(path, shell('nikola build'))
