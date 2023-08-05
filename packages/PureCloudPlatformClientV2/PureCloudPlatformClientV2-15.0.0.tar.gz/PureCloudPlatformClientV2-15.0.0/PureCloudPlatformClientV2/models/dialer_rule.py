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


class DialerRule(object):
    """
    NOTE: This class is auto generated by the swagger code generator program.
    Do not edit the class manually.
    """
    def __init__(self):
        """
        DialerRule - a model defined in Swagger

        :param dict swaggerTypes: The key is attribute name
                                  and the value is attribute type.
        :param dict attributeMap: The key is attribute name
                                  and the value is json key in definition.
        """
        self.swagger_types = {
            'id': 'str',
            'name': 'str',
            'order': 'int',
            'category': 'str',
            'conditions': 'list[Condition]',
            'actions': 'list[DialerAction]'
        }

        self.attribute_map = {
            'id': 'id',
            'name': 'name',
            'order': 'order',
            'category': 'category',
            'conditions': 'conditions',
            'actions': 'actions'
        }

        self._id = None
        self._name = None
        self._order = None
        self._category = None
        self._conditions = None
        self._actions = None

    @property
    def id(self):
        """
        Gets the id of this DialerRule.
        The identifier of the rule

        :return: The id of this DialerRule.
        :rtype: str
        """
        return self._id

    @id.setter
    def id(self, id):
        """
        Sets the id of this DialerRule.
        The identifier of the rule

        :param id: The id of this DialerRule.
        :type: str
        """
        
        self._id = id

    @property
    def name(self):
        """
        Gets the name of this DialerRule.
        The name of the rule

        :return: The name of this DialerRule.
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """
        Sets the name of this DialerRule.
        The name of the rule

        :param name: The name of this DialerRule.
        :type: str
        """
        
        self._name = name

    @property
    def order(self):
        """
        Gets the order of this DialerRule.
        The ranked order of the rule; rules are processed from lowest number to highest

        :return: The order of this DialerRule.
        :rtype: int
        """
        return self._order

    @order.setter
    def order(self, order):
        """
        Sets the order of this DialerRule.
        The ranked order of the rule; rules are processed from lowest number to highest

        :param order: The order of this DialerRule.
        :type: int
        """
        
        self._order = order

    @property
    def category(self):
        """
        Gets the category of this DialerRule.
        The category of the rule

        :return: The category of this DialerRule.
        :rtype: str
        """
        return self._category

    @category.setter
    def category(self, category):
        """
        Sets the category of this DialerRule.
        The category of the rule

        :param category: The category of this DialerRule.
        :type: str
        """
        allowed_values = ["DIALER_PRECALL", "DIALER_WRAPUP"]
        if category.lower() not in map(str.lower, allowed_values):
            # print "Invalid value for category -> " + category
            self._category = "outdated_sdk_version"
        else:
            self._category = category

    @property
    def conditions(self):
        """
        Gets the conditions of this DialerRule.
        The list of rule conditions; all must evaluate to true to trigger the rule actions

        :return: The conditions of this DialerRule.
        :rtype: list[Condition]
        """
        return self._conditions

    @conditions.setter
    def conditions(self, conditions):
        """
        Sets the conditions of this DialerRule.
        The list of rule conditions; all must evaluate to true to trigger the rule actions

        :param conditions: The conditions of this DialerRule.
        :type: list[Condition]
        """
        
        self._conditions = conditions

    @property
    def actions(self):
        """
        Gets the actions of this DialerRule.
        The list of rule actions to be taken if the conditions are true

        :return: The actions of this DialerRule.
        :rtype: list[DialerAction]
        """
        return self._actions

    @actions.setter
    def actions(self, actions):
        """
        Sets the actions of this DialerRule.
        The list of rule actions to be taken if the conditions are true

        :param actions: The actions of this DialerRule.
        :type: list[DialerAction]
        """
        
        self._actions = actions

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

