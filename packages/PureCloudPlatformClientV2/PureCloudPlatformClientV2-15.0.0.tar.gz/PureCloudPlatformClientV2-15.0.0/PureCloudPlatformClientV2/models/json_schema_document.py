# coding: utf-8

"""
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

    Ref: https://github.com/swagger-api/swagger-codegen
"""

from pprint import pformat
from six import iteritems
import re


class JsonSchemaDocument(object):
    """
    NOTE: This class is auto generated by the swagger code generator program.
    Do not edit the class manually.
    """
    def __init__(self):
        """
        JsonSchemaDocument - a model defined in Swagger

        :param dict swaggerTypes: The key is attribute name
                                  and the value is attribute type.
        :param dict attributeMap: The key is attribute name
                                  and the value is json key in definition.
        """
        self.swagger_types = {
            'id': 'str',
            'schema': 'str',
            'title': 'str',
            'description': 'str',
            'type': 'str',
            'required': 'list[str]',
            'properties': 'dict(str, object)'
        }

        self.attribute_map = {
            'id': 'id',
            'schema': '$schema',
            'title': 'title',
            'description': 'description',
            'type': 'type',
            'required': 'required',
            'properties': 'properties'
        }

        self._id = None
        self._schema = None
        self._title = None
        self._description = None
        self._type = None
        self._required = None
        self._properties = None

    @property
    def id(self):
        """
        Gets the id of this JsonSchemaDocument.


        :return: The id of this JsonSchemaDocument.
        :rtype: str
        """
        return self._id

    @id.setter
    def id(self, id):
        """
        Sets the id of this JsonSchemaDocument.


        :param id: The id of this JsonSchemaDocument.
        :type: str
        """
        
        self._id = id

    @property
    def schema(self):
        """
        Gets the schema of this JsonSchemaDocument.


        :return: The schema of this JsonSchemaDocument.
        :rtype: str
        """
        return self._schema

    @schema.setter
    def schema(self, schema):
        """
        Sets the schema of this JsonSchemaDocument.


        :param schema: The schema of this JsonSchemaDocument.
        :type: str
        """
        
        self._schema = schema

    @property
    def title(self):
        """
        Gets the title of this JsonSchemaDocument.


        :return: The title of this JsonSchemaDocument.
        :rtype: str
        """
        return self._title

    @title.setter
    def title(self, title):
        """
        Sets the title of this JsonSchemaDocument.


        :param title: The title of this JsonSchemaDocument.
        :type: str
        """
        
        self._title = title

    @property
    def description(self):
        """
        Gets the description of this JsonSchemaDocument.


        :return: The description of this JsonSchemaDocument.
        :rtype: str
        """
        return self._description

    @description.setter
    def description(self, description):
        """
        Sets the description of this JsonSchemaDocument.


        :param description: The description of this JsonSchemaDocument.
        :type: str
        """
        
        self._description = description

    @property
    def type(self):
        """
        Gets the type of this JsonSchemaDocument.


        :return: The type of this JsonSchemaDocument.
        :rtype: str
        """
        return self._type

    @type.setter
    def type(self, type):
        """
        Sets the type of this JsonSchemaDocument.


        :param type: The type of this JsonSchemaDocument.
        :type: str
        """
        
        self._type = type

    @property
    def required(self):
        """
        Gets the required of this JsonSchemaDocument.


        :return: The required of this JsonSchemaDocument.
        :rtype: list[str]
        """
        return self._required

    @required.setter
    def required(self, required):
        """
        Sets the required of this JsonSchemaDocument.


        :param required: The required of this JsonSchemaDocument.
        :type: list[str]
        """
        
        self._required = required

    @property
    def properties(self):
        """
        Gets the properties of this JsonSchemaDocument.


        :return: The properties of this JsonSchemaDocument.
        :rtype: dict(str, object)
        """
        return self._properties

    @properties.setter
    def properties(self, properties):
        """
        Sets the properties of this JsonSchemaDocument.


        :param properties: The properties of this JsonSchemaDocument.
        :type: dict(str, object)
        """
        
        self._properties = properties

    def to_dict(self):
        """
        Returns the model properties as a dict
        """
        result = {}

        for attr, _ in iteritems(self.swagger_types):
            value = getattr(self, attr)
            if isinstance(value, list):
                result[attr] = list(map(
                    lambda x: x.to_dict() if hasattr(x, "to_dict") else x,
                    value
                ))
            elif hasattr(value, "to_dict"):
                result[attr] = value.to_dict()
            elif isinstance(value, dict):
                result[attr] = dict(map(
                    lambda item: (item[0], item[1].to_dict())
                    if hasattr(item[1], "to_dict") else item,
                    value.items()
                ))
            else:
                result[attr] = value

        return result

    def to_str(self):
        """
        Returns the string representation of the model
        """
        return pformat(self.to_dict())

    def __repr__(self):
        """
        For `print` and `pprint`
        """
        return self.to_str()

    def __eq__(self, other):
        """
        Returns true if both objects are equal
        """
        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """
        Returns true if both objects are not equal
        """
        return not self == other

