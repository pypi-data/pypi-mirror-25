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


class ConversationNotificationParticipants(object):
    """
    NOTE: This class is auto generated by the swagger code generator program.
    Do not edit the class manually.
    """
    def __init__(self):
        """
        ConversationNotificationParticipants - a model defined in Swagger

        :param dict swaggerTypes: The key is attribute name
                                  and the value is attribute type.
        :param dict attributeMap: The key is attribute name
                                  and the value is json key in definition.
        """
        self.swagger_types = {
            'id': 'str',
            'connected_time': 'datetime',
            'end_time': 'datetime',
            'user_id': 'str',
            'external_contact_id': 'str',
            'external_organization_id': 'str',
            'name': 'str',
            'queue_id': 'str',
            'group_id': 'str',
            'purpose': 'str',
            'consult_participant_id': 'str',
            'address': 'str',
            'wrapup_required': 'bool',
            'wrapup_expected': 'bool',
            'wrapup_prompt': 'str',
            'wrapup_timeout_ms': 'int',
            'wrapup': 'ConversationNotificationWrapup',
            'monitored_participant_id': 'str',
            'screen_recording_state': 'str',
            'attributes': 'dict(str, str)',
            'calls': 'list[ConversationNotificationCalls]',
            'callbacks': 'list[ConversationNotificationCallbacks]',
            'chats': 'list[ConversationNotificationChats]',
            'cobrowsesessions': 'list[ConversationNotificationCobrowsesessions]',
            'emails': 'list[ConversationNotificationEmails]',
            'screenshares': 'list[ConversationNotificationScreenshares]',
            'social_expressions': 'list[ConversationNotificationSocialExpressions]',
            'videos': 'list[ConversationNotificationVideos]',
            'additional_properties': 'object'
        }

        self.attribute_map = {
            'id': 'id',
            'connected_time': 'connectedTime',
            'end_time': 'endTime',
            'user_id': 'userId',
            'external_contact_id': 'externalContactId',
            'external_organization_id': 'externalOrganizationId',
            'name': 'name',
            'queue_id': 'queueId',
            'group_id': 'groupId',
            'purpose': 'purpose',
            'consult_participant_id': 'consultParticipantId',
            'address': 'address',
            'wrapup_required': 'wrapupRequired',
            'wrapup_expected': 'wrapupExpected',
            'wrapup_prompt': 'wrapupPrompt',
            'wrapup_timeout_ms': 'wrapupTimeoutMs',
            'wrapup': 'wrapup',
            'monitored_participant_id': 'monitoredParticipantId',
            'screen_recording_state': 'screenRecordingState',
            'attributes': 'attributes',
            'calls': 'calls',
            'callbacks': 'callbacks',
            'chats': 'chats',
            'cobrowsesessions': 'cobrowsesessions',
            'emails': 'emails',
            'screenshares': 'screenshares',
            'social_expressions': 'socialExpressions',
            'videos': 'videos',
            'additional_properties': 'additionalProperties'
        }

        self._id = None
        self._connected_time = None
        self._end_time = None
        self._user_id = None
        self._external_contact_id = None
        self._external_organization_id = None
        self._name = None
        self._queue_id = None
        self._group_id = None
        self._purpose = None
        self._consult_participant_id = None
        self._address = None
        self._wrapup_required = None
        self._wrapup_expected = None
        self._wrapup_prompt = None
        self._wrapup_timeout_ms = None
        self._wrapup = None
        self._monitored_participant_id = None
        self._screen_recording_state = None
        self._attributes = None
        self._calls = None
        self._callbacks = None
        self._chats = None
        self._cobrowsesessions = None
        self._emails = None
        self._screenshares = None
        self._social_expressions = None
        self._videos = None
        self._additional_properties = None

    @property
    def id(self):
        """
        Gets the id of this ConversationNotificationParticipants.


        :return: The id of this ConversationNotificationParticipants.
        :rtype: str
        """
        return self._id

    @id.setter
    def id(self, id):
        """
        Sets the id of this ConversationNotificationParticipants.


        :param id: The id of this ConversationNotificationParticipants.
        :type: str
        """
        
        self._id = id

    @property
    def connected_time(self):
        """
        Gets the connected_time of this ConversationNotificationParticipants.


        :return: The connected_time of this ConversationNotificationParticipants.
        :rtype: datetime
        """
        return self._connected_time

    @connected_time.setter
    def connected_time(self, connected_time):
        """
        Sets the connected_time of this ConversationNotificationParticipants.


        :param connected_time: The connected_time of this ConversationNotificationParticipants.
        :type: datetime
        """
        
        self._connected_time = connected_time

    @property
    def end_time(self):
        """
        Gets the end_time of this ConversationNotificationParticipants.


        :return: The end_time of this ConversationNotificationParticipants.
        :rtype: datetime
        """
        return self._end_time

    @end_time.setter
    def end_time(self, end_time):
        """
        Sets the end_time of this ConversationNotificationParticipants.


        :param end_time: The end_time of this ConversationNotificationParticipants.
        :type: datetime
        """
        
        self._end_time = end_time

    @property
    def user_id(self):
        """
        Gets the user_id of this ConversationNotificationParticipants.


        :return: The user_id of this ConversationNotificationParticipants.
        :rtype: str
        """
        return self._user_id

    @user_id.setter
    def user_id(self, user_id):
        """
        Sets the user_id of this ConversationNotificationParticipants.


        :param user_id: The user_id of this ConversationNotificationParticipants.
        :type: str
        """
        
        self._user_id = user_id

    @property
    def external_contact_id(self):
        """
        Gets the external_contact_id of this ConversationNotificationParticipants.


        :return: The external_contact_id of this ConversationNotificationParticipants.
        :rtype: str
        """
        return self._external_contact_id

    @external_contact_id.setter
    def external_contact_id(self, external_contact_id):
        """
        Sets the external_contact_id of this ConversationNotificationParticipants.


        :param external_contact_id: The external_contact_id of this ConversationNotificationParticipants.
        :type: str
        """
        
        self._external_contact_id = external_contact_id

    @property
    def external_organization_id(self):
        """
        Gets the external_organization_id of this ConversationNotificationParticipants.


        :return: The external_organization_id of this ConversationNotificationParticipants.
        :rtype: str
        """
        return self._external_organization_id

    @external_organization_id.setter
    def external_organization_id(self, external_organization_id):
        """
        Sets the external_organization_id of this ConversationNotificationParticipants.


        :param external_organization_id: The external_organization_id of this ConversationNotificationParticipants.
        :type: str
        """
        
        self._external_organization_id = external_organization_id

    @property
    def name(self):
        """
        Gets the name of this ConversationNotificationParticipants.


        :return: The name of this ConversationNotificationParticipants.
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """
        Sets the name of this ConversationNotificationParticipants.


        :param name: The name of this ConversationNotificationParticipants.
        :type: str
        """
        
        self._name = name

    @property
    def queue_id(self):
        """
        Gets the queue_id of this ConversationNotificationParticipants.


        :return: The queue_id of this ConversationNotificationParticipants.
        :rtype: str
        """
        return self._queue_id

    @queue_id.setter
    def queue_id(self, queue_id):
        """
        Sets the queue_id of this ConversationNotificationParticipants.


        :param queue_id: The queue_id of this ConversationNotificationParticipants.
        :type: str
        """
        
        self._queue_id = queue_id

    @property
    def group_id(self):
        """
        Gets the group_id of this ConversationNotificationParticipants.


        :return: The group_id of this ConversationNotificationParticipants.
        :rtype: str
        """
        return self._group_id

    @group_id.setter
    def group_id(self, group_id):
        """
        Sets the group_id of this ConversationNotificationParticipants.


        :param group_id: The group_id of this ConversationNotificationParticipants.
        :type: str
        """
        
        self._group_id = group_id

    @property
    def purpose(self):
        """
        Gets the purpose of this ConversationNotificationParticipants.


        :return: The purpose of this ConversationNotificationParticipants.
        :rtype: str
        """
        return self._purpose

    @purpose.setter
    def purpose(self, purpose):
        """
        Sets the purpose of this ConversationNotificationParticipants.


        :param purpose: The purpose of this ConversationNotificationParticipants.
        :type: str
        """
        
        self._purpose = purpose

    @property
    def consult_participant_id(self):
        """
        Gets the consult_participant_id of this ConversationNotificationParticipants.


        :return: The consult_participant_id of this ConversationNotificationParticipants.
        :rtype: str
        """
        return self._consult_participant_id

    @consult_participant_id.setter
    def consult_participant_id(self, consult_participant_id):
        """
        Sets the consult_participant_id of this ConversationNotificationParticipants.


        :param consult_participant_id: The consult_participant_id of this ConversationNotificationParticipants.
        :type: str
        """
        
        self._consult_participant_id = consult_participant_id

    @property
    def address(self):
        """
        Gets the address of this ConversationNotificationParticipants.


        :return: The address of this ConversationNotificationParticipants.
        :rtype: str
        """
        return self._address

    @address.setter
    def address(self, address):
        """
        Sets the address of this ConversationNotificationParticipants.


        :param address: The address of this ConversationNotificationParticipants.
        :type: str
        """
        
        self._address = address

    @property
    def wrapup_required(self):
        """
        Gets the wrapup_required of this ConversationNotificationParticipants.


        :return: The wrapup_required of this ConversationNotificationParticipants.
        :rtype: bool
        """
        return self._wrapup_required

    @wrapup_required.setter
    def wrapup_required(self, wrapup_required):
        """
        Sets the wrapup_required of this ConversationNotificationParticipants.


        :param wrapup_required: The wrapup_required of this ConversationNotificationParticipants.
        :type: bool
        """
        
        self._wrapup_required = wrapup_required

    @property
    def wrapup_expected(self):
        """
        Gets the wrapup_expected of this ConversationNotificationParticipants.


        :return: The wrapup_expected of this ConversationNotificationParticipants.
        :rtype: bool
        """
        return self._wrapup_expected

    @wrapup_expected.setter
    def wrapup_expected(self, wrapup_expected):
        """
        Sets the wrapup_expected of this ConversationNotificationParticipants.


        :param wrapup_expected: The wrapup_expected of this ConversationNotificationParticipants.
        :type: bool
        """
        
        self._wrapup_expected = wrapup_expected

    @property
    def wrapup_prompt(self):
        """
        Gets the wrapup_prompt of this ConversationNotificationParticipants.


        :return: The wrapup_prompt of this ConversationNotificationParticipants.
        :rtype: str
        """
        return self._wrapup_prompt

    @wrapup_prompt.setter
    def wrapup_prompt(self, wrapup_prompt):
        """
        Sets the wrapup_prompt of this ConversationNotificationParticipants.


        :param wrapup_prompt: The wrapup_prompt of this ConversationNotificationParticipants.
        :type: str
        """
        
        self._wrapup_prompt = wrapup_prompt

    @property
    def wrapup_timeout_ms(self):
        """
        Gets the wrapup_timeout_ms of this ConversationNotificationParticipants.


        :return: The wrapup_timeout_ms of this ConversationNotificationParticipants.
        :rtype: int
        """
        return self._wrapup_timeout_ms

    @wrapup_timeout_ms.setter
    def wrapup_timeout_ms(self, wrapup_timeout_ms):
        """
        Sets the wrapup_timeout_ms of this ConversationNotificationParticipants.


        :param wrapup_timeout_ms: The wrapup_timeout_ms of this ConversationNotificationParticipants.
        :type: int
        """
        
        self._wrapup_timeout_ms = wrapup_timeout_ms

    @property
    def wrapup(self):
        """
        Gets the wrapup of this ConversationNotificationParticipants.


        :return: The wrapup of this ConversationNotificationParticipants.
        :rtype: ConversationNotificationWrapup
        """
        return self._wrapup

    @wrapup.setter
    def wrapup(self, wrapup):
        """
        Sets the wrapup of this ConversationNotificationParticipants.


        :param wrapup: The wrapup of this ConversationNotificationParticipants.
        :type: ConversationNotificationWrapup
        """
        
        self._wrapup = wrapup

    @property
    def monitored_participant_id(self):
        """
        Gets the monitored_participant_id of this ConversationNotificationParticipants.


        :return: The monitored_participant_id of this ConversationNotificationParticipants.
        :rtype: str
        """
        return self._monitored_participant_id

    @monitored_participant_id.setter
    def monitored_participant_id(self, monitored_participant_id):
        """
        Sets the monitored_participant_id of this ConversationNotificationParticipants.


        :param monitored_participant_id: The monitored_participant_id of this ConversationNotificationParticipants.
        :type: str
        """
        
        self._monitored_participant_id = monitored_participant_id

    @property
    def screen_recording_state(self):
        """
        Gets the screen_recording_state of this ConversationNotificationParticipants.


        :return: The screen_recording_state of this ConversationNotificationParticipants.
        :rtype: str
        """
        return self._screen_recording_state

    @screen_recording_state.setter
    def screen_recording_state(self, screen_recording_state):
        """
        Sets the screen_recording_state of this ConversationNotificationParticipants.


        :param screen_recording_state: The screen_recording_state of this ConversationNotificationParticipants.
        :type: str
        """
        allowed_values = ["REQUESTED", "ACTIVE", "PAUSED", "STOPPED", "ERROR"]
        if screen_recording_state.lower() not in map(str.lower, allowed_values):
            # print "Invalid value for screen_recording_state -> " + screen_recording_state
            self._screen_recording_state = "outdated_sdk_version"
        else:
            self._screen_recording_state = screen_recording_state

    @property
    def attributes(self):
        """
        Gets the attributes of this ConversationNotificationParticipants.


        :return: The attributes of this ConversationNotificationParticipants.
        :rtype: dict(str, str)
        """
        return self._attributes

    @attributes.setter
    def attributes(self, attributes):
        """
        Sets the attributes of this ConversationNotificationParticipants.


        :param attributes: The attributes of this ConversationNotificationParticipants.
        :type: dict(str, str)
        """
        
        self._attributes = attributes

    @property
    def calls(self):
        """
        Gets the calls of this ConversationNotificationParticipants.


        :return: The calls of this ConversationNotificationParticipants.
        :rtype: list[ConversationNotificationCalls]
        """
        return self._calls

    @calls.setter
    def calls(self, calls):
        """
        Sets the calls of this ConversationNotificationParticipants.


        :param calls: The calls of this ConversationNotificationParticipants.
        :type: list[ConversationNotificationCalls]
        """
        
        self._calls = calls

    @property
    def callbacks(self):
        """
        Gets the callbacks of this ConversationNotificationParticipants.


        :return: The callbacks of this ConversationNotificationParticipants.
        :rtype: list[ConversationNotificationCallbacks]
        """
        return self._callbacks

    @callbacks.setter
    def callbacks(self, callbacks):
        """
        Sets the callbacks of this ConversationNotificationParticipants.


        :param callbacks: The callbacks of this ConversationNotificationParticipants.
        :type: list[ConversationNotificationCallbacks]
        """
        
        self._callbacks = callbacks

    @property
    def chats(self):
        """
        Gets the chats of this ConversationNotificationParticipants.


        :return: The chats of this ConversationNotificationParticipants.
        :rtype: list[ConversationNotificationChats]
        """
        return self._chats

    @chats.setter
    def chats(self, chats):
        """
        Sets the chats of this ConversationNotificationParticipants.


        :param chats: The chats of this ConversationNotificationParticipants.
        :type: list[ConversationNotificationChats]
        """
        
        self._chats = chats

    @property
    def cobrowsesessions(self):
        """
        Gets the cobrowsesessions of this ConversationNotificationParticipants.


        :return: The cobrowsesessions of this ConversationNotificationParticipants.
        :rtype: list[ConversationNotificationCobrowsesessions]
        """
        return self._cobrowsesessions

    @cobrowsesessions.setter
    def cobrowsesessions(self, cobrowsesessions):
        """
        Sets the cobrowsesessions of this ConversationNotificationParticipants.


        :param cobrowsesessions: The cobrowsesessions of this ConversationNotificationParticipants.
        :type: list[ConversationNotificationCobrowsesessions]
        """
        
        self._cobrowsesessions = cobrowsesessions

    @property
    def emails(self):
        """
        Gets the emails of this ConversationNotificationParticipants.


        :return: The emails of this ConversationNotificationParticipants.
        :rtype: list[ConversationNotificationEmails]
        """
        return self._emails

    @emails.setter
    def emails(self, emails):
        """
        Sets the emails of this ConversationNotificationParticipants.


        :param emails: The emails of this ConversationNotificationParticipants.
        :type: list[ConversationNotificationEmails]
        """
        
        self._emails = emails

    @property
    def screenshares(self):
        """
        Gets the screenshares of this ConversationNotificationParticipants.


        :return: The screenshares of this ConversationNotificationParticipants.
        :rtype: list[ConversationNotificationScreenshares]
        """
        return self._screenshares

    @screenshares.setter
    def screenshares(self, screenshares):
        """
        Sets the screenshares of this ConversationNotificationParticipants.


        :param screenshares: The screenshares of this ConversationNotificationParticipants.
        :type: list[ConversationNotificationScreenshares]
        """
        
        self._screenshares = screenshares

    @property
    def social_expressions(self):
        """
        Gets the social_expressions of this ConversationNotificationParticipants.


        :return: The social_expressions of this ConversationNotificationParticipants.
        :rtype: list[ConversationNotificationSocialExpressions]
        """
        return self._social_expressions

    @social_expressions.setter
    def social_expressions(self, social_expressions):
        """
        Sets the social_expressions of this ConversationNotificationParticipants.


        :param social_expressions: The social_expressions of this ConversationNotificationParticipants.
        :type: list[ConversationNotificationSocialExpressions]
        """
        
        self._social_expressions = social_expressions

    @property
    def videos(self):
        """
        Gets the videos of this ConversationNotificationParticipants.


        :return: The videos of this ConversationNotificationParticipants.
        :rtype: list[ConversationNotificationVideos]
        """
        return self._videos

    @videos.setter
    def videos(self, videos):
        """
        Sets the videos of this ConversationNotificationParticipants.


        :param videos: The videos of this ConversationNotificationParticipants.
        :type: list[ConversationNotificationVideos]
        """
        
        self._videos = videos

    @property
    def additional_properties(self):
        """
        Gets the additional_properties of this ConversationNotificationParticipants.


        :return: The additional_properties of this ConversationNotificationParticipants.
        :rtype: object
        """
        return self._additional_properties

    @additional_properties.setter
    def additional_properties(self, additional_properties):
        """
        Sets the additional_properties of this ConversationNotificationParticipants.


        :param additional_properties: The additional_properties of this ConversationNotificationParticipants.
        :type: object
        """
        
        self._additional_properties = additional_properties

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

