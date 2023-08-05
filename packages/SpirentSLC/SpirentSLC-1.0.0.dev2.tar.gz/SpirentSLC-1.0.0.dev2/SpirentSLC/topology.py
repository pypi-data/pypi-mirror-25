# ****************       BEGIN-STANDARD-COPYRIGHT      ***************
#
# Copyright (c) 2017, Spirent Communications.
#
# All rights reserved. Proprietary and confidential information of Spirent Communications.
#
#  ***************        END-STANDARD-COPYRIGHT       ***************

"""Topology class and necessary tools."""

from .session_profile import SessionProfile

class Topology():
    """Topology representation.

    Provide a list of devices with sessions
    """

    def __init__(self, project, uri, devices):
        """Initiates a new topology.

        Arguments:
        protocol_socket -- an instance of ProtocolSocket. It must be connected by the time open() is called.
        agent_type -- agent type (local/itest/velocity)
        uri -- topology URI, e.g. project://my_project/topologies/ServerAndPC.tbml
        devices -- map of device names to assigned sessions
        """

        self._project = project
        self._uri = uri
        self._devices = dict((dev_name, Device(self, dev_name, devices[dev_name])) for dev_name in devices.keys())

    def protocol(self):
        return self._project.protocol()

    def agent_type(self):
        return self._project.agent_type

    def uri(self):
        return self._uri

    def __getitem__(self, key):
        return self._devices.get(key)

    def __getattr__(self, key):
        ret = self[key]
        if ret == None:
            raise AttributeError(key)
        return ret

class Device():

    def __init__(self, topology, name, sessions):
        self._topology = topology
        self._name = name
        self._sessions = dict((session, self._create_session(session)) for session in sessions)

    def _create_session(self, session):
        session_uri = self._topology.uri() + '#' + self.name() + ':' + session
        return SessionProfile(self.protocol(), self.agent_type(), session_uri)

    def protocol(self):
        return self._topology.protocol()

    def agent_type(self):
        return self._topology.agent_type()

    def name(self):
        return self._name

    def __getitem__(self, key):
        return self._sessions.get(key)

    def __getattr__(self, key):
        ret = self[key]
        if ret == None:
            raise AttributeError(key)
        return ret
