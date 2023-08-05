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


class ContactListFilter(object):
    """
    NOTE: This class is auto generated by the swagger code generator program.
    Do not edit the class manually.
    """
    def __init__(self):
        """
        ContactListFilter - a model defined in Swagger

        :param dict swaggerTypes: The key is attribute name
                                  and the value is attribute type.
        :param dict attributeMap: The key is attribute name
                                  and the value is json key in definition.
        """
        self.swagger_types = {
            'id': 'str',
            'name': 'str',
            'date_created': 'datetime',
            'date_modified': 'datetime',
            'version': 'int',
            'contact_list': 'UriReference',
            'clauses': 'list[ContactListFilterClause]',
            'filter_type': 'str',
            'self_uri': 'str'
        }

        self.attribute_map = {
            'id': 'id',
            'name': 'name',
            'date_created': 'dateCreated',
            'date_modified': 'dateModified',
            'version': 'version',
            'contact_list': 'contactList',
            'clauses': 'clauses',
            'filter_type': 'filterType',
            'self_uri': 'selfUri'
        }

        self._id = None
        self._name = None
        self._date_created = None
        self._date_modified = None
        self._version = None
        self._contact_list = None
        self._clauses = None
        self._filter_type = None
        self._self_uri = None

    @property
    def id(self):
        """
        Gets the id of this ContactListFilter.
        The globally unique identifier for the object.

        :return: The id of this ContactListFilter.
        :rtype: str
        """
        return self._id

    @id.setter
    def id(self, id):
        """
        Sets the id of this ContactListFilter.
        The globally unique identifier for the object.

        :param id: The id of this ContactListFilter.
        :type: str
        """
        
        self._id = id

    @property
    def name(self):
        """
        Gets the name of this ContactListFilter.


        :return: The name of this ContactListFilter.
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """
        Sets the name of this ContactListFilter.


        :param name: The name of this ContactListFilter.
        :type: str
        """
        
        self._name = name

    @property
    def date_created(self):
        """
        Gets the date_created of this ContactListFilter.
        Creation time of the entity. Date time is represented as an ISO-8601 string. For example: yyyy-MM-ddTHH:mm:ss.SSSZ

        :return: The date_created of this ContactListFilter.
        :rtype: datetime
        """
        return self._date_created

    @date_created.setter
    def date_created(self, date_created):
        """
        Sets the date_created of this ContactListFilter.
        Creation time of the entity. Date time is represented as an ISO-8601 string. For example: yyyy-MM-ddTHH:mm:ss.SSSZ

        :param date_created: The date_created of this ContactListFilter.
        :type: datetime
        """
        
        self._date_created = date_created

    @property
    def date_modified(self):
        """
        Gets the date_modified of this ContactListFilter.
        Last modified time of the entity. Date time is represented as an ISO-8601 string. For example: yyyy-MM-ddTHH:mm:ss.SSSZ

        :return: The date_modified of this ContactListFilter.
        :rtype: datetime
        """
        return self._date_modified

    @date_modified.setter
    def date_modified(self, date_modified):
        """
        Sets the date_modified of this ContactListFilter.
        Last modified time of the entity. Date time is represented as an ISO-8601 string. For example: yyyy-MM-ddTHH:mm:ss.SSSZ

        :param date_modified: The date_modified of this ContactListFilter.
        :type: datetime
        """
        
        self._date_modified = date_modified

    @property
    def version(self):
        """
        Gets the version of this ContactListFilter.
        Required for updates, must match the version number of the most recent update

        :return: The version of this ContactListFilter.
        :rtype: int
        """
        return self._version

    @version.setter
    def version(self, version):
        """
        Sets the version of this ContactListFilter.
        Required for updates, must match the version number of the most recent update

        :param version: The version of this ContactListFilter.
        :type: int
        """
        
        self._version = version

    @property
    def contact_list(self):
        """
        Gets the contact_list of this ContactListFilter.
        The contact list the filter is based on

        :return: The contact_list of this ContactListFilter.
        :rtype: UriReference
        """
        return self._contact_list

    @contact_list.setter
    def contact_list(self, contact_list):
        """
        Sets the contact_list of this ContactListFilter.
        The contact list the filter is based on

        :param contact_list: The contact_list of this ContactListFilter.
        :type: UriReference
        """
        
        self._contact_list = contact_list

    @property
    def clauses(self):
        """
        Gets the clauses of this ContactListFilter.


        :return: The clauses of this ContactListFilter.
        :rtype: list[ContactListFilterClause]
        """
        return self._clauses

    @clauses.setter
    def clauses(self, clauses):
        """
        Sets the clauses of this ContactListFilter.


        :param clauses: The clauses of this ContactListFilter.
        :type: list[ContactListFilterClause]
        """
        
        self._clauses = clauses

    @property
    def filter_type(self):
        """
        Gets the filter_type of this ContactListFilter.
        The filter type tells the api how to compare between clauses

        :return: The filter_type of this ContactListFilter.
        :rtype: str
        """
        return self._filter_type

    @filter_type.setter
    def filter_type(self, filter_type):
        """
        Sets the filter_type of this ContactListFilter.
        The filter type tells the api how to compare between clauses

        :param filter_type: The filter_type of this ContactListFilter.
        :type: str
        """
        allowed_values = ["AND", "OR"]
        if filter_type.lower() not in map(str.lower, allowed_values):
            # print "Invalid value for filter_type -> " + filter_type
            self._filter_type = "outdated_sdk_version"
        else:
            self._filter_type = filter_type

    @property
    def self_uri(self):
        """
        Gets the self_uri of this ContactListFilter.
        The URI for this object

        :return: The self_uri of this ContactListFilter.
        :rtype: str
        """
        return self._self_uri

    @self_uri.setter
    def self_uri(self, self_uri):
        """
        Sets the self_uri of this ContactListFilter.
        The URI for this object

        :param self_uri: The self_uri of this ContactListFilter.
        :type: str
        """
        
        self._self_uri = self_uri

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

