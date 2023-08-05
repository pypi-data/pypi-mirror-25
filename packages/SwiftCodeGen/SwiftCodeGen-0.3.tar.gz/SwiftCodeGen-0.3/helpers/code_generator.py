__author__ = 'akhilraj'
import json
import time
import os
from enum import Enum
from stemming.porter2 import stem
from string import Template
from dateutil.parser import parse
from urlparse import urlparse
from mod_pbxproj import XcodeProject
from models.project import Project
import string_utils
import click
import re


class ModelType(Enum):
    Model = 1,
    Response = 2,
    Request = 3

class CodeGenerator(object):
    """A Class for generating model and api classes in Swfit from its template classes."""
    def __init__(self, pjt):
        self.template_dir = pjt.template_dir
        self.project_name = str(pjt.project_name)
        self.project = pjt.get_pbx_project()
        self.base_group = pjt.get_pbx_base_group()
        self.root_folder_path = pjt.root_folder_directory
        self.class_prefix = pjt.class_prefix

    def generate_code_for_project(self, pjt):
        #iterate through each api's in provided list and geneate classes
        for api in pjt.api_list:
            self.generate_code_for_api_spec(api)

    def generate_code_for_api_spec(self, api_spec_json):
        model_name_aliases = {}
        if "model_alias" in api_spec_json:
            #checking if any alias names provided in the spec.
            #this is used for identifying same models with different name in spec json.
            #so the same model with different names will be mapped to one class.
            model_name_aliases = api_spec_json["model_alias"]
        api_name = api_spec_json["api_name"]
        response_sample = api_spec_json["response"]
        response_model_name = "{}{}Response".format(self.class_prefix, api_name)
        self.create_model_from_json(response_sample, response_model_name, model_alias=model_name_aliases, model_type=ModelType.Response)
        if "request" in api_spec_json:
            #checking for request params, GET requests may not have request params. So this is optional.
            request_sample = api_spec_json["request"]
            request_model_name = "{}{}Request".format(self.class_prefix, api_name)
            self.create_model_from_json(request_sample, request_model_name, model_alias=model_name_aliases, model_type=ModelType.Request)
        self._create_service_class(api_spec_json)


    def create_model_from_json(self, json_data, response_model_name, model_alias={}, create_file=True, model_type=ModelType.Model):
        #check the type of json_data, and create models
        if isinstance(json_data, dict):
            result = self._create_model_of_dict(json_data, response_model_name, model_alias=model_alias, model_type=model_type, create_file=create_file)
            return result
        elif isinstance(json_data, list):
            result = self._create_model_of_dict(json_data[0], response_model_name, model_alias=model_alias, model_type=model_type,
                                           create_file=create_file)
            return result
        else:
            return "Not dictionary"


    def _create_model_of_dict(self, dict_data, root_name, model_alias={}, model_type=ModelType.Model, create_file=True):
        with open("{}/TypeMap.json".format(self.template_dir)) as data_file:
            data_type_map = json.load(data_file)
            properties = list()
            maps = list()
            if model_type == ModelType.Response and "response" in model_alias:
                root_name = str(model_alias["response"])
            if model_type == ModelType.Request and "request" in model_alias:
                root_name = str(model_alias["request"])

            for key in dict_data:
                name = self.camel_case(key)
                if key in model_alias:
                    name = model_alias[key]
                    click.echo('Alias name found for model - {}, mapping to alias - {}'.format(key, name))
                value = dict_data[key]
                type_name = ""
                if isinstance(value, dict):
                    singular_name = stem(name)
                    singular_name = singular_name[:1].upper() + singular_name[1:]
                    singular_name = "{}".format(singular_name)
                    type_name = "{}{}".format(self.class_prefix, singular_name)
                    self._create_model_of_dict(value, "{}".format(type_name), model_alias=model_alias)
                elif isinstance(value, list):
                    singular_name = stem(name)
                    singular_name = singular_name[:1].upper() + singular_name[1:]
                    singular_name = "{}".format(singular_name)
                    type_name = "[{}{}]".format(self.class_prefix, singular_name)
                    self._create_model_of_dict(value[0], singular_name, model_alias=model_alias)
                else:
                    type_name = data_type_map[type(value).__name__]
                map_content = "{} <- map[\"{}\"]".format(name, key)
                # if type_name == "String" and self.is_date(value):
                #     type_name = "NSDate"
                #     map_content = "{} <- (map[\"{}\"], DateTransform())".format(name, key)
                property_content = "var {} : {}?".format(name, type_name)
                properties.append(property_content)
                maps.append(map_content)
            new_file_name = "{}.swift".format(root_name)
            if not new_file_name.startswith(self.class_prefix):
                new_file_name = "{}{}".format(self.class_prefix, new_file_name)
            properties, maps = self.check_model_in_cache(new_file_name, properties, maps)
            if len(properties) == 0:
                click.echo('No new properties found for class - {}'.format(new_file_name))
                return
            click.echo('Creating model class - {}'.format(new_file_name))
            file_in = open("{}/ModelTemplate.swift".format(self.template_dir))
            src = Template(file_in.read())
            file_in.close()
            d = {'file_name': "{}.swift".format(root_name), 'project_name': self.project_name, 'date': time.strftime("%d/%m/%Y"),
                 'class_name': root_name, 'properties': '\n\t'.join(properties), 'maps': '\n \t \t'.join(maps)}

            result = src.substitute(d)
            model_folder_name = "Models"
            model_dir_path = os.path.join(self.root_folder_path, model_folder_name)
            model_dir_f_path = os.path.join(self.project_name, model_folder_name)
            parent_group = self.base_group
            if model_type == ModelType.Response:
                parent_group = self.project.get_or_create_group(model_folder_name, None, self.base_group)
                model_folder_name = "Response"
                model_dir_path = os.path.join(model_dir_path, model_folder_name)
                model_dir_f_path = os.path.join(model_dir_f_path, model_folder_name)
            elif model_type == ModelType.Request:
                parent_group = self.project.get_or_create_group(model_folder_name, None, self.base_group)
                model_folder_name = "Request"
                model_dir_path = os.path.join(model_dir_path, model_folder_name)
                model_dir_f_path = os.path.join(model_dir_f_path, model_folder_name)

            if os.path.exists(model_dir_path):
                click.echo('Path exists for model - {}'.format(model_dir_path))
            else:
                click.echo('Creating folder reference at - {}'.format(model_dir_path))
                os.makedirs(model_dir_path)
            new_file_path = os.path.join(model_dir_path, new_file_name)
            file = open(new_file_path, 'a+w')
            file.seek(0)
            file.truncate()
            file.write(result)
            file.close()
            model_group = self.project.get_or_create_group(model_folder_name, None, parent_group)
            new_file_f_path = os.path.join(model_dir_f_path, new_file_name)
            self.project.add_file_if_doesnt_exist(f_path=new_file_f_path, parent=model_group)
            self.project.save()
            click.echo('Updated project with model.')
            return result


    def _create_service_class(self, api_spec_json):
        # _add_base_service_class()
        api_name = api_spec_json["api_name"]
        end_url = str(api_spec_json["endpoint"])
        parse_obj = urlparse(end_url)
        url_path = parse_obj.path
        path_components = url_path.split('/')
        url_vars = []
        endpoint = ""
        for component in path_components:
            if re.match(r"^\{[\S\s]*}$", component):
                url_vars.append(component[1:-1])
                endpoint += "/\({})".format(component[1:-1])
            else:
                endpoint += "/{}".format(component)
        url_var_params = ""
        for param in url_vars:
            url_var_params += "{}:String, ".format(param)
        request_method = ".{}".format((api_spec_json["method"]).lower())
        class_name = "{}{}Service".format(self.class_prefix, api_name)
        response_model_name = "{}{}Response".format(self.class_prefix, api_name)
        model_alias = {}
        if "model_alias" in api_spec_json:
            model_alias = api_spec_json["model_alias"]
        if "response" in model_alias:
            response_model_name = str(model_alias["response"])
        response_type = response_model_name
        map_type = "map(JSON: JSON as! [String : Any])"
        request_param = ""
        set_request_param = "nil"
        if isinstance(api_spec_json["response"], list):
            response_type = "[{}]".format(response_model_name)
            map_type = "mapArray(JSONArray: JSON as! [[String : Any]])"
        if isinstance(api_spec_json["request"], dict):
            request_model_name = "{}{}Request".format(self.class_prefix, api_name)
            if "request" in model_alias:
                request_model_name = str(model_alias["request"])
            request_param_name = self.camel_case(request_model_name)
            request_param = "{}: {},".format(request_param_name, request_model_name)
            set_request_param = "Mapper().toJSON({})".format(request_param_name)
        if isinstance(api_spec_json["request"], list):
            request_model_name = "{}{}Request".format(self.class_prefix, api_name)
            if "request" in model_alias:
                request_model_name = str(model_alias["request"])
            request_param_name = self.camel_case(request_model_name)
            request_param = "{}: [{}],".format(request_param_name, request_model_name)
            set_request_param = "Mapper().toJSONArray({})".format(request_param_name)
        if len(url_var_params) > 0:
            request_param = "{}{}".format(url_var_params, request_param)
        response_var_name = self.camel_case(response_model_name)
        method_name = str(self.camel_case(api_name))
        new_file_name = "{}.swift".format(class_name)
        d = {'file_name': new_file_name, 'project_name': self.project_name, 'date': time.strftime("%d/%m/%Y"),
             'class_name': class_name, 'response_type': response_type, 'method_name': method_name,
             'endpoint': endpoint, 'request_type': request_method, 'response_var': response_var_name,
             'response_model': response_model_name, 'map_type': map_type, 'request_var': request_param,
             'request_params': set_request_param}
        has_changes = self.check_service_class_in_cache_for_changes(new_file_name, d)
        if not has_changes:
            return
        click.echo('Creating web service class - {}.'.format(new_file_name))
        file_in = open("{}/ServiceTemplate.swift".format(self.template_dir))
        src = Template(file_in.read())
        file_in.close()
        result = src.substitute(d)
        new_folder_name = "Webservices"
        service_dir_path = os.path.join(self.root_folder_path, new_folder_name)
        if os.path.exists(service_dir_path):
            click.echo('Web service path exists - {}'.format(service_dir_path))
        else:
            os.makedirs(service_dir_path)
        new_file_path = os.path.join(service_dir_path, new_file_name)
        file = open(new_file_path, 'a+w')
        file.seek(0)
        file.truncate()
        file.write(result)
        file.close()
        service_group = self.project.get_or_create_group(new_folder_name, None, self.base_group)
        new_file_f_path = os.path.join(self.project_name, new_folder_name, new_file_name)
        self.project.add_file_if_doesnt_exist(f_path=new_file_f_path, parent=service_group)
        self.project.save()


    def _add_base_service_class(self):
        new_file_name = "{}.swift".format("BaseWebService")
        new_folder_name = "Webservices"
        service_dir_path = os.path.join(self.root_folder_path, new_folder_name)
        if os.path.exists(service_dir_path):
            print 'Path exists'
        else:
            os.makedirs(service_dir_path)
        new_file_path = os.path.join(service_dir_path, new_file_name)
        if os.path.isfile(new_file_path):
            print 'Base service file exists'
        else:
            file_in = open("swift/BaseServiceTemplate.swift")
            src = Template(file_in.read())
            file_in.close()
            d = {'file_name': new_file_name, 'project_name': "Test", 'date': time.strftime("%d/%m/%Y")}
            result = src.substitute(d)
            print result
            file = open(new_file_path, 'a+w')
            file.seek(0)
            file.truncate()
            file.write(result)
            file.close()
            service_group = self.project.get_or_create_group(new_folder_name, None, self.base_group)
            new_file_f_path = os.path.join(self.project_name, new_folder_name, new_file_name)
            self.project.add_file_if_doesnt_exist(f_path=new_file_f_path, parent=service_group)
            self.project.save()


    def camel_case(self, st):
        if string_utils.is_camel_case(st):
            return st[0].lower() + st[1:]
        elif string_utils.is_snake_case(st):
            output = string_utils.snake_case_to_camel(st, upper_case_first=False)
            return output
        else:
            output = ''.join(x for x in st.title() if x.isalpha())
            return output[0].lower() + output[1:]


    def is_date(self, string):
        try:
            parse(string)
            return True
        except ValueError:
            return False

    def get_cache_json(self):
        cache_content = None
        path = "{}/.cache".format(self.template_dir)
        if not os.path.isfile(path):
            file = open(path, 'a+w')
            file.close()
            data = {}
            cache_content = data

        else:
            if os.stat(path).st_size == 0:
                self.update_cache({})
            with open(path, 'r+') as data_file:
                cache_content = json.load(data_file)
        return cache_content

    def update_cache(self, cache_content):
        path = "{}/.cache".format(self.template_dir)
        with open(path, 'w') as outfile:
            json.dump(cache_content, outfile)

    def check_model_in_cache(self, name, properties, maps):
        cache_content = self.get_cache_json()
        final_props = []
        final_maps = []
        if name in cache_content:
            click.echo('model name : {} found in cache_content'.format(name))
            existing_class = cache_content[name]
            existing_props = existing_class["props"]
            existing_maps = existing_class["maps"]
            new_props = []
            new_maps = []
            for idx, val in enumerate(properties):
                match_found = False
                if any(val == prop for prop in existing_props):
                    match_found = True
                if not match_found:
                    new_props.append(val)
                    new_maps.append(maps[idx])
            if len(new_props) > 0:
                exis_prop_updated = [str(i) for i in existing_props]
                final_props.extend(exis_prop_updated)
                final_props.extend(new_props)
                exis_maps_updated = [str(i) for i in existing_maps]
                final_maps.extend(exis_maps_updated)
                final_maps.extend(new_maps)
                existing_class["props"] = final_props
                existing_class["maps"] = final_maps
                cache_content[name] = existing_class
                self.update_cache(cache_content)
        else:
            click.echo('new model file')
            final_props = properties
            final_maps = maps
            existing_class = {}
            existing_class["props"] = final_props
            existing_class["maps"] = final_maps
            cache_content[name] = existing_class
            self.update_cache(cache_content)
        return final_props, final_maps

    def check_service_class_in_cache_for_changes(self, name, service_dict):
        cache_content = self.get_cache_json()
        changes_found = False
        if name in cache_content:
            click.echo('service name : {} found in cache_content'.format(name))
            cache_service = cache_content[name]
            keys_to_comapre = ['response_type', 'method_name', 'endpoint', 'request_type', 'response_var',
             'response_model', 'map_type', 'request_var', 'request_params']
            for key in keys_to_comapre:
                if cache_service[key] != service_dict[key]:
                    changes_found = True
        else:
            click.echo('new service class')
            changes_found = True
        cache_content[name] = service_dict
        self.update_cache(cache_content)
        return changes_found
