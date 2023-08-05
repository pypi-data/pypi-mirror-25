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


class ParticipantBasic(object):
    """
    NOTE: This class is auto generated by the swagger code generator program.
    Do not edit the class manually.
    """
    def __init__(self):
        """
        ParticipantBasic - a model defined in Swagger

        :param dict swaggerTypes: The key is attribute name
                                  and the value is attribute type.
        :param dict attributeMap: The key is attribute name
                                  and the value is json key in definition.
        """
        self.swagger_types = {
            'id': 'str',
            'start_time': 'datetime',
            'end_time': 'datetime',
            'connected_time': 'datetime',
            'name': 'str',
            'user_uri': 'str',
            'user_id': 'str',
            'external_contact_id': 'str',
            'external_organization_id': 'str',
            'queue_id': 'str',
            'group_id': 'str',
            'queue_name': 'str',
            'purpose': 'str',
            'participant_type': 'str',
            'consult_participant_id': 'str',
            'address': 'str',
            'ani': 'str',
            'ani_name': 'str',
            'dnis': 'str',
            'locale': 'str',
            'wrapup_required': 'bool',
            'wrapup_prompt': 'str',
            'wrapup_timeout_ms': 'int',
            'wrapup_skipped': 'bool',
            'wrapup': 'Wrapup',
            'monitored_participant_id': 'str',
            'attributes': 'dict(str, str)',
            'calls': 'list[CallBasic]',
            'callbacks': 'list[CallbackBasic]',
            'chats': 'list[ConversationChat]',
            'cobrowsesessions': 'list[Cobrowsesession]',
            'emails': 'list[Email]',
            'screenshares': 'list[Screenshare]',
            'social_expressions': 'list[SocialExpression]',
            'videos': 'list[Video]',
            'evaluations': 'list[Evaluation]',
            'screen_recording_state': 'str'
        }

        self.attribute_map = {
            'id': 'id',
            'start_time': 'startTime',
            'end_time': 'endTime',
            'connected_time': 'connectedTime',
            'name': 'name',
            'user_uri': 'userUri',
            'user_id': 'userId',
            'external_contact_id': 'externalContactId',
            'external_organization_id': 'externalOrganizationId',
            'queue_id': 'queueId',
            'group_id': 'groupId',
            'queue_name': 'queueName',
            'purpose': 'purpose',
            'participant_type': 'participantType',
            'consult_participant_id': 'consultParticipantId',
            'address': 'address',
            'ani': 'ani',
            'ani_name': 'aniName',
            'dnis': 'dnis',
            'locale': 'locale',
            'wrapup_required': 'wrapupRequired',
            'wrapup_prompt': 'wrapupPrompt',
            'wrapup_timeout_ms': 'wrapupTimeoutMs',
            'wrapup_skipped': 'wrapupSkipped',
            'wrapup': 'wrapup',
            'monitored_participant_id': 'monitoredParticipantId',
            'attributes': 'attributes',
            'calls': 'calls',
            'callbacks': 'callbacks',
            'chats': 'chats',
            'cobrowsesessions': 'cobrowsesessions',
            'emails': 'emails',
            'screenshares': 'screenshares',
            'social_expressions': 'socialExpressions',
            'videos': 'videos',
            'evaluations': 'evaluations',
            'screen_recording_state': 'screenRecordingState'
        }

        self._id = None
        self._start_time = None
        self._end_time = None
        self._connected_time = None
        self._name = None
        self._user_uri = None
        self._user_id = None
        self._external_contact_id = None
        self._external_organization_id = None
        self._queue_id = None
        self._group_id = None
        self._queue_name = None
        self._purpose = None
        self._participant_type = None
        self._consult_participant_id = None
        self._address = None
        self._ani = None
        self._ani_name = None
        self._dnis = None
        self._locale = None
        self._wrapup_required = None
        self._wrapup_prompt = None
        self._wrapup_timeout_ms = None
        self._wrapup_skipped = None
        self._wrapup = None
        self._monitored_participant_id = None
        self._attributes = None
        self._calls = None
        self._callbacks = None
        self._chats = None
        self._cobrowsesessions = None
        self._emails = None
        self._screenshares = None
        self._social_expressions = None
        self._videos = None
        self._evaluations = None
        self._screen_recording_state = None

    @property
    def id(self):
        """
        Gets the id of this ParticipantBasic.
        A globally unique identifier for this conversation.

        :return: The id of this ParticipantBasic.
        :rtype: str
        """
        return self._id

    @id.setter
    def id(self, id):
        """
        Sets the id of this ParticipantBasic.
        A globally unique identifier for this conversation.

        :param id: The id of this ParticipantBasic.
        :type: str
        """
        
        self._id = id

    @property
    def start_time(self):
        """
        Gets the start_time of this ParticipantBasic.
        The timestamp when this participant joined the conversation in the provider clock. Date time is represented as an ISO-8601 string. For example: yyyy-MM-ddTHH:mm:ss.SSSZ

        :return: The start_time of this ParticipantBasic.
        :rtype: datetime
        """
        return self._start_time

    @start_time.setter
    def start_time(self, start_time):
        """
        Sets the start_time of this ParticipantBasic.
        The timestamp when this participant joined the conversation in the provider clock. Date time is represented as an ISO-8601 string. For example: yyyy-MM-ddTHH:mm:ss.SSSZ

        :param start_time: The start_time of this ParticipantBasic.
        :type: datetime
        """
        
        self._start_time = start_time

    @property
    def end_time(self):
        """
        Gets the end_time of this ParticipantBasic.
        The timestamp when this participant disconnected from the conversation in the provider clock. Date time is represented as an ISO-8601 string. For example: yyyy-MM-ddTHH:mm:ss.SSSZ

        :return: The end_time of this ParticipantBasic.
        :rtype: datetime
        """
        return self._end_time

    @end_time.setter
    def end_time(self, end_time):
        """
        Sets the end_time of this ParticipantBasic.
        The timestamp when this participant disconnected from the conversation in the provider clock. Date time is represented as an ISO-8601 string. For example: yyyy-MM-ddTHH:mm:ss.SSSZ

        :param end_time: The end_time of this ParticipantBasic.
        :type: datetime
        """
        
        self._end_time = end_time

    @property
    def connected_time(self):
        """
        Gets the connected_time of this ParticipantBasic.
        The timestamp when this participant was connected to the conversation in the provider clock. Date time is represented as an ISO-8601 string. For example: yyyy-MM-ddTHH:mm:ss.SSSZ

        :return: The connected_time of this ParticipantBasic.
        :rtype: datetime
        """
        return self._connected_time

    @connected_time.setter
    def connected_time(self, connected_time):
        """
        Sets the connected_time of this ParticipantBasic.
        The timestamp when this participant was connected to the conversation in the provider clock. Date time is represented as an ISO-8601 string. For example: yyyy-MM-ddTHH:mm:ss.SSSZ

        :param connected_time: The connected_time of this ParticipantBasic.
        :type: datetime
        """
        
        self._connected_time = connected_time

    @property
    def name(self):
        """
        Gets the name of this ParticipantBasic.
        A human readable name identifying the participant.

        :return: The name of this ParticipantBasic.
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """
        Sets the name of this ParticipantBasic.
        A human readable name identifying the participant.

        :param name: The name of this ParticipantBasic.
        :type: str
        """
        
        self._name = name

    @property
    def user_uri(self):
        """
        Gets the user_uri of this ParticipantBasic.
        If this participant represents a user, then this will be an URI that can be used to fetch the user.

        :return: The user_uri of this ParticipantBasic.
        :rtype: str
        """
        return self._user_uri

    @user_uri.setter
    def user_uri(self, user_uri):
        """
        Sets the user_uri of this ParticipantBasic.
        If this participant represents a user, then this will be an URI that can be used to fetch the user.

        :param user_uri: The user_uri of this ParticipantBasic.
        :type: str
        """
        
        self._user_uri = user_uri

    @property
    def user_id(self):
        """
        Gets the user_id of this ParticipantBasic.
        If this participant represents a user, then this will be the globally unique identifier for the user.

        :return: The user_id of this ParticipantBasic.
        :rtype: str
        """
        return self._user_id

    @user_id.setter
    def user_id(self, user_id):
        """
        Sets the user_id of this ParticipantBasic.
        If this participant represents a user, then this will be the globally unique identifier for the user.

        :param user_id: The user_id of this ParticipantBasic.
        :type: str
        """
        
        self._user_id = user_id

    @property
    def external_contact_id(self):
        """
        Gets the external_contact_id of this ParticipantBasic.
        If this participant represents an external contact, then this will be the globally unique identifier for the external contact.

        :return: The external_contact_id of this ParticipantBasic.
        :rtype: str
        """
        return self._external_contact_id

    @external_contact_id.setter
    def external_contact_id(self, external_contact_id):
        """
        Sets the external_contact_id of this ParticipantBasic.
        If this participant represents an external contact, then this will be the globally unique identifier for the external contact.

        :param external_contact_id: The external_contact_id of this ParticipantBasic.
        :type: str
        """
        
        self._external_contact_id = external_contact_id

    @property
    def external_organization_id(self):
        """
        Gets the external_organization_id of this ParticipantBasic.
        If this participant represents an external org, then this will be the globally unique identifier for the external org.

        :return: The external_organization_id of this ParticipantBasic.
        :rtype: str
        """
        return self._external_organization_id

    @external_organization_id.setter
    def external_organization_id(self, external_organization_id):
        """
        Sets the external_organization_id of this ParticipantBasic.
        If this participant represents an external org, then this will be the globally unique identifier for the external org.

        :param external_organization_id: The external_organization_id of this ParticipantBasic.
        :type: str
        """
        
        self._external_organization_id = external_organization_id

    @property
    def queue_id(self):
        """
        Gets the queue_id of this ParticipantBasic.
        If present, the queue id that the communication channel came in on.

        :return: The queue_id of this ParticipantBasic.
        :rtype: str
        """
        return self._queue_id

    @queue_id.setter
    def queue_id(self, queue_id):
        """
        Sets the queue_id of this ParticipantBasic.
        If present, the queue id that the communication channel came in on.

        :param queue_id: The queue_id of this ParticipantBasic.
        :type: str
        """
        
        self._queue_id = queue_id

    @property
    def group_id(self):
        """
        Gets the group_id of this ParticipantBasic.
        If present, group of users the participant represents.

        :return: The group_id of this ParticipantBasic.
        :rtype: str
        """
        return self._group_id

    @group_id.setter
    def group_id(self, group_id):
        """
        Sets the group_id of this ParticipantBasic.
        If present, group of users the participant represents.

        :param group_id: The group_id of this ParticipantBasic.
        :type: str
        """
        
        self._group_id = group_id

    @property
    def queue_name(self):
        """
        Gets the queue_name of this ParticipantBasic.
        If present, the queue name that the communication channel came in on.

        :return: The queue_name of this ParticipantBasic.
        :rtype: str
        """
        return self._queue_name

    @queue_name.setter
    def queue_name(self, queue_name):
        """
        Sets the queue_name of this ParticipantBasic.
        If present, the queue name that the communication channel came in on.

        :param queue_name: The queue_name of this ParticipantBasic.
        :type: str
        """
        
        self._queue_name = queue_name

    @property
    def purpose(self):
        """
        Gets the purpose of this ParticipantBasic.
        A well known string that specifies the purpose of this participant.

        :return: The purpose of this ParticipantBasic.
        :rtype: str
        """
        return self._purpose

    @purpose.setter
    def purpose(self, purpose):
        """
        Sets the purpose of this ParticipantBasic.
        A well known string that specifies the purpose of this participant.

        :param purpose: The purpose of this ParticipantBasic.
        :type: str
        """
        
        self._purpose = purpose

    @property
    def participant_type(self):
        """
        Gets the participant_type of this ParticipantBasic.
        A well known string that specifies the type of this participant.

        :return: The participant_type of this ParticipantBasic.
        :rtype: str
        """
        return self._participant_type

    @participant_type.setter
    def participant_type(self, participant_type):
        """
        Sets the participant_type of this ParticipantBasic.
        A well known string that specifies the type of this participant.

        :param participant_type: The participant_type of this ParticipantBasic.
        :type: str
        """
        
        self._participant_type = participant_type

    @property
    def consult_participant_id(self):
        """
        Gets the consult_participant_id of this ParticipantBasic.
        If this participant is part of a consult transfer, then this will be the participant id of the participant being transferred.

        :return: The consult_participant_id of this ParticipantBasic.
        :rtype: str
        """
        return self._consult_participant_id

    @consult_participant_id.setter
    def consult_participant_id(self, consult_participant_id):
        """
        Sets the consult_participant_id of this ParticipantBasic.
        If this participant is part of a consult transfer, then this will be the participant id of the participant being transferred.

        :param consult_participant_id: The consult_participant_id of this ParticipantBasic.
        :type: str
        """
        
        self._consult_participant_id = consult_participant_id

    @property
    def address(self):
        """
        Gets the address of this ParticipantBasic.
        The address for the this participant. For a phone call this will be the ANI.

        :return: The address of this ParticipantBasic.
        :rtype: str
        """
        return self._address

    @address.setter
    def address(self, address):
        """
        Sets the address of this ParticipantBasic.
        The address for the this participant. For a phone call this will be the ANI.

        :param address: The address of this ParticipantBasic.
        :type: str
        """
        
        self._address = address

    @property
    def ani(self):
        """
        Gets the ani of this ParticipantBasic.
        The address for the this participant. For a phone call this will be the ANI.

        :return: The ani of this ParticipantBasic.
        :rtype: str
        """
        return self._ani

    @ani.setter
    def ani(self, ani):
        """
        Sets the ani of this ParticipantBasic.
        The address for the this participant. For a phone call this will be the ANI.

        :param ani: The ani of this ParticipantBasic.
        :type: str
        """
        
        self._ani = ani

    @property
    def ani_name(self):
        """
        Gets the ani_name of this ParticipantBasic.
        The ani-based name for this participant.

        :return: The ani_name of this ParticipantBasic.
        :rtype: str
        """
        return self._ani_name

    @ani_name.setter
    def ani_name(self, ani_name):
        """
        Sets the ani_name of this ParticipantBasic.
        The ani-based name for this participant.

        :param ani_name: The ani_name of this ParticipantBasic.
        :type: str
        """
        
        self._ani_name = ani_name

    @property
    def dnis(self):
        """
        Gets the dnis of this ParticipantBasic.
        The address for the this participant. For a phone call this will be the ANI.

        :return: The dnis of this ParticipantBasic.
        :rtype: str
        """
        return self._dnis

    @dnis.setter
    def dnis(self, dnis):
        """
        Sets the dnis of this ParticipantBasic.
        The address for the this participant. For a phone call this will be the ANI.

        :param dnis: The dnis of this ParticipantBasic.
        :type: str
        """
        
        self._dnis = dnis

    @property
    def locale(self):
        """
        Gets the locale of this ParticipantBasic.
        An ISO 639 language code specifying the locale for this participant

        :return: The locale of this ParticipantBasic.
        :rtype: str
        """
        return self._locale

    @locale.setter
    def locale(self, locale):
        """
        Sets the locale of this ParticipantBasic.
        An ISO 639 language code specifying the locale for this participant

        :param locale: The locale of this ParticipantBasic.
        :type: str
        """
        
        self._locale = locale

    @property
    def wrapup_required(self):
        """
        Gets the wrapup_required of this ParticipantBasic.
        True iff this participant is required to enter wrapup for this conversation.

        :return: The wrapup_required of this ParticipantBasic.
        :rtype: bool
        """
        return self._wrapup_required

    @wrapup_required.setter
    def wrapup_required(self, wrapup_required):
        """
        Sets the wrapup_required of this ParticipantBasic.
        True iff this participant is required to enter wrapup for this conversation.

        :param wrapup_required: The wrapup_required of this ParticipantBasic.
        :type: bool
        """
        
        self._wrapup_required = wrapup_required

    @property
    def wrapup_prompt(self):
        """
        Gets the wrapup_prompt of this ParticipantBasic.
        This field controls how the UI prompts the agent for a wrapup.

        :return: The wrapup_prompt of this ParticipantBasic.
        :rtype: str
        """
        return self._wrapup_prompt

    @wrapup_prompt.setter
    def wrapup_prompt(self, wrapup_prompt):
        """
        Sets the wrapup_prompt of this ParticipantBasic.
        This field controls how the UI prompts the agent for a wrapup.

        :param wrapup_prompt: The wrapup_prompt of this ParticipantBasic.
        :type: str
        """
        allowed_values = ["mandatory", "optional", "timeout", "forcedTimeout"]
        if wrapup_prompt.lower() not in map(str.lower, allowed_values):
            # print "Invalid value for wrapup_prompt -> " + wrapup_prompt
            self._wrapup_prompt = "outdated_sdk_version"
        else:
            self._wrapup_prompt = wrapup_prompt

    @property
    def wrapup_timeout_ms(self):
        """
        Gets the wrapup_timeout_ms of this ParticipantBasic.
        Specifies how long a timed ACW session will last.

        :return: The wrapup_timeout_ms of this ParticipantBasic.
        :rtype: int
        """
        return self._wrapup_timeout_ms

    @wrapup_timeout_ms.setter
    def wrapup_timeout_ms(self, wrapup_timeout_ms):
        """
        Sets the wrapup_timeout_ms of this ParticipantBasic.
        Specifies how long a timed ACW session will last.

        :param wrapup_timeout_ms: The wrapup_timeout_ms of this ParticipantBasic.
        :type: int
        """
        
        self._wrapup_timeout_ms = wrapup_timeout_ms

    @property
    def wrapup_skipped(self):
        """
        Gets the wrapup_skipped of this ParticipantBasic.
        The UI sets this field when the agent chooses to skip entering a wrapup for this participant.

        :return: The wrapup_skipped of this ParticipantBasic.
        :rtype: bool
        """
        return self._wrapup_skipped

    @wrapup_skipped.setter
    def wrapup_skipped(self, wrapup_skipped):
        """
        Sets the wrapup_skipped of this ParticipantBasic.
        The UI sets this field when the agent chooses to skip entering a wrapup for this participant.

        :param wrapup_skipped: The wrapup_skipped of this ParticipantBasic.
        :type: bool
        """
        
        self._wrapup_skipped = wrapup_skipped

    @property
    def wrapup(self):
        """
        Gets the wrapup of this ParticipantBasic.
        Call wrap up or disposition data.

        :return: The wrapup of this ParticipantBasic.
        :rtype: Wrapup
        """
        return self._wrapup

    @wrapup.setter
    def wrapup(self, wrapup):
        """
        Sets the wrapup of this ParticipantBasic.
        Call wrap up or disposition data.

        :param wrapup: The wrapup of this ParticipantBasic.
        :type: Wrapup
        """
        
        self._wrapup = wrapup

    @property
    def monitored_participant_id(self):
        """
        Gets the monitored_participant_id of this ParticipantBasic.
        If this participant is a monitor, then this will be the id of the participant that is being monitored.

        :return: The monitored_participant_id of this ParticipantBasic.
        :rtype: str
        """
        return self._monitored_participant_id

    @monitored_participant_id.setter
    def monitored_participant_id(self, monitored_participant_id):
        """
        Sets the monitored_participant_id of this ParticipantBasic.
        If this participant is a monitor, then this will be the id of the participant that is being monitored.

        :param monitored_participant_id: The monitored_participant_id of this ParticipantBasic.
        :type: str
        """
        
        self._monitored_participant_id = monitored_participant_id

    @property
    def attributes(self):
        """
        Gets the attributes of this ParticipantBasic.
        Additional participant attributes

        :return: The attributes of this ParticipantBasic.
        :rtype: dict(str, str)
        """
        return self._attributes

    @attributes.setter
    def attributes(self, attributes):
        """
        Sets the attributes of this ParticipantBasic.
        Additional participant attributes

        :param attributes: The attributes of this ParticipantBasic.
        :type: dict(str, str)
        """
        
        self._attributes = attributes

    @property
    def calls(self):
        """
        Gets the calls of this ParticipantBasic.


        :return: The calls of this ParticipantBasic.
        :rtype: list[CallBasic]
        """
        return self._calls

    @calls.setter
    def calls(self, calls):
        """
        Sets the calls of this ParticipantBasic.


        :param calls: The calls of this ParticipantBasic.
        :type: list[CallBasic]
        """
        
        self._calls = calls

    @property
    def callbacks(self):
        """
        Gets the callbacks of this ParticipantBasic.


        :return: The callbacks of this ParticipantBasic.
        :rtype: list[CallbackBasic]
        """
        return self._callbacks

    @callbacks.setter
    def callbacks(self, callbacks):
        """
        Sets the callbacks of this ParticipantBasic.


        :param callbacks: The callbacks of this ParticipantBasic.
        :type: list[CallbackBasic]
        """
        
        self._callbacks = callbacks

    @property
    def chats(self):
        """
        Gets the chats of this ParticipantBasic.


        :return: The chats of this ParticipantBasic.
        :rtype: list[ConversationChat]
        """
        return self._chats

    @chats.setter
    def chats(self, chats):
        """
        Sets the chats of this ParticipantBasic.


        :param chats: The chats of this ParticipantBasic.
        :type: list[ConversationChat]
        """
        
        self._chats = chats

    @property
    def cobrowsesessions(self):
        """
        Gets the cobrowsesessions of this ParticipantBasic.


        :return: The cobrowsesessions of this ParticipantBasic.
        :rtype: list[Cobrowsesession]
        """
        return self._cobrowsesessions

    @cobrowsesessions.setter
    def cobrowsesessions(self, cobrowsesessions):
        """
        Sets the cobrowsesessions of this ParticipantBasic.


        :param cobrowsesessions: The cobrowsesessions of this ParticipantBasic.
        :type: list[Cobrowsesession]
        """
        
        self._cobrowsesessions = cobrowsesessions

    @property
    def emails(self):
        """
        Gets the emails of this ParticipantBasic.


        :return: The emails of this ParticipantBasic.
        :rtype: list[Email]
        """
        return self._emails

    @emails.setter
    def emails(self, emails):
        """
        Sets the emails of this ParticipantBasic.


        :param emails: The emails of this ParticipantBasic.
        :type: list[Email]
        """
        
        self._emails = emails

    @property
    def screenshares(self):
        """
        Gets the screenshares of this ParticipantBasic.


        :return: The screenshares of this ParticipantBasic.
        :rtype: list[Screenshare]
        """
        return self._screenshares

    @screenshares.setter
    def screenshares(self, screenshares):
        """
        Sets the screenshares of this ParticipantBasic.


        :param screenshares: The screenshares of this ParticipantBasic.
        :type: list[Screenshare]
        """
        
        self._screenshares = screenshares

    @property
    def social_expressions(self):
        """
        Gets the social_expressions of this ParticipantBasic.


        :return: The social_expressions of this ParticipantBasic.
        :rtype: list[SocialExpression]
        """
        return self._social_expressions

    @social_expressions.setter
    def social_expressions(self, social_expressions):
        """
        Sets the social_expressions of this ParticipantBasic.


        :param social_expressions: The social_expressions of this ParticipantBasic.
        :type: list[SocialExpression]
        """
        
        self._social_expressions = social_expressions

    @property
    def videos(self):
        """
        Gets the videos of this ParticipantBasic.


        :return: The videos of this ParticipantBasic.
        :rtype: list[Video]
        """
        return self._videos

    @videos.setter
    def videos(self, videos):
        """
        Sets the videos of this ParticipantBasic.


        :param videos: The videos of this ParticipantBasic.
        :type: list[Video]
        """
        
        self._videos = videos

    @property
    def evaluations(self):
        """
        Gets the evaluations of this ParticipantBasic.


        :return: The evaluations of this ParticipantBasic.
        :rtype: list[Evaluation]
        """
        return self._evaluations

    @evaluations.setter
    def evaluations(self, evaluations):
        """
        Sets the evaluations of this ParticipantBasic.


        :param evaluations: The evaluations of this ParticipantBasic.
        :type: list[Evaluation]
        """
        
        self._evaluations = evaluations

    @property
    def screen_recording_state(self):
        """
        Gets the screen_recording_state of this ParticipantBasic.
        The current screen recording state for this participant.

        :return: The screen_recording_state of this ParticipantBasic.
        :rtype: str
        """
        return self._screen_recording_state

    @screen_recording_state.setter
    def screen_recording_state(self, screen_recording_state):
        """
        Sets the screen_recording_state of this ParticipantBasic.
        The current screen recording state for this participant.

        :param screen_recording_state: The screen_recording_state of this ParticipantBasic.
        :type: str
        """
        allowed_values = ["requested", "active", "paused", "stopped", "error"]
        if screen_recording_state.lower() not in map(str.lower, allowed_values):
            # print "Invalid value for screen_recording_state -> " + screen_recording_state
            self._screen_recording_state = "outdated_sdk_version"
        else:
            self._screen_recording_state = screen_recording_state

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

