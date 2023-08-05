# ****************       BEGIN-STANDARD-COPYRIGHT      ***************
#
# Copyright (c) 2017, Spirent Communications.
#
# All rights reserved. Proprietary and confidential information of Spirent Communications.
#
#  ***************        END-STANDARD-COPYRIGHT       ***************

"""Main SLC library API entry point."""

import os
import tempfile

from sys import platform as _platform
from . import config as cfg
from .internal.protocol import ProtocolSocket
from .project import Project

try:
    import subprocess
    from subprocess import DEVNULL # Python 3.x
except ImportError:
    DEVNULL = open(os.devnull, 'wb')

_DEBUG_SLC = False

try:
    from urlparse import urlparse
except ImportError:
    # in Python 3, urlparse renamed to urllib.parse
    # pylint: disable=no-name-in-module,import-error
    from urllib.parse import urlparse

# pylint: disable=invalid-name
_SLC_instance = None

class SLCError(Exception):
    """General exception indicating various types of SLC errors."""

    pass

class _SLC(object):
    """A private class to represent SLC.

    Objects of this class should not be created directly, but rather obtained via the init() function below.
    """

    def __init__(self, isLocal, host, port, agent_path, itar_path):
        global _SLC_instance

        if _SLC_instance:
            raise SLCError('Multiple instances of SLC are not supported')

        _SLC_instance = self

        self._agent_path = agent_path

        if isLocal:
            if _platform == "darwin":
                # we need to check path is correct for macos
                if not agent_path.endswith('/Contents/Eclipse'):
                    agent_path += '/Contents/Eclipse/'

            agent_jre = agent_path + os.sep + 'jre'
            # env = {
            #     'VELOCITY_AGENT_HOME': agent_path,
            # }

            java_bin = None
            tmp_param = '-Djava.io.tmpdir=' + tempfile.gettempdir()
            if _platform == "linux" or _platform == "linux2":
                # linux
                java_bin = agent_jre +'/bin/java'
            elif _platform == "darwin":
                # MAC OS X
                java_bin = agent_jre +'/Contents/Home/jre/bin/java'
            elif _platform == "win32":
                # Windows
                java_bin = agent_jre +'\\bin\\java'
            elif _platform == "win64":
                # Windows 64-bit
                java_bin = agent_jre +'\\bin\\java'

            self.agent_args = [java_bin,
                          '-Xmx512M',
                          '-Dfile.encoding=UTF-8',
                          '-XX:MaxMetaspaceSize=128M',
                          '-Dorg.eclipse.emf.ecore.plugin.EcorePlugin.doNotLoadResourcesPlugin=true',
                          '-Djava.awt.headless=true',
                          tmp_param,
                          '-jar', agent_path + os.sep + 'plugins' + os.sep +
                            'org.eclipse.equinox.launcher_1.4.0.v20161219-1356.jar',
                          '-consoleLog', '-data', '@no',
                          '--agentVelocityHost', host,
                          '--sfAgentServerPort', str(port),
                          '--listeningMode',
                          '--sfAgentDisableSslValidation']

            if itar_path != None:
                print('add itar_path:', itar_path)
                self.agent_args.append('--itar')
                self.agent_args.append(itar_path)

            if _DEBUG_SLC:
                print("Launching agent with args: ", ' '.join(agent_args))
            self._agent_process = subprocess.Popen(
                self.agent_args, stdin=None, stderr=subprocess.STDOUT, stdout=DEVNULL, shell=False)
            self._agent_type = "local"
        else:
            self._agent_process = None

            # agent type will be updated based on information retrieved from agent itself.
            self._agent_type = 'remote'

        self._protosock = ProtocolSocket(host, port, cfg.get_agent_start_timeout())

        self._projects = dict()

        for project in self._protosock.list_projects():
            # TODO: All spaces in the name of a project or any other characters that are not legal in a Python identifier should be replaced by underscores
            # TODO: duplicates after replacing
            py_project_name = project
            self._projects[py_project_name] = Project(project, self._protosock, self._agent_type)

    def list(self):
        """Returns a list of names of all projects."""
        return self._projects.keys()

    def open(self, projectName):
        """Opens a project.

        Arguments:
        projectName -- project name.

        Returns the project. If project name is None, empty or not present in the projects' list, raises ValueError.
        """
        return self._projects[projectName].open()

    def close(self):
        """Closes SLC.

        Underlying connections are dropped (if any) and processes are terminated (if any).
        """
        global _SLC_instance
        _SLC_instance = None

        protosock = self._protosock
        self._protosock = None
        protosock.close()

        p = self._agent_process
        self._agent_process = None
        if p:
            p.kill()

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.close()

def _parse_host_port(host_port):
    """Parse a "host:port" string and returns (host, port) pair

    Arguments:
    host_port -- a string of the "host:port" format

    Return (host, port) pair. If the given string does not comply with the pattern "host:port", one or both components
    of the pair returned may be None.
    """

    url = urlparse('http://' + host_port)       # we need some schema for urlparse to work
    return (url.hostname, url.port)

def init(host=None, password=None, agent_path=None, itar_path=None):
    """Initialises and returns an SLC object.

    Arguments:
    host -- SLC host to connect to in a form of 'host:port' string. Env var: SPIRENT_SLC_HOST. Default: 'local', which
            means the library is to run its own instance of the Velocity agent.

    password -- password to connect to SLC. Env var: SPIRENT_SLC_PASSWORD. Default: no password.

    agent_path -- path to the 'velocity-agent' executable. Env var: SPIRENT_SLC_AGENT_PATH.
                  Default: find 'velocity-agent' in PATH.
                  If the agent is not found, and 'host' specifies 'local', SLCError is raised.
    itar_path -- path to location of local itar's. will use ITAR_PATH environment variable if not specified.
                In case of relative path, current working directory will be used to construct absolute path.

    All arguments are optional. If something is not specified, the value is taken from the respective environment
    variable. If the respective environment variable is not set, the respective default value is used.

    Returns an SLC object.

    Only one SLC object (or none at all) may exist at a time. First time this function is called, it is created.
    After that, unless the object is closed via it's close() method, the same object is returned.
    If the returned object gets closed, the next init() call will create a new one.
    """

    if _SLC_instance:
        return _SLC_instance

    if not host:
        host = cfg.get_agent_host_port()

    isLocal = host == 'local'
    if isLocal:
        host = cfg.get_local_agent_host_port()

    host, port = _parse_host_port(host)

    if not agent_path:
        agent_path = cfg.get_agent_path()
    if not agent_path and isLocal:
        raise SLCError('agentPath is not specified and SPIRENT_SLC_AGENT_PATH environment variable is not set')

    if itar_path is None:
        itar_path = cfg.get_itar_path()
    else:
        # Check if it is relative path we need to add current script directory
        if not os.path.isabs(itar_path):
            itar_path = os.getcwd() + os.sep + itar_path

    return _SLC(isLocal, host, port, agent_path, itar_path)
