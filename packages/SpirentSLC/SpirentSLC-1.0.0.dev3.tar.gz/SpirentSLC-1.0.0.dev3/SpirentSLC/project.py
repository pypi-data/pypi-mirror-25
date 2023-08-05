# ****************       BEGIN-STANDARD-COPYRIGHT      ***************
#
# Copyright (c) 2017, Spirent Communications.
#
# All rights reserved. Proprietary and confidential information of Spirent Communications.
#
#  ***************        END-STANDARD-COPYRIGHT       ***************

"""Project class and necessary tools."""

from .session_profile import SessionProfile
from .topology import Topology

class Project(object):
    """This class represents a single project.

    Objects of this class should not be created directly, but rather obtained from an SLC object.
    """

    def __init__(self, project_name, protocol_socket, agent_type):
        self._project_name = project_name
        self._protosock = protocol_socket
        self.agent_type = agent_type

        self._update_agent_type()

        self._session_profiles = dict()
        self._topologies = dict()
        self._parameter_files = list()
        self._response_maps = list()

    def open(self):
        """
        Parses itar and init a list of all the usable topologies and session profiles in the project.

        Returns self for convenience.
        """

        ret = self._protosock.query_project(self._project_name, parameter_file=True, response_map=True)
        for session_profile in ret.sessionProfiles:
            name = self._resource_name(session_profile, '_ffsp')
            uri = 'project://%s/%s' %(self._project_name, session_profile)
            self._session_profiles[name] = SessionProfile(self._protosock, self.agent_type, uri)

        for topology in ret.topologies:
            name = self._resource_name(topology.name, '_tbml')
            topology_uri = 'project://%s/%s' %(self._project_name, topology.name)
            devices = dict((self.python_name(device.name), device.sessions) for device in topology.devices)
            self._topologies[name] = Topology(self, topology_uri, devices)

        self._parameter_files = [self._resource_name(name, '_ffpt') for name in ret.parameterFiles]
        self._response_maps = [self._resource_name(name, '_ffrm') for name in ret.responseMaps]

        return self

    def protocol(self):
        return self._protosock

    def _resource_name(self, itest_name, suffix):
        pos_from = itest_name.rfind('/') + 1
        pos_to = itest_name.rfind('.')
        return self.python_name(itest_name[pos_from:pos_to] + suffix)

    def python_name(self, name):
        # TODO: All spaces in the name of a project or any other characters that are not legal in a Python identifier should be replaced by underscores
        # TODO: duplicates after replacing
        return name

    def _update_agent_type(self):
        """ Detect agent type based on init packet send by server """
        pass

    def list(self, parameter_file=False, response_map=False):
        """
        Returns a list of names of all the usable topologies and session profiles in the project.

        Example:
            proj.list()
            ==> ['dut1_ffsp', 'lab1_setup_tbml']
        """
        result = list(self._session_profiles.keys()) + list(self._topologies.keys())

        if parameter_file:
            result = result + list(self._parameter_files)

        if response_map:
            result = result + list(self._response_maps)

        return result

    def __getitem__(self, key):
        """
            Sessions are opened either directly on a session profile or local topology.

            Examples:
                s1 = proj.dut1_ffsp.open()
                s1 = proj.rest_session_ffsp.open(url='https://my_site.my_domain.com', accept_all_cookies=True)
                s1 = proj.rest_session_ffsp.open(parameter_file=proj.main_setup_ffpt)
                s1 = proj.rest_session_ffsp.open(properties={'authentication.authentication': 'Basic', 'authentication.user': 'me', 'authentication.password': 'totes_secret!'})

            Opening native sessions:
                s1 = slc.sessions.ssh.open(ip_address='10.20.30.40')
        """
        profile = self._session_profiles.get(key)
        if profile:
            return profile

        topology = self._topologies.get(key)
        if topology:
            return topology

        return None

    def __getattr__(self, key):
        ret = self[key]
        if ret == None:
            raise AttributeError(key)
        return ret
