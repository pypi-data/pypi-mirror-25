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


class UserConversationSummaryNotification(object):
    """
    NOTE: This class is auto generated by the swagger code generator program.
    Do not edit the class manually.
    """
    def __init__(self):
        """
        UserConversationSummaryNotification - a model defined in Swagger

        :param dict swaggerTypes: The key is attribute name
                                  and the value is attribute type.
        :param dict attributeMap: The key is attribute name
                                  and the value is json key in definition.
        """
        self.swagger_types = {
            'user_id': 'str',
            'call': 'UserConversationSummaryNotificationCall',
            'callback': 'UserConversationSummaryNotificationMediaSummary',
            'email': 'UserConversationSummaryNotificationMediaSummary',
            'chat': 'UserConversationSummaryNotificationMediaSummary',
            'social_expression': 'UserConversationSummaryNotificationMediaSummary',
            'video': 'UserConversationSummaryNotificationMediaSummary'
        }

        self.attribute_map = {
            'user_id': 'userId',
            'call': 'call',
            'callback': 'callback',
            'email': 'email',
            'chat': 'chat',
            'social_expression': 'socialExpression',
            'video': 'video'
        }

        self._user_id = None
        self._call = None
        self._callback = None
        self._email = None
        self._chat = None
        self._social_expression = None
        self._video = None

    @property
    def user_id(self):
        """
        Gets the user_id of this UserConversationSummaryNotification.


        :return: The user_id of this UserConversationSummaryNotification.
        :rtype: str
        """
        return self._user_id

    @user_id.setter
    def user_id(self, user_id):
        """
        Sets the user_id of this UserConversationSummaryNotification.


        :param user_id: The user_id of this UserConversationSummaryNotification.
        :type: str
        """
        
        self._user_id = user_id

    @property
    def call(self):
        """
        Gets the call of this UserConversationSummaryNotification.


        :return: The call of this UserConversationSummaryNotification.
        :rtype: UserConversationSummaryNotificationCall
        """
        return self._call

    @call.setter
    def call(self, call):
        """
        Sets the call of this UserConversationSummaryNotification.


        :param call: The call of this UserConversationSummaryNotification.
        :type: UserConversationSummaryNotificationCall
        """
        
        self._call = call

    @property
    def callback(self):
        """
        Gets the callback of this UserConversationSummaryNotification.


        :return: The callback of this UserConversationSummaryNotification.
        :rtype: UserConversationSummaryNotificationMediaSummary
        """
        return self._callback

    @callback.setter
    def callback(self, callback):
        """
        Sets the callback of this UserConversationSummaryNotification.


        :param callback: The callback of this UserConversationSummaryNotification.
        :type: UserConversationSummaryNotificationMediaSummary
        """
        
        self._callback = callback

    @property
    def email(self):
        """
        Gets the email of this UserConversationSummaryNotification.


        :return: The email of this UserConversationSummaryNotification.
        :rtype: UserConversationSummaryNotificationMediaSummary
        """
        return self._email

    @email.setter
    def email(self, email):
        """
        Sets the email of this UserConversationSummaryNotification.


        :param email: The email of this UserConversationSummaryNotification.
        :type: UserConversationSummaryNotificationMediaSummary
        """
        
        self._email = email

    @property
    def chat(self):
        """
        Gets the chat of this UserConversationSummaryNotification.


        :return: The chat of this UserConversationSummaryNotification.
        :rtype: UserConversationSummaryNotificationMediaSummary
        """
        return self._chat

    @chat.setter
    def chat(self, chat):
        """
        Sets the chat of this UserConversationSummaryNotification.


        :param chat: The chat of this UserConversationSummaryNotification.
        :type: UserConversationSummaryNotificationMediaSummary
        """
        
        self._chat = chat

    @property
    def social_expression(self):
        """
        Gets the social_expression of this UserConversationSummaryNotification.


        :return: The social_expression of this UserConversationSummaryNotification.
        :rtype: UserConversationSummaryNotificationMediaSummary
        """
        return self._social_expression

    @social_expression.setter
    def social_expression(self, social_expression):
        """
        Sets the social_expression of this UserConversationSummaryNotification.


        :param social_expression: The social_expression of this UserConversationSummaryNotification.
        :type: UserConversationSummaryNotificationMediaSummary
        """
        
        self._social_expression = social_expression

    @property
    def video(self):
        """
        Gets the video of this UserConversationSummaryNotification.


        :return: The video of this UserConversationSummaryNotification.
        :rtype: UserConversationSummaryNotificationMediaSummary
        """
        return self._video

    @video.setter
    def video(self, video):
        """
        Sets the video of this UserConversationSummaryNotification.


        :param video: The video of this UserConversationSummaryNotification.
        :type: UserConversationSummaryNotificationMediaSummary
        """
        
        self._video = video

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

