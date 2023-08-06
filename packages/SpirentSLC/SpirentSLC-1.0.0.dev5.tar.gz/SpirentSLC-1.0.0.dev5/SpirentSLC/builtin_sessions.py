# ****************       BEGIN-STANDARD-COPYRIGHT      ***************
#
# Copyright (c) 2017, Spirent Communications.
#
# All rights reserved. Proprietary and confidential information of Spirent Communications.
#
#  ***************        END-STANDARD-COPYRIGHT       ***************

"""Builtin sessions provider."""

from .session_profile import SessionProfile

class BuiltinSession(object):
    """Provide an access to builtin sessions"""

    def __init__(self, protocol_socket, agent_type):
        self._protosock = protocol_socket
        self._agent_type = agent_type

        self.rtf = SessionProfile(self._protosock, self._agent_type, 'application://com.fanfare.itest.appstore.applications.rft')
        self.chat = SessionProfile(self._protosock, self._agent_type, 'application://com.fnfr.bobcat.tools.chat')
        self.serial = SessionProfile(self._protosock, self._agent_type, 'application://com.fnfr.itest.application.serial')
        self.sf_tool = SessionProfile(self._protosock, self._agent_type, 'application://com.fnfr.itest.application.sf.tool')
        self.file = SessionProfile(self._protosock, self._agent_type, 'application://com.fnfr.itest.applications.file')
        self.landslide = SessionProfile(self._protosock, self._agent_type, 'application://com.fnfr.itest.applications.landslide')
        self.ranorex = SessionProfile(self._protosock, self._agent_type, 'application://com.fnfr.itest.applications.ranorex')
        self.selenium = SessionProfile(self._protosock, self._agent_type, 'application://com.fnfr.itest.applications.selenium')
        self.netconf = SessionProfile(self._protosock, self._agent_type, 'application://com.fnfr.itest.applications.spirent.netconf.tool')
        self.posapp = SessionProfile(self._protosock, self._agent_type, 'application://com.fnfr.itest.applications.spirent.posapp.tool')
        self.udp = SessionProfile(self._protosock, self._agent_type, 'application://com.fnfr.itest.applications.udp.tool')
        self.vmware_core = SessionProfile(self._protosock, self._agent_type, 'application://com.fnfr.itest.applications.vmware.vi.core.tool')
        self.vmware_vscphere = SessionProfile(self._protosock, self._agent_type, 'application://com.fnfr.itest.applications.vmware.vsphere.core.tool')
        self.vnc = SessionProfile(self._protosock, self._agent_type, 'application://com.fnfr.itest.applications.vnc')
        self.webservices = SessionProfile(self._protosock, self._agent_type, 'application://com.fnfr.itest.applications.webservices')
        self.rest = SessionProfile(self._protosock, self._agent_type, 'application://com.fnfr.itest.applications.webservices.restful')
        self.xmlrpc = SessionProfile(self._protosock, self._agent_type, 'application://com.fnfr.itest.applications.webservices.xmlrpc')
        self.database = SessionProfile(self._protosock, self._agent_type, 'application://com.fnfr.itest.tools.database')
        self.flex = SessionProfile(self._protosock, self._agent_type, 'application://com.fnfr.itest.tools.flex')
        self.windowsgui = SessionProfile(self._protosock, self._agent_type, 'application://com.fnfr.itest.tools.windowsgui')
        #self.testtool = SessionProfile(self._protosock, self._agent_type, 'application://com.fnfr.open.automation.tool.testtool')
        self.agilent = SessionProfile(self._protosock, self._agent_type, 'application://com.fnfr.svt.applications.agilent')
        self.http = SessionProfile(self._protosock, self._agent_type, 'application://com.fnfr.svt.applications.http')
        self.ixia_ixload = SessionProfile(self._protosock, self._agent_type, 'application://com.fnfr.svt.applications.ixia.ixload')
        self.ixia_ixnetwork = SessionProfile(self._protosock, self._agent_type, 'application://com.fnfr.svt.applications.ixia.ixnetwork')
        self.ixiaTraffic = SessionProfile(self._protosock, self._agent_type, 'application://com.fnfr.svt.applications.ixiaTraffic')
        #self.swing = SessionProfile(self._protosock, self._agent_type, 'application://com.fnfr.svt.applications.java.swing')
        self.mail = SessionProfile(self._protosock, self._agent_type, 'application://com.fnfr.svt.applications.mail')
        self.process = SessionProfile(self._protosock, self._agent_type, 'application://com.fnfr.svt.applications.process')
        self.python = SessionProfile(self._protosock, self._agent_type, 'application://com.fnfr.svt.applications.python')
        self.smartbits = SessionProfile(self._protosock, self._agent_type, 'application://com.fnfr.svt.applications.smartbits')
        self.snmp = SessionProfile(self._protosock, self._agent_type, 'application://com.fnfr.svt.applications.snmp')
        self.avalanche = SessionProfile(self._protosock, self._agent_type, 'application://com.fnfr.svt.applications.spirent.avalanche')
        self.testcenter_gui = SessionProfile(self._protosock, self._agent_type, 'application://com.fnfr.svt.applications.spirent.testcenter.gui')
        self.spirenttestcenter = SessionProfile(self._protosock, self._agent_type, 'application://com.fnfr.svt.applications.spirenttestcenter')
        self.ssh = SessionProfile(self._protosock, self._agent_type, 'application://com.fnfr.svt.applications.ssh')
        self.syslog = SessionProfile(self._protosock, self._agent_type, 'application://com.fnfr.svt.applications.syslog')
        self.tclsh = SessionProfile(self._protosock, self._agent_type, 'application://com.fnfr.svt.applications.tclsh')
        self.telnet = SessionProfile(self._protosock, self._agent_type, 'application://com.fnfr.svt.applications.telnet')
        self.web = SessionProfile(self._protosock, self._agent_type, 'application://com.fnfr.svt.applications.web')
        self.wireshark = SessionProfile(self._protosock, self._agent_type, 'application://com.fnfr.svt.applications.wireshark')
        self.landsliderest = SessionProfile(self._protosock, self._agent_type, 'application://com.spirent.itest.applications.landsliderest')
        self.popmail = SessionProfile(self._protosock, self._agent_type, 'application://com.spirent.itest.applications.popmail')
        #self.scriptingSession = SessionProfile(self._protosock, self._agent_type, 'application://com.spirent.itest.applications.sf.scriptingSession')
        self.stcrest = SessionProfile(self._protosock, self._agent_type, 'application://com.spirent.itest.applications.stcrest')
        self.testplant = SessionProfile(self._protosock, self._agent_type, 'application://com.spirent.itest.applications.testplant')
