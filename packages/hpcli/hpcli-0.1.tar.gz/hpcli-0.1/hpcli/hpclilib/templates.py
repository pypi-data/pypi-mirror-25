import os
from distutils.dir_util import copy_tree
from .common import MODULE_ROOT, big_print

TEMPLATE_ROOT_DIR = os.path.join(MODULE_ROOT, 'templates')


def copy_template(arguments, config):
    big_print('Copying template...')
    project_name = arguments['<project-name>']
    project_type = arguments['<template-type>']
    if project_name in os.listdir():
        raise RuntimeError(
            'Project %s already exists! Aborting template creation' %
            (project_name))
    template_dir = os.path.join(TEMPLATE_ROOT_DIR, project_type)
    copy_tree(template_dir, project_name)
