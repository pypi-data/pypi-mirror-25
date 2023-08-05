# ****************       BEGIN-STANDARD-COPYRIGHT      ***************
#
# Copyright (c) 2017, Spirent Communications.
#
# All rights reserved. Proprietary and confidential information of Spirent Communications.
#
#  ***************        END-STANDARD-COPYRIGHT       ***************

"""Builtin sessions provider."""

from .session_profile import SessionProfile

class BuiltinSession():
    """Provide an access to builtin sessions"""

    def __init__(self, protocol_socket, agent_type):
        self._protosock = protocol_socket
        self._agent_type = agent_type

        self.agilent = SessionProfile(self._protosock, self._agent_type, 'application://com.fnfr.svt.applications.agilent')
        self.cmd = SessionProfile(self._protosock, self._agent_type, 'application://com.fnfr.svt.applications.cmd')
        self.http = SessionProfile(self._protosock, self._agent_type, 'application://com.fnfr.svt.applications.http')
        self.ixload = SessionProfile(self._protosock, self._agent_type, 'application://com.fnfr.svt.applications.ixia.ixload')
        self.ixnetwork = SessionProfile(self._protosock, self._agent_type, 'application://com.fnfr.svt.applications.ixia.ixnetwork')
        self.ixiaTraffic = SessionProfile(self._protosock, self._agent_type, 'application://com.fnfr.svt.applications.ixiaTraffic')
        self.swing = SessionProfile(self._protosock, self._agent_type, 'application://com.fnfr.svt.applications.java.swing')
        self.mail = SessionProfile(self._protosock, self._agent_type, 'application://com.fnfr.svt.applications.mail')
        self.process = SessionProfile(self._protosock, self._agent_type, 'application://com.fnfr.svt.applications.process')
        self.python = SessionProfile(self._protosock, self._agent_type, 'application://com.fnfr.svt.applications.python')
        self.smartbits = SessionProfile(self._protosock, self._agent_type, 'application://com.fnfr.svt.applications.smartbits')
        self.snmp = SessionProfile(self._protosock, self._agent_type, 'application://com.fnfr.svt.applications.snmp')
        self.spirenttestcenter = SessionProfile(self._protosock, self._agent_type, 'application://com.fnfr.svt.applications.spirenttestcenter')
        self.ssh = SessionProfile(self._protosock, self._agent_type, 'application://com.fnfr.svt.applications.ssh')
        self.syslog = SessionProfile(self._protosock, self._agent_type, 'application://com.fnfr.svt.applications.syslog.syslog')
        self.tclsh = SessionProfile(self._protosock, self._agent_type, 'application://com.fnfr.svt.applications.tclsh')
        self.telnet = SessionProfile(self._protosock, self._agent_type, 'application://com.fnfr.svt.applications.telnet')
        self.web = SessionProfile(self._protosock, self._agent_type, 'application://com.fnfr.svt.applications.web')
        self.wireshark = SessionProfile(self._protosock, self._agent_type, 'application://com.fnfr.svt.applications.wireshark')