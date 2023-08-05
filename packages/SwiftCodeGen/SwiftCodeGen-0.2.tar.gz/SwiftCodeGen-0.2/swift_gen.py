__author__ = 'akhilraj'
import click
import json
import time
import os, glob
from mod_pbxproj import XcodeProject
from enum import Enum
from stemming.porter2 import stem
from dateutil.parser import parse
from urlparse import urlparse
from string import Template
from pathlib import Path
import sys
from models.project import Project
from helpers.code_generator import CodeGenerator
import urllib

@click.group()
def cli():
    pass

@click.command()
def init():
    path = os.getcwd()
    conf_path = "{}/SwiftGen".format(path)
    project_files = glob.glob("*.xcodeproj")
    name = ""
    if len(project_files) > 0:
        name = project_files[0][:-10]
    if not os.path.isdir(conf_path):
        os.makedirs(conf_path)
    os.chdir(conf_path)
    conf_file = urllib.URLopener()
    conf_file.retrieve("https://raw.githubusercontent.com/akhilraj-rajkumar/swift-code-gen/master/SwiftGen/SwiftGenConf.json", "SwiftGenConf.json")
    conf_file.retrieve("https://raw.githubusercontent.com/akhilraj-rajkumar/swift-code-gen/master/SwiftGen/TypeMap.json", "TypeMap.json")
    conf_file.retrieve("https://raw.githubusercontent.com/akhilraj-rajkumar/swift-code-gen/master/SwiftGen/ModelTemplate.swift", "ModelTemplate.swift")
    conf_file.retrieve("https://raw.githubusercontent.com/akhilraj-rajkumar/swift-code-gen/master/SwiftGen/ServiceTemplate.swift", "ServiceTemplate.swift")
    conf_dict = {}
    conf_dict["project_name"] = name
    conf_dict["project_path"] = os.path.relpath(path, conf_path)
    conf_dict["base_directory"] = "{}/{}".format(os.path.relpath(path, conf_path), name)
    conf_dict["class_prefix"] = ""
    apis = []
    user_api = {}
    user_api["endpoint"] = "some/path/getUser"
    user_api["api_name"] = "GetUser"
    user_api["method"] = "GET"
    user_api["request"] = ""
    user_response = {}
    user_response["first_name"] = "Akhilraj"
    user_response["last_name"] = "Rajkumar"
    user_response["sex"] = "M"
    user_response["age"] = "30"
    user_api["response"] = user_response
    apis.append(user_api)
    conf_dict["apis"] = apis
    conf_file_path = "{}/SwiftGenConf.json".format(conf_path)
    with open(conf_file_path, 'w') as outfile:
        json.dump(conf_dict, outfile)

@click.command()
@click.option('--config_dir', '-c', type=click.Path(exists=True))
def cache_clean(config_dir):
    '''To clean the cache, so the next time all code will be generated again.'''
    if config_dir is None or not os.path.isdir(os.path.abspath(config_dir)):
        click.echo('Config directory is not provided or invalid.')
        dir_path = os.getcwd()
        config_dir = dir_path + "/SwiftGen"
        click.echo('Checking default config directory at - {}'.format(config_dir))
    cache_file = config_dir + "/.cache"
    if os.path.isfile(cache_file):
        os.remove(cache_file)
        click.echo('Cache cleaned.')
    else:
        click.echo('Cache not found or already removed.')


@click.command()
@click.option('--config_dir', '-c', type=click.Path(exists=True))
@click.pass_context
def gen(ctx, config_dir):
    '''To generate model classes and api classes from config and template files'''
    project = ctx.invoke(validate, config_dir=config_dir)
    if project is None:
        click.echo('Failed!')
        return
    print project
    code_generator = CodeGenerator(project)
    code_generator.generate_code_for_project(project)
    click.echo('** Finished code generation **')

@click.command()
@click.option('--config_dir', '-c', type=click.Path(exists=True))
def validate(config_dir):
    '''To validate the SwiftGenConfig file'''
    conf_file_doc_path = " -coming soon- "
    template_doc_link = " -- coming soon -- "
    is_valid = True
    project = None
    # conf_file = Path("swift/SwiftGenConfig.json")
    if config_dir is None or not os.path.isdir(os.path.abspath(config_dir)):
        click.echo('Config directory is not provided or invalid.')
        dir_path = os.getcwd()
        config_dir = dir_path + "/SwiftGen"
        click.echo('Checking default config directory at - {}'.format(config_dir))
        if not os.path.isdir(os.path.abspath(config_dir)):
            click.echo('Require a config directory. Please read the documentation - {}'.format(template_doc_link))
            return project
    config_dir = os.path.abspath(config_dir)
    conf_file = config_dir + "/SwiftGenConf.json"

    if os.path.isfile(conf_file):
        os.chdir(config_dir)
        click.echo('Configuration file exists.')
        click.echo('Parsing configuration file for validation.')
        data = json.loads(open(conf_file).read())
        if 'project_path' not in data:
            raise ValueError("No value found for project_path key in configuration file. Please see the documentation of configuration file - {}".format(conf_file_doc_path))
        if 'apis' not in data:
            raise ValueError("No value found for apis key in configuration file. Please see the documentation of configuration file - {}".format(conf_file_doc_path))
        api_list = data['apis']
        project_path = os.path.abspath(data['project_path'])
        root_folder_directory = ''
        if 'base_directory' in data:
            root_folder_directory = os.path.abspath(data['base_directory'])
        project_name = ''
        if 'project_name' in data:
            project_name = data['project_name']
        class_prefix = ''
        if 'class_prefix' in data:
            class_prefix = data['class_prefix']
        project = Project(project_path, project_name, template_dir=config_dir, class_prefix=class_prefix, api_list=api_list, root_folder_directory=root_folder_directory)
        click.echo('---')
        is_valid = project.validate()
        if is_valid:
            click.echo(click.style('VALIDATION SUCCESS', fg='green', bold=True))
        click.echo('---')
    else:
        click.echo('Configuration file not found. There should be a SwiftGenConf.json file inside /SwiftGen directory or a path to configuration file directory should be provided for -config_dir argument. Please read the documentation - {}'.format(conf_file_doc_path))
    return project

cli.add_command(gen)
cli.add_command(validate)
cli.add_command(init)
cli.add_command(cache_clean)
