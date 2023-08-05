#!/usr/bin/env python
# vim: set fileencoding=utf-8 :
# Pavel Korshunov <pavel.korshunov@idiap.ch>
# Thu 6 Oct 20:43:22 2016

"""Table models and functionality for the AVSpoof DB.
"""

import os
from sqlalchemy import Table, Column, Integer, String, ForeignKey
from bob.db.base.sqlalchemy_migration import Enum, relationship
from sqlalchemy.orm import backref
from sqlalchemy.ext.declarative import declarative_base
import bob

import bob.db.base

Base = declarative_base()


class Client(Base):
    """Database clients, marked by an integer identifier and the set they belong
    to"""

    __tablename__ = 'client'

    gender_choices = ('male', 'female')
    """Male or female speech"""

    group_choices = ('train', 'dev', 'eval')
    """Possible groups to which clients may belong to"""

    id = Column(Integer, primary_key=True)
    """Key identifier for clients"""

    gender = Column(Enum(*gender_choices))
    """The gender of the subject"""

    group = Column(Enum(*group_choices))
    """Group (or set) to which this client belongs to"""

    def __init__(self, id, gender, group):
        self.id = id
        self.gender = gender
        self.group = group

    def __repr__(self):
        return "Client('%d', '%s', '%s')" % (self.id, self.gender, self.group)


class File(Base, bob.db.base.File):
    """Generic file container"""

    __tablename__ = 'file'

    recording_device_choices = ('laptop', 'iphone3gs', 'samsungs3')
    """List of devices used to record audio samples"""

    session_choices = ('sess1', 'sess2', 'sess3', 'sess4')
    """List of sessions during which audio samples were recorded"""

    speech_choices = ('pass', 'read', 'free')
    """Types of speech subjects were asked to say,
    pass - password, read - short text, free - 2-5 mints free speech"""

    # types of the possible recorded attack data (what devices recorded the data)
    attack_data_choices = ('undefined', 'laptop', 'iphone3gs', 'samsungs3', 'ss', 'vc')
    """Types of attacks data, i.e., what medium was used to create the attacks"""

    attack_device_choices = ('undefined', 'laptop', 'hqspeaker', 'iphone3gs', 'samsungs3', 'iphone6s')
    """Types of devices that used to playback the attack data"""

    asv_device_choices = ('undefined', 'laptop', 'iphone3gs', 'samsungs3')
    """Types of devices that are running the ASV system, i.e., the devices that are being attacked"""

    environment_choices = ('undefined', 'r106', 'r107', 'seboffice')
    """Types of environments where the attacks were recorded. 'r107' and 'seboffice' are small offices
    and 'r106' is a conference room"""

    purpose_choices = ('real', 'attack')
    """Possible purpose of this file"""

    id = Column(Integer, primary_key=True)
    """Key identifier for files"""

    path = Column(String(200), unique=True)
    """The (unique) path to this file inside the database"""

    recording_device = Column(Enum(*recording_device_choices))
    """The device using which the data for this file was taken"""

    session = Column(Enum(*session_choices))
    """The session during which the data for this file was taken"""

    speech = Column(Enum(*speech_choices))
    """The speech type of the data for this file was taken"""

    attack_data = Column(Enum(*attack_data_choices))
    """The type of attack data and how it was created"""

    attack_device = Column(Enum(*attack_device_choices))
    """The attack device, which was used to playback attacks"""

    asv_device = Column(Enum(*asv_device_choices ))
    """The device which is running the ASV system, i.e., the device that is being attacked"""

    environment = Column(Enum(*environment_choices))
    """The environment in which the data was recorded"""

    purpose = Column(Enum(*purpose_choices))
    """Purpose of this file"""

    client_id = Column(Integer, ForeignKey('client.id'))  # for SQL
    """The client identifier to which this file is bound to"""

    # for Python
    client = relationship(Client, backref=backref('files', order_by=id))
    """A direct link to the client object that this file belongs to"""

    def __init__(self, client, path, recording_device, session, speech, attack_data, attack_device, 
                 asv_device, environment, purpose):
        bob.db.base.File.__init__(self, path=path)
        self.client = client
        self.recording_device = recording_device
        self.session = session
        self.speech = speech
        self.attack_data = attack_data
        self.attack_device = attack_device
        self.asv_device = asv_device
        self.environment = environment
        self.purpose = purpose


    def audiofile(self, directory=None):
        """Returns the path to the database audio file for this object

        Keyword parameters:

        directory
            An optional directory name that will be prefixed to the returned result.

        Returns a string containing the video file path.
        """

        return self.make_path(directory, '.wav')

    def is_real(self):
        """Returns True if this file belongs to a real access, False otherwise"""

        return self.purpose == 'real'

    def is_attack(self):
        """Returns True if this file an attack, False otherwise"""

        return self.purpose == 'attack'

    def get_attack(self):
        """Returns the full attack bame raise"""
        if not self.is_attack():
            raise RuntimeError("%s is not an attack" % self)
        return self.environment + '-' + self.asv_device + '-' + self.attack_data + '-' + self.attack_device


class Protocol(Base):
    """AVSpoof general protocol"""

    __tablename__ = 'protocol'

    #    purpose_choices = ('antispoofing', 'verification')
    #    """What kind of protocol is it? It's true purpose"""

    id = Column(Integer, primary_key=True)
    """Unique identifier for the protocol (integer)"""

    name = Column(String(20), unique=True)
    """Protocol name"""

    #    purpose = Column(Enum(*purpose_choices))
    #    """It can one of two purposes"""


    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return "Protocol('%s')" % self.name


class ProtocolFiles(Base):
    """Database clients, marked by an integer identifier and the set they belong
    to"""

    __tablename__ = 'protocolfiles'

    id = Column(Integer, primary_key=True)
    """Key identifier for Protocols"""

    protocol_id = Column(String, ForeignKey('protocol.id'))  # for SQL
    """The protocol identifier that the file is linked to"""

    # for Python
    protocol = relationship(Protocol, backref=backref('protocolfiles', order_by=id))
    """A direct link to the protocol object that refers to the given file"""

    file_id = Column(String, ForeignKey('file.id'))  # for SQL
    """The file id that the protocol references"""

    # for Python
    file = relationship(File, backref=backref('protocolfiles', order_by=id))
    """A direct link to the file object that the protocol references"""


    def __init__(self, protocol, file):
        self.protocol = protocol
        self.file = file

    def __repr__(self):
        return "ProtocolFiles('%s, %s')" % (self.protocol_id, self.file_id)
