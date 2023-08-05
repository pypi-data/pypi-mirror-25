# coding: utf-8

"""
OrganizationApi.py
Copyright 2016 SmartBear Software

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.
"""

from __future__ import absolute_import

import sys
import os
import re

# python 2 and python 3 compatibility library
from six import iteritems

from ..configuration import Configuration
from ..api_client import ApiClient


class OrganizationApi(object):
    """
    NOTE: This class is auto generated by the swagger code generator program.
    Do not edit the class manually.
    Ref: https://github.com/swagger-api/swagger-codegen
    """

    def __init__(self, api_client=None):
        config = Configuration()
        if api_client:
            self.api_client = api_client
        else:
            if not config.api_client:
                config.api_client = ApiClient()
            self.api_client = config.api_client

    def get_fieldconfig(self, type, **kwargs):
        """
        Fetch field config for an entity type
        

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please define a `callback` function
        to be invoked when receiving the response.
        >>> def callback_function(response):
        >>>     pprint(response)
        >>>
        >>> thread = api.get_fieldconfig(type, callback=callback_function)

        :param callback function: The callback function
            for asynchronous request. (optional)
        :param str type: Field type (required)
        :return: FieldConfig
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['type']
        all_params.append('callback')

        params = locals()
        for key, val in iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method get_fieldconfig" % key
                )
            params[key] = val
        del params['kwargs']

        # verify the required parameter 'type' is set
        if ('type' not in params) or (params['type'] is None):
            raise ValueError("Missing the required parameter `type` when calling `get_fieldconfig`")


        resource_path = '/api/v2/fieldconfig'.replace('{format}', 'json')
        path_params = {}

        query_params = {}
        if 'type' in params:
            query_params['type'] = params['type']

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None

        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.\
            select_header_accept(['application/json'])
        if not header_params['Accept']:
            del header_params['Accept']

        # HTTP header `Content-Type`
        header_params['Content-Type'] = self.api_client.\
            select_header_content_type(['application/json'])

        # Authentication setting
        auth_settings = ['PureCloud Auth']

        response = self.api_client.call_api(resource_path, 'GET',
                                            path_params,
                                            query_params,
                                            header_params,
                                            body=body_params,
                                            post_params=form_params,
                                            files=local_var_files,
                                            response_type='FieldConfig',
                                            auth_settings=auth_settings,
                                            callback=params.get('callback'))
        return response

    def get_organizations_me(self, **kwargs):
        """
        Get organization.
        

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please define a `callback` function
        to be invoked when receiving the response.
        >>> def callback_function(response):
        >>>     pprint(response)
        >>>
        >>> thread = api.get_organizations_me(callback=callback_function)

        :param callback function: The callback function
            for asynchronous request. (optional)
        :return: Organization
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = []
        all_params.append('callback')

        params = locals()
        for key, val in iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method get_organizations_me" % key
                )
            params[key] = val
        del params['kwargs']



        resource_path = '/api/v2/organizations/me'.replace('{format}', 'json')
        path_params = {}

        query_params = {}

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None

        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.\
            select_header_accept(['application/json'])
        if not header_params['Accept']:
            del header_params['Accept']

        # HTTP header `Content-Type`
        header_params['Content-Type'] = self.api_client.\
            select_header_content_type(['application/json'])

        # Authentication setting
        auth_settings = ['PureCloud Auth']

        response = self.api_client.call_api(resource_path, 'GET',
                                            path_params,
                                            query_params,
                                            header_params,
                                            body=body_params,
                                            post_params=form_params,
                                            files=local_var_files,
                                            response_type='Organization',
                                            auth_settings=auth_settings,
                                            callback=params.get('callback'))
        return response

    def patch_organizations_feature(self, feature_name, enabled, **kwargs):
        """
        Update organization
        

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please define a `callback` function
        to be invoked when receiving the response.
        >>> def callback_function(response):
        >>>     pprint(response)
        >>>
        >>> thread = api.patch_organizations_feature(feature_name, enabled, callback=callback_function)

        :param callback function: The callback function
            for asynchronous request. (optional)
        :param str feature_name: Organization feature (required)
        :param FeatureState enabled: New state of feature (required)
        :return: OrganizationFeatures
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['feature_name', 'enabled']
        all_params.append('callback')

        params = locals()
        for key, val in iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method patch_organizations_feature" % key
                )
            params[key] = val
        del params['kwargs']

        # verify the required parameter 'feature_name' is set
        if ('feature_name' not in params) or (params['feature_name'] is None):
            raise ValueError("Missing the required parameter `feature_name` when calling `patch_organizations_feature`")
        # verify the required parameter 'enabled' is set
        if ('enabled' not in params) or (params['enabled'] is None):
            raise ValueError("Missing the required parameter `enabled` when calling `patch_organizations_feature`")


        resource_path = '/api/v2/organizations/features/{featureName}'.replace('{format}', 'json')
        path_params = {}
        if 'feature_name' in params:
            path_params['featureName'] = params['feature_name']

        query_params = {}

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        if 'enabled' in params:
            body_params = params['enabled']

        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.\
            select_header_accept(['application/json'])
        if not header_params['Accept']:
            del header_params['Accept']

        # HTTP header `Content-Type`
        header_params['Content-Type'] = self.api_client.\
            select_header_content_type(['application/json'])

        # Authentication setting
        auth_settings = ['PureCloud Auth']

        response = self.api_client.call_api(resource_path, 'PATCH',
                                            path_params,
                                            query_params,
                                            header_params,
                                            body=body_params,
                                            post_params=form_params,
                                            files=local_var_files,
                                            response_type='OrganizationFeatures',
                                            auth_settings=auth_settings,
                                            callback=params.get('callback'))
        return response

    def put_organizations_me(self, **kwargs):
        """
        Update organization.
        

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please define a `callback` function
        to be invoked when receiving the response.
        >>> def callback_function(response):
        >>>     pprint(response)
        >>>
        >>> thread = api.put_organizations_me(callback=callback_function)

        :param callback function: The callback function
            for asynchronous request. (optional)
        :param Organization body: Organization
        :return: Organization
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['body']
        all_params.append('callback')

        params = locals()
        for key, val in iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method put_organizations_me" % key
                )
            params[key] = val
        del params['kwargs']



        resource_path = '/api/v2/organizations/me'.replace('{format}', 'json')
        path_params = {}

        query_params = {}

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        if 'body' in params:
            body_params = params['body']

        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.\
            select_header_accept(['application/json'])
        if not header_params['Accept']:
            del header_params['Accept']

        # HTTP header `Content-Type`
        header_params['Content-Type'] = self.api_client.\
            select_header_content_type(['application/json'])

        # Authentication setting
        auth_settings = ['PureCloud Auth']

        response = self.api_client.call_api(resource_path, 'PUT',
                                            path_params,
                                            query_params,
                                            header_params,
                                            body=body_params,
                                            post_params=form_params,
                                            files=local_var_files,
                                            response_type='Organization',
                                            auth_settings=auth_settings,
                                            callback=params.get('callback'))
        return response
