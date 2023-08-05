#!/usr/bin/env python
# vim: set fileencoding=utf-8 :
# Pavel Korshunov <pavel.korshunov@idiap.ch>
# Thu 6 Oct 21:43:22 2016

"""This module provides the Dataset interface allowing the user to query the
voicepa attack database in the most obvious ways.
"""

from bob.db.base import utils
from .models import File, Client, Protocol, ProtocolFiles
from .driver import Interface

import bob.db.base

INFO = Interface()

SQLITE_FILE = INFO.files()[0]


class Database(bob.db.base.SQLiteDatabase):
    """The dataset class opens and maintains a connection opened to the Database.

    It provides many different ways to probe for the characteristics of the data
    and for the data itself inside the database.
    """

    def __init__(self, original_directory=None, original_extension=None):
        # opens a session to the database - keep it open until the end
        super(Database, self).__init__(SQLITE_FILE, File,
                                       original_directory, original_extension)

    def objects(self, protocol='grandtest', attack_data=File.attack_data_choices,
                groups=Client.group_choices, cls=('real',), recording_devices=File.recording_device_choices,
                sessions=File.session_choices, gender=Client.gender_choices, attack_devices=File.attack_device_choices,
                asv_devices=File.asv_device_choices, environments=File.environment_choices, clients=None):
        """Returns a list of unique :py:class:`File` objects for the specific query by the user


        Parameters:

          protocol (str): The protocol for the attack. one of the ones returned
            by protocols(). if you set this parameter to an empty string or the
            value none, we reset it to the default, "grandtest".

          groups (str): One of the protocol subgroups of data as returned by
            groups() or a tuple with several of them.  if you set this
            parameter to an empty string or the value none, we reset it to the
            default which is to get all.

          cls (str): Either ``attack``, ``real``, ``enroll``, ``probe``, or a
            combination of those (in a tuple). defines the class of data to be
            retrieved. If you set this parameter to an empty string or the
            value none, we reset it to the default, (``real``).

          attack_data (str): One of the valid attack types as returned by
            ``models.attack.attack_datas()`` or all, as a tuple.  if you set
            this parameter to an empty string or the value none, we reset it to
            the default, which is to get all.

          asv_devices (str): One or more devices that are running automatic
            verification system, i.e., these are the devices that are being
            attacked.

          attack_devices (str): One or more devices that are used to play the
            presentation attack.

          environments (str): One or more locations (rooms) where the attacks
            were recorded.

          recording_devices (str): One of the recording_devices used to record
            the data (laptop, phone1, and phone2) or a combination of them (in
            a tuple), which is also the default.

          clients (int): If set, should be a single integer or a list of
            integers that define the client identifiers from which files should
            be retrieved. if omitted, set to none or an empty list, then data
            from all clients is retrieved.


        Returns:

          list of :py:class:`File`: Corresponds to the selected objects

        """

        self.assert_validity()

        # check if groups set are valid
        VALID_GROUPS = self.groups()
        groups = self.check_parameters_for_validity(
            groups, "group", VALID_GROUPS, None)

        # check if groups set are valid
        VALID_GENDER = self.genders()
        gender = self.check_parameters_for_validity(
            gender, "gender", VALID_GENDER, None)

        # check if supports set are valid
        VALID_SUPPORTS = self.attack_datas()
        attack_data = self.check_parameters_for_validity(
            attack_data, "attack_data", VALID_SUPPORTS, None)

        # check if supports set are valid
        VALID_ATTACKDEVICES = self.attack_devices()
        attack_devices = self.check_parameters_for_validity(
            attack_devices, "attack_device", VALID_ATTACKDEVICES, None)

        # check if supports set are valid
        VALID_ASVDEVICES = self.asv_devices()
        asv_devices = self.check_parameters_for_validity(
            asv_devices, "asv_device", VALID_ASVDEVICES, None)

        # check if supports set are valid
        VALID_ENVIRONMENTS = self.environments()
        environments = self.check_parameters_for_validity(
            environments, "environment", VALID_ENVIRONMENTS, None)

        # by default, do NOT grab enrollment data from the database
        VALID_CLASSES = ('real', 'attack', 'enroll', 'probe')
        cls = self.check_parameters_for_validity(
            cls, "class", VALID_CLASSES, VALID_CLASSES)

        # check protocol validity
        VALID_PROTOCOLS = [k.name for k in self.protocols()]
        protocol = self.check_parameters_for_validity(
            protocol, "protocol", VALID_PROTOCOLS, ('grandtest',))

        # checks client identity validity
        VALID_CLIENTS = [k.id for k in self.clients()]
        clients = self.check_parameters_for_validity(
            clients, "client", VALID_CLIENTS, None)

        # checks if the device is valid
        VALID_DEVICES = self.devices()
        recording_devices = self.check_parameters_for_validity(
            recording_devices, "recording_device", VALID_DEVICES, None)

        # checks if the device is valid
        VALID_SESSIONS = self.sessions()
        sessions = self.check_parameters_for_validity(
            sessions, "session", VALID_SESSIONS, None)

        # now query the database
        retval = []

        # first, check the real data
        purpose = ('real',)
        if 'real' in cls:  # the whole real data
            # init the query
            q = self.m_session.query(File).join(ProtocolFiles).join(
                (Protocol, ProtocolFiles.protocol)).join(Client)
            if groups:
                q = q.filter(Client.group.in_(groups))
            if clients:
                q = q.filter(Client.id.in_(clients))
            if gender:
                q = q.filter(Client.gender.in_(gender))
            if recording_devices:
                q = q.filter(File.recording_device.in_(recording_devices))
            if sessions:
                q = q.filter(File.session.in_(sessions))
            if attack_data:
                q = q.filter(File.attack_data.in_(attack_data))
            if attack_devices:
                q = q.filter(File.attack_device.in_(attack_devices))
            if asv_devices:
                q = q.filter(File.asv_device.in_(asv_devices))
            if environments:
                q = q.filter(File.environment.in_(environments))
            q = q.filter(File.purpose.in_(purpose))
            q = q.filter(Protocol.name.in_(protocol))
            q = q.order_by(File.path)
            retval += list(q)

        # if we need enroll data (a small subset of real data)
        if 'enroll' in cls:
            # init the query
            q = self.m_session.query(File).join(ProtocolFiles).join(
                (Protocol, ProtocolFiles.protocol)).join(Client)
            from sqlalchemy import and_
            # only data from sess1 and laptop is in enrollment
            q = q.filter(and_(File.recording_device ==
                              'laptop', File.session == 'sess1'))
            if groups:
                q = q.filter(Client.group.in_(groups))
            if clients:
                q = q.filter(Client.id.in_(clients))
            if gender:
                q = q.filter(Client.gender.in_(gender))
            if recording_devices:
                q = q.filter(File.recording_device.in_(recording_devices))
            if sessions:
                q = q.filter(File.session.in_(sessions))
            if attack_data:
                q = q.filter(File.attack_data.in_(attack_data))
            if attack_devices:
                q = q.filter(File.attack_device.in_(attack_devices))
            if asv_devices:
                q = q.filter(File.asv_device.in_(asv_devices))
            if environments:
                q = q.filter(File.environment.in_(environments))
            q = q.filter(File.purpose.in_(purpose))
            q = q.filter(Protocol.name.in_(protocol))
            q = q.order_by(File.path)
            retval += list(q)

        # if we need probe data (a large subset of real data)
        if 'probe' in cls:
            # init the query
            q = self.m_session.query(File).join(ProtocolFiles).join(
                (Protocol, ProtocolFiles.protocol)).join(Client)
            from sqlalchemy import or_
            # all data except the one from sess1 and laptop
            q = q.filter(or_(File.recording_device !=
                             'laptop', File.session != 'sess1'))
            if groups:
                q = q.filter(Client.group.in_(groups))
            if clients:
                q = q.filter(Client.id.in_(clients))
            if gender:
                q = q.filter(Client.gender.in_(gender))
            if recording_devices:
                q = q.filter(File.recording_device.in_(recording_devices))
            if sessions:
                q = q.filter(File.session.in_(sessions))
            if attack_data:
                q = q.filter(File.attack_data.in_(attack_data))
            if attack_devices:
                q = q.filter(File.attack_device.in_(attack_devices))
            if asv_devices:
                q = q.filter(File.asv_device.in_(asv_devices))
            if environments:
                q = q.filter(File.environment.in_(environments))
            q = q.filter(File.purpose.in_(purpose))
            q = q.filter(Protocol.name.in_(protocol))
            q = q.order_by(File.path)
            retval += list(q)

        if 'attack' in cls:
            purpose = ('attack',)
            # init the query
            q = self.m_session.query(File).join(ProtocolFiles).join(
                (Protocol, ProtocolFiles.protocol)).join(Client)
            # if both enroll and probe data is requested, then do not do
            # anything
            if groups:
                q = q.filter(Client.group.in_(groups))
            if clients:
                q = q.filter(Client.id.in_(clients))
            if gender:
                q = q.filter(Client.gender.in_(gender))
            if attack_data:
                q = q.filter(File.attack_data.in_(attack_data))
            if attack_devices:
                q = q.filter(File.attack_device.in_(attack_devices))
            if asv_devices:
                q = q.filter(File.asv_device.in_(asv_devices))
            if environments:
                q = q.filter(File.environment.in_(environments))
            if recording_devices:
                q = q.filter(File.recording_device.in_(recording_devices))
            if sessions:
                q = q.filter(File.session.in_(sessions))
            q = q.filter(File.purpose.in_(purpose))
            q = q.filter(Protocol.name.in_(protocol))
            q = q.order_by(File.path)
            retval += list(q)

        return retval

    def clients(self, groups=None, protocol=None, gender=None):
        """Returns a list of Clients for the specific query by the user.
        If no parameters are specified - return all clients.

        Keyword Parameters:

        protocol
            An voicePA protocol.

        groups
            The groups to which the subjects attached to the models belong ('train', 'dev', 'eval')

        gender
            The gender to consider ('male', 'female')

        Returns: A list containing the ids of all models belonging to the given group.
        """
        if protocol == '.':
            protocol = None
        protocol = self.check_parameters_for_validity(
            protocol, "protocol", self.protocol_names(), None)
        groups = self.check_parameters_for_validity(
            groups, "group", self.groups(), self.groups())
        gender = self.check_parameters_for_validity(
            gender, "gender", self.genders(), None)

        retval = []
        if groups:
            q = self.m_session.query(Client).filter(Client.group.in_(groups))
            if gender:
                q = q.filter(Client.gender.in_(gender))

            q = q.order_by(Client.id)
            retval += list(q)

        return retval

    def has_client_id(self, id):
        """Returns True if we have a client with a certain integer identifier"""

        self.assert_validity()
        return self.m_session.query(Client).filter(Client.id == id).count() != 0

    def client(self, id):
        """Returns the Client object in the database given a certain id. Raises
        an error if that does not exist."""

        return self.m_session.query(Client).filter(Client.id == id).one()

    def protocols(self):
        """Returns all protocol objects.
        """

        self.assert_validity()
        return list(self.m_session.query(Protocol))

    def protocol_names(self):
        """Returns all registered protocol names"""

        l = self.protocols()
        retval = [str(k.name) for k in l]
        return retval

    def has_protocol(self, name):
        """Tells if a certain protocol is available"""

        self.assert_validity()
        return self.m_session.query(Protocol).filter(Protocol.name == name).count() != 0

    def protocol(self, name):
        """Returns the protocol object in the database given a certain name. Raises
        an error if that does not exist."""

        self.assert_validity()
        return self.m_session.query(Protocol).filter(Protocol.name == name).one()

    def groups(self):
        """Returns the names of all registered groups"""

        return Client.group_choices

    def genders(self):
        """Returns the list of genders"""

        return Client.gender_choices

    def devices(self):
        """Returns devices used in the database"""

        return File.recording_device_choices

    def sessions(self):
        """Returns sessions used in the database"""

        return File.session_choices

    def attack_datas(self):
        """Returns attack supports available in the database"""

        return File.attack_data_choices

    def attack_devices(self):
        """Returns attack devices available in the database"""

        return File.attack_device_choices

    def asv_devices(self):
        """Returns from the database the devices that were attacked (run ASV)"""

        return File.asv_device_choices

    def environments(self):
        """Returns from database the environments where attacks were recorded"""

        return File.environment_choices

    def file_speech(self):
        """Returns attack sample types available in the database"""

        return File.speech_choices
