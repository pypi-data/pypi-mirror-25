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


class InteractionStatsAlert(object):
    """
    NOTE: This class is auto generated by the swagger code generator program.
    Do not edit the class manually.
    """
    def __init__(self):
        """
        InteractionStatsAlert - a model defined in Swagger

        :param dict swaggerTypes: The key is attribute name
                                  and the value is attribute type.
        :param dict attributeMap: The key is attribute name
                                  and the value is json key in definition.
        """
        self.swagger_types = {
            'id': 'str',
            'name': 'str',
            'dimension': 'str',
            'dimension_value': 'str',
            'metric': 'str',
            'media_type': 'str',
            'numeric_range': 'str',
            'statistic': 'str',
            'value': 'float',
            'rule_id': 'str',
            'unread': 'bool',
            'start_date': 'datetime',
            'end_date': 'datetime',
            'notification_users': 'list[User]',
            'alert_types': 'list[str]',
            'rule_uri': 'str',
            'self_uri': 'str'
        }

        self.attribute_map = {
            'id': 'id',
            'name': 'name',
            'dimension': 'dimension',
            'dimension_value': 'dimensionValue',
            'metric': 'metric',
            'media_type': 'mediaType',
            'numeric_range': 'numericRange',
            'statistic': 'statistic',
            'value': 'value',
            'rule_id': 'ruleId',
            'unread': 'unread',
            'start_date': 'startDate',
            'end_date': 'endDate',
            'notification_users': 'notificationUsers',
            'alert_types': 'alertTypes',
            'rule_uri': 'ruleUri',
            'self_uri': 'selfUri'
        }

        self._id = None
        self._name = None
        self._dimension = None
        self._dimension_value = None
        self._metric = None
        self._media_type = None
        self._numeric_range = None
        self._statistic = None
        self._value = None
        self._rule_id = None
        self._unread = None
        self._start_date = None
        self._end_date = None
        self._notification_users = None
        self._alert_types = None
        self._rule_uri = None
        self._self_uri = None

    @property
    def id(self):
        """
        Gets the id of this InteractionStatsAlert.
        The globally unique identifier for the object.

        :return: The id of this InteractionStatsAlert.
        :rtype: str
        """
        return self._id

    @id.setter
    def id(self, id):
        """
        Sets the id of this InteractionStatsAlert.
        The globally unique identifier for the object.

        :param id: The id of this InteractionStatsAlert.
        :type: str
        """
        
        self._id = id

    @property
    def name(self):
        """
        Gets the name of this InteractionStatsAlert.
        Name of the rule that generated the alert

        :return: The name of this InteractionStatsAlert.
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """
        Sets the name of this InteractionStatsAlert.
        Name of the rule that generated the alert

        :param name: The name of this InteractionStatsAlert.
        :type: str
        """
        
        self._name = name

    @property
    def dimension(self):
        """
        Gets the dimension of this InteractionStatsAlert.
        The dimension of concern.

        :return: The dimension of this InteractionStatsAlert.
        :rtype: str
        """
        return self._dimension

    @dimension.setter
    def dimension(self, dimension):
        """
        Sets the dimension of this InteractionStatsAlert.
        The dimension of concern.

        :param dimension: The dimension of this InteractionStatsAlert.
        :type: str
        """
        allowed_values = ["queueId", "userId"]
        if dimension.lower() not in map(str.lower, allowed_values):
            # print "Invalid value for dimension -> " + dimension
            self._dimension = "outdated_sdk_version"
        else:
            self._dimension = dimension

    @property
    def dimension_value(self):
        """
        Gets the dimension_value of this InteractionStatsAlert.
        The value of the dimension.

        :return: The dimension_value of this InteractionStatsAlert.
        :rtype: str
        """
        return self._dimension_value

    @dimension_value.setter
    def dimension_value(self, dimension_value):
        """
        Sets the dimension_value of this InteractionStatsAlert.
        The value of the dimension.

        :param dimension_value: The dimension_value of this InteractionStatsAlert.
        :type: str
        """
        
        self._dimension_value = dimension_value

    @property
    def metric(self):
        """
        Gets the metric of this InteractionStatsAlert.
        The metric to be assessed.

        :return: The metric of this InteractionStatsAlert.
        :rtype: str
        """
        return self._metric

    @metric.setter
    def metric(self, metric):
        """
        Sets the metric of this InteractionStatsAlert.
        The metric to be assessed.

        :param metric: The metric of this InteractionStatsAlert.
        :type: str
        """
        allowed_values = ["tAbandon", "tAnswered", "tTalk", "nOffered", "tHandle", "nTransferred", "oServiceLevel", "tWait", "tHeld", "tAcw"]
        if metric.lower() not in map(str.lower, allowed_values):
            # print "Invalid value for metric -> " + metric
            self._metric = "outdated_sdk_version"
        else:
            self._metric = metric

    @property
    def media_type(self):
        """
        Gets the media_type of this InteractionStatsAlert.
        The media type.

        :return: The media_type of this InteractionStatsAlert.
        :rtype: str
        """
        return self._media_type

    @media_type.setter
    def media_type(self, media_type):
        """
        Sets the media_type of this InteractionStatsAlert.
        The media type.

        :param media_type: The media_type of this InteractionStatsAlert.
        :type: str
        """
        allowed_values = ["voice", "chat", "email", "callback"]
        if media_type.lower() not in map(str.lower, allowed_values):
            # print "Invalid value for media_type -> " + media_type
            self._media_type = "outdated_sdk_version"
        else:
            self._media_type = media_type

    @property
    def numeric_range(self):
        """
        Gets the numeric_range of this InteractionStatsAlert.
        The comparison descriptor used against the metric's value.

        :return: The numeric_range of this InteractionStatsAlert.
        :rtype: str
        """
        return self._numeric_range

    @numeric_range.setter
    def numeric_range(self, numeric_range):
        """
        Sets the numeric_range of this InteractionStatsAlert.
        The comparison descriptor used against the metric's value.

        :param numeric_range: The numeric_range of this InteractionStatsAlert.
        :type: str
        """
        allowed_values = ["gt", "gte", "lt", "lte", "eq", "ne"]
        if numeric_range.lower() not in map(str.lower, allowed_values):
            # print "Invalid value for numeric_range -> " + numeric_range
            self._numeric_range = "outdated_sdk_version"
        else:
            self._numeric_range = numeric_range

    @property
    def statistic(self):
        """
        Gets the statistic of this InteractionStatsAlert.
        The statistic of concern for the metric.

        :return: The statistic of this InteractionStatsAlert.
        :rtype: str
        """
        return self._statistic

    @statistic.setter
    def statistic(self, statistic):
        """
        Sets the statistic of this InteractionStatsAlert.
        The statistic of concern for the metric.

        :param statistic: The statistic of this InteractionStatsAlert.
        :type: str
        """
        allowed_values = ["count", "min", "ratio", "max"]
        if statistic.lower() not in map(str.lower, allowed_values):
            # print "Invalid value for statistic -> " + statistic
            self._statistic = "outdated_sdk_version"
        else:
            self._statistic = statistic

    @property
    def value(self):
        """
        Gets the value of this InteractionStatsAlert.
        The threshold value.

        :return: The value of this InteractionStatsAlert.
        :rtype: float
        """
        return self._value

    @value.setter
    def value(self, value):
        """
        Sets the value of this InteractionStatsAlert.
        The threshold value.

        :param value: The value of this InteractionStatsAlert.
        :type: float
        """
        
        self._value = value

    @property
    def rule_id(self):
        """
        Gets the rule_id of this InteractionStatsAlert.
        The id of the rule.

        :return: The rule_id of this InteractionStatsAlert.
        :rtype: str
        """
        return self._rule_id

    @rule_id.setter
    def rule_id(self, rule_id):
        """
        Sets the rule_id of this InteractionStatsAlert.
        The id of the rule.

        :param rule_id: The rule_id of this InteractionStatsAlert.
        :type: str
        """
        
        self._rule_id = rule_id

    @property
    def unread(self):
        """
        Gets the unread of this InteractionStatsAlert.
        Indicates if the alert has been read.

        :return: The unread of this InteractionStatsAlert.
        :rtype: bool
        """
        return self._unread

    @unread.setter
    def unread(self, unread):
        """
        Sets the unread of this InteractionStatsAlert.
        Indicates if the alert has been read.

        :param unread: The unread of this InteractionStatsAlert.
        :type: bool
        """
        
        self._unread = unread

    @property
    def start_date(self):
        """
        Gets the start_date of this InteractionStatsAlert.
        The date/time the alert was created. Date time is represented as an ISO-8601 string. For example: yyyy-MM-ddTHH:mm:ss.SSSZ

        :return: The start_date of this InteractionStatsAlert.
        :rtype: datetime
        """
        return self._start_date

    @start_date.setter
    def start_date(self, start_date):
        """
        Sets the start_date of this InteractionStatsAlert.
        The date/time the alert was created. Date time is represented as an ISO-8601 string. For example: yyyy-MM-ddTHH:mm:ss.SSSZ

        :param start_date: The start_date of this InteractionStatsAlert.
        :type: datetime
        """
        
        self._start_date = start_date

    @property
    def end_date(self):
        """
        Gets the end_date of this InteractionStatsAlert.
        The date/time the owning rule exiting in alarm status. Date time is represented as an ISO-8601 string. For example: yyyy-MM-ddTHH:mm:ss.SSSZ

        :return: The end_date of this InteractionStatsAlert.
        :rtype: datetime
        """
        return self._end_date

    @end_date.setter
    def end_date(self, end_date):
        """
        Sets the end_date of this InteractionStatsAlert.
        The date/time the owning rule exiting in alarm status. Date time is represented as an ISO-8601 string. For example: yyyy-MM-ddTHH:mm:ss.SSSZ

        :param end_date: The end_date of this InteractionStatsAlert.
        :type: datetime
        """
        
        self._end_date = end_date

    @property
    def notification_users(self):
        """
        Gets the notification_users of this InteractionStatsAlert.
        The ids of users who were notified of alarm state change.

        :return: The notification_users of this InteractionStatsAlert.
        :rtype: list[User]
        """
        return self._notification_users

    @notification_users.setter
    def notification_users(self, notification_users):
        """
        Sets the notification_users of this InteractionStatsAlert.
        The ids of users who were notified of alarm state change.

        :param notification_users: The notification_users of this InteractionStatsAlert.
        :type: list[User]
        """
        
        self._notification_users = notification_users

    @property
    def alert_types(self):
        """
        Gets the alert_types of this InteractionStatsAlert.
        A collection of notification methods.

        :return: The alert_types of this InteractionStatsAlert.
        :rtype: list[str]
        """
        return self._alert_types

    @alert_types.setter
    def alert_types(self, alert_types):
        """
        Sets the alert_types of this InteractionStatsAlert.
        A collection of notification methods.

        :param alert_types: The alert_types of this InteractionStatsAlert.
        :type: list[str]
        """
        
        self._alert_types = alert_types

    @property
    def rule_uri(self):
        """
        Gets the rule_uri of this InteractionStatsAlert.


        :return: The rule_uri of this InteractionStatsAlert.
        :rtype: str
        """
        return self._rule_uri

    @rule_uri.setter
    def rule_uri(self, rule_uri):
        """
        Sets the rule_uri of this InteractionStatsAlert.


        :param rule_uri: The rule_uri of this InteractionStatsAlert.
        :type: str
        """
        
        self._rule_uri = rule_uri

    @property
    def self_uri(self):
        """
        Gets the self_uri of this InteractionStatsAlert.
        The URI for this object

        :return: The self_uri of this InteractionStatsAlert.
        :rtype: str
        """
        return self._self_uri

    @self_uri.setter
    def self_uri(self, self_uri):
        """
        Sets the self_uri of this InteractionStatsAlert.
        The URI for this object

        :param self_uri: The self_uri of this InteractionStatsAlert.
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

