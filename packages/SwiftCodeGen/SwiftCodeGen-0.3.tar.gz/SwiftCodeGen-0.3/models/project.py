__author__ = 'akhilraj'
from mod_pbxproj import XcodeProject
import click
import os, glob

class Project(object):
    """Class to keep properties of parsed project. """

    def __init__(self, project_path, project_name, api_list, template_dir, root_folder_directory="", class_prefix=""):
        super(Project, self).__init__()
        self.project_path = project_path
        self.project_name = project_name
        # if root_folder_directory == "":
        #     click.echo("Project base directory or root folder path is empty. Checking default path with project name.")
        #     click.echo(project_name)
        #     root_folder_directory = "{}/{}".format(project_path, project_name)
        #     click.echo(root_folder_directory)
        self.root_folder_directory = root_folder_directory
        self.class_prefix = class_prefix
        self.api_list = api_list
        self.template_dir = template_dir
        self.pbx_project = None

    def get_pbx_project(self):
        if self.pbx_project is None:
            project_file_path = '{}/{}.xcodeproj/project.pbxproj'.format(self.project_path, self.project_name)
            self.pbx_project = XcodeProject.Load(project_file_path)
        return self.pbx_project

    def get_pbx_base_group(self):
        if self.pbx_project is None:
            get_pbx_project()
        base_group = self.pbx_project.get_or_create_group(self.project_name)
        return base_group

    def validate(self):
        conf_file_doc_path = ' -- coming soon -- '
        template_doc_link = ' -- coming soon -- '
        try:
            click.echo('Checking project in directory : {}'.format(self.project_path))
            # ******checking project path*******
            if not os.path.isdir(self.project_path):
                raise ValueError('project_path is not a valid directory. Please see the documentation of configuration file - {}'.format(conf_file_doc_path))
            os.chdir(self.project_path)
            project_files = glob.glob("*.xcodeproj")
            if len(project_files) == 0:
                raise ValueError('No project file (.xcodeproj) found in directory provided - {}'.format(self.project_path))
            else:
                click.echo('Found project : {}'.format(project_files[0]))
                name = project_files[0][:-10]
                if len(self.project_name) == 0:
                    self.project_name = name
                if name != self.project_name:
                    click.echo('Project Name mismatch, using the value provided in configuration file - {}'.format(self.project_name))
                click.echo(name)
            # ******checking base directory*******
            if len(self.root_folder_directory) == 0:
                click.echo("Project base directory or root folder path is empty. Checking default path with project name.")
                self.root_folder_directory = "{}/{}".format(self.project_path, self.project_name)
            click.echo('Setting base directory as {}'.format(self.root_folder_directory))
            click.echo('Template directory : {}'.format(self.template_dir))
            is_model_template_exist = os.path.isfile('{}/ModelTemplate.swift'.format(self.template_dir))
            is_service_template_exist = os.path.isfile('{}/ServiceTemplate.swift'.format(self.template_dir))
            if not is_model_template_exist or not is_service_template_exist:
                raise ValueError('Not a valid template directory. Required template files not found. Please read he documentation on template files at - {}'.format(template_doc_link))
            return True

        except Exception as e:
            click.echo(click.style('Unexpected error on config file validation.', fg='red'))
            click.echo('Additional info : {}'.format(e))
            return False
