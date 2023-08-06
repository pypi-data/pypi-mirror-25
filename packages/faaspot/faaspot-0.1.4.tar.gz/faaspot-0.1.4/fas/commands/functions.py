#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import six
import json
import string
import logging
import pkg_resources

from six.moves.urllib.parse import quote, unquote

from .command import Command
from ..utils import WaitCompletion

logger = logging.getLogger(__name__)


class Functions(Command):
    def __init__(self, *args, **kwargs):
        super(Functions, self).__init__(*args, **kwargs)

    def list(self):
        self.columns = ['name', 'runner_url']
        uri = 'functions/'
        all = self.api.get(uri=uri)
        return all

    @WaitCompletion(logger=logger)
    def create(self, name, file, context_file=None, **kwargs):
        self._validate_function_name(name)
        logger.debug('Going to create deployment: {0}'.format(name))
        uri = 'functions/'
        query_params = None
        encoded_file_content = self._encode_content(file)
        context_file_content = self._encode_content(context_file)
        data = {"code": encoded_file_content,
                "name": name,
                "context": context_file_content}
        task_id = self.api.put(uri, params=query_params, data=data, expected_status_code=200)
        return "Execution id: {0}".format(task_id) if self._is_execution_id(task_id) else task_id

    @WaitCompletion(logger=logger)
    def update(self, name, file=None, context_file=None, new_name=None, **kwargs):
        self._validate_function_name(name)
        logger.debug('Going to update deployment: {0}'.format(name))
        if not (file or context_file or new_name):
            raise Exception('No action requested.')
        uri = 'functions/{0}'.format(name)
        query_params = None
        file_content = self._encode_content(file)
        context_file_content = self._encode_content(context_file)
        data = {}
        if file_content:
            data['code'] = file_content
        if context_file_content:
            data['context'] = context_file_content
        if new_name:
            data['name'] = new_name
        response = self.api.patch(uri, params=query_params, data=data, expected_status_code=200)
        return response

    def get(self, name, pretty_print=False):
        logger.debug('Going to retrieve deployment: {0}'.format(name))
        uri = 'functions/{0}'.format(name)
        response = self.api.get(uri=uri)
        code = response.get('code')
        response['code'] = unquote(code)
        if not pretty_print:
            return response
        result = ''
        code = response.pop('code')
        for k, v in response.items():
            result += '{:15s}| {}\n'.format(k, v)
        result += 'code:\n{0}'.format(code)
        return result

    @WaitCompletion(logger=logger)
    def delete(self, name, **kwargs):
        logger.debug('Going to delete deployment: {0}'.format(name))
        uri = 'functions/{0}'.format(name)
        response = self.api.delete(uri=uri)
        return response

    def run(self, name, parameters=None, **kwargs):
        """
        :param name:
        :param parameters: the input for the function.
            can be dict of {key: value}
            can be a list of [["key=value"], ["key=value"]]
        """
        logger.debug('Going to run `{0}`'.format(name))
        uri = 'functions/{0}/rpc/'.format(name)
        if isinstance(parameters, dict):
            data = parameters
        elif isinstance(parameters, list):
            data = self._str_parameters_to_obj(parameters)[0]
        else:
            data = None
        logger.debug('Going to run `{0}` with parameter: {1}'.format(name, data))
        wait = kwargs.get('wait', False)
        if wait:
            uri = 'sync/functions/{0}/rpc/'.format(name)
            return self.api.get(uri=uri, params=data)
        task_id = self.api.post(uri=uri, data=data)
        return task_id

    def run_bulk(self, name, parameters=None, **kwargs):
        """
        :param name:
        :param parameters: the input for the function.
            can be dict list of dicts [{key: value}, {key: value}]
            can be a list of [["key=value", ], ["key=value"]]
        """
        logger.debug('Goring to bulk run of `{0}`'.format(name))
        uri = 'functions/{0}/bulk_rpc/'.format(name)
        if not isinstance(parameters, list) or len(parameters) == 0:
            raise Exception('Missing require list of group-of-parameters..')
        if not isinstance(parameters[0], dict):
            parameters = self._str_bulk_parameters_to_obj(parameters)
        data = json.dumps(parameters)
        task_id = self.api.post(uri=uri, data=data)
        return task_id

    def samples(self, hello_world=False, get_content=False, sleep=False):
        if not (hello_world or get_content or sleep):
            raise Exception('No action requested, need to select some sample..')
        name = ''
        if hello_world:
            name = 'hello-world.py'
        elif get_content:
            name = 'get-content.py'
        elif sleep:
            name = 'sleep.py'
        if os.path.isfile(name):
            return 'File with name `{0}` already exists.'.format(name)
        logger.debug('Going to create a sample file: `{0}`'.format(name))
        resource_package = __name__
        resource_path = '/'.join(('samples', name))
        sample = pkg_resources.resource_stream(resource_package, resource_path)
        content = sample.read()
        with open(name, 'w') as sample_file:
            sample_file.write(content)
        return "Sample file `{0}` been created.".format(name)

    @staticmethod
    def _validate_function_name(name):
        """
        Raise exception if the input name is not a valid function name.
        """
        allowed_characters = set(
            string.ascii_letters +
            string.digits +
            '-_.'
        )
        invalid_characters = list(filter(lambda x: x not in allowed_characters, name))
        if invalid_characters:
            raise Exception('Invalid name: `{0}`. Allowed only letters and numbers'.format(name))
        _, file_extension = os.path.splitext(name)
        if not file_extension or file_extension not in {'.py'}:
            raise Exception('Invalid name: `{0}`. Missing a valid extension [".py"]'.format(name))

    def _str_parameters_to_obj(self, parameters):
        """
        convert:  [['k1=v1, k2=v2'], ['k1=v1, k2=v2']]
        to: [ {'k1': 'v1', 'k2': 'v2'}, {'k1': 'v1', 'k2': 'v2'} ]
        """
        args_dict = {}
        for param in parameters:
            arg, value = param[0].split('=', 1)
            args_dict[arg.strip()] = value.strip()
        return [args_dict]

    def _str_bulk_parameters_to_obj(self, parameters):
        """
        convert:  [['k1=v1, k2=v2'], ['k1=v1, k2=v2']]
        to: [ {'k1': 'v1', 'k2': 'v2'}, {'k1': 'v1', 'k2': 'v2'} ]
        """
        result = []
        for params_set in parameters:
            args_dict = {}
            params = params_set[0].strip(' ,').split(',')
            for param in params:
                arg, value = param.split('=')
                args_dict[arg.strip()] = value.strip()
            result.append(args_dict)
        return result

    def _bulk_run(self, name, parameters_list):
        uri = 'functions/{0}/bulk_rpc/'.format(name)
        task_id = self.api.post(uri=uri,
                                data={'values': json.dumps(parameters_list)})
        return task_id

    @staticmethod
    def _encode_content(data):
        """
        Encode content into utf-8
        """
        if not data:
            return ''
        if isinstance(data, six.string_types):
            if not os.path.isfile(data):
                raise Exception('Missing file in path: {0}'.format(data))
            with open(data, "r") as input_file:
                content = input_file.read()
        else:
            content = data.read()
        if sys.version_info[0] == 2:
            content = content.encode('utf-8')
        return quote(content)

    @staticmethod
    def _is_execution_id(text):
        """
        Verify that input is a valid Faaspot execution_id
        """
        return len(text) == 36 and len(text.split('-')) == 5
