# ****************       BEGIN-STANDARD-COPYRIGHT      ***************
#
# Copyright (c) 2017, Spirent Communications.
#
# All rights reserved. Proprietary and confidential information of Spirent Communications.
#
#  ***************        END-STANDARD-COPYRIGHT       ***************

"""Session profile class and necessary tools."""

from .internal.protocol import Type

from .session_response import SessionActionResponse

_KNOWN_INVOKE_ARGS = ['response_map', 'parameters', 'command']

def _to_invoke_args(kwargs):
    """Prepares the given arguments dict for invoking as action arguments.

    Arguments:
    kwargs -- dict or arguments

    Returns a new dict, ready to be passed as arguments to invoke_command().
    """

    ret = {}
    params = {}

    for key, value in kwargs.items():
        if key in _KNOWN_INVOKE_ARGS:
            ret[key] = value
        else:
            params[key] = value

    if params:
        ret['parameters'] = params
    return ret

def _to_list(arg):
    """If arg is a list, returns it. If it's None, returns None. Otherwise, returns a one-element list with arg."""

    if arg is None:
        return None

    if isinstance(arg, list):
        return arg

    return [arg,]

def _to_requirements(agent_requirements):
    """Converts the given argument into a list of Type.Requirement.

    Arguments:
    agent_requirements -- dict of the format {'requirement_name': 'requirement_value'}. Can be None.

    Returns a list of Type.Requirement, or None.
    """

    if not agent_requirements:
        return None

    ret = []
    for key, value in agent_requirements.items():
        req = Type.Requirement()
        req.name = key
        req.value = value
        ret.append(req)

    return ret

def _to_property_list(properties, skip, property_type=Type.Property):
    """Converts the given properties into a list of Type.Property.

    Arguments:
    properties -- a dict with keys being property names and value being property values (strings). Can be None.
    skip -- a list of keys to skip.
    property_type -- a type (class) of property object. Must have 'name' and 'value' fields.

    Returns a list of Type.Property, or None.
    """

    if not properties:
        return None

    ret = []
    for key, value in properties.items():
        if key not in skip:
            prop = property_type()
            prop.name = key
            prop.value = value
            ret.append(prop)

    return ret

def _to_property_group(properties):
    """Converts the given properties dict into Type.PropertiesGroup.

    Arguments:
    properties -- a dict with keys being property names and value being property values (strings).
                      The key 'children', if any, provides nesting capabilities. Its value must be a list of other
                      dicts with the similar format. If 'children' is a session property name, use an alternative
                      dict format: {'properties': [{'name': 'value'}, ...], 'children': [{...}, ...]}.
                      Can be None.

    Returns Type.PropertiesGroup, or None.
    """

    if not properties:
        return None

    ret = Type.PropertiesGroup()

    prop_list = None
    if 'properties' in properties:
        prop_list = _to_property_list(properties['properties'], skip=[])
    else:
        prop_list = _to_property_list(properties, skip=['children'])
    ret.properties.extend(prop_list)

    if 'children' in properties:
        child_list = [_to_property_group(child) for child in properties['children'] if child]
        ret.children.extend(child_list)

    return ret

def _to_params_list(parameters):
    """Converts the given parameters to a list of Type.Param.

    Arguments:
    parameters -- a dict with keys being parameter names and values being either parameter values, or
                  a dict with two keys: 'value', which is the parameter value, and 'children', which is a dict
                  of the same type as above. Example:
                  {'param1': 'value1', 'param2': {'value': 'value2', 'children': {'child_param1': 'value3'}}}
                  Can be None.

    Returns a list of Type.Param, or None.
    """

    if not parameters:
        return None

    ret = []

    for key, value in parameters.items():
        param = Type.Param()
        param.name = key
        if isinstance(value, dict):
            param.value = str(value['value'])
            if 'children' in value:
                param.parameters.extend(_to_params_list(value['children']))
        else:
            param.value = str(value)

        ret.append(param)

    return ret


class SessionProfileInformation(object):
    """ A details object to specify agent parameters"""

    def __init__(self, agent_name, agent_id, protocol_version, agent_type ):
        """Initialise a agent parameters object
        agent_name -- a name of agent.
        agent_id -- a identifier of agent.
        protocol_version -- a version of protocol used
        """
        self.name = agent_id
        self.agent_name = agent_name
        self.protocol_version = protocol_version
        self.agent_type = agent_type

    def __str__(self):
        return str(vars(self))

class SessionProfile(object):
    """Session profile representation.

    Allows to open and close session, as well as invoking its actions and quickcalls.

    Recommended way to use this class is as follows:

        with proj.session_name_ffsp.open() as s1:
            # invoke a quickcall:
            response = s1.init_routes(all=True)

            # invoke a command:
            response = s1.command('command', response_map=proj.response_map_ffrm)

    Constructing instances of this class directly may be handy for testing, but generally is discouraged.

    Properties:
    agent -- agent information
    session_id -- if the session is opened, this will be a string representation of the session's ID.
                  Otherwise, this will be None. May be used to check is the session is opened.
    """

    def __init__(self, protocol_socket, agent_type, uri, dependencies=None):
        """Initiates a new session profile.

        Arguments:
        protocol_socket -- an instance of ProtocolSocket. It must be connected by the time open() is called.
        uri -- session profile URI, e.g. project://my_project/session_profiles/slc_test.ffsp
        dependencies -- session profile dependencies,
                        e.g. ['file:///home/dsavenko/itest/itest/dev/src/non-plugins/SpirentSLC/my_project.itar']

        """

        self._uri = uri
        self._protosock = protocol_socket
        self._deps = dependencies

        self.agent = SessionProfileInformation(self._protosock.agent_name, self._protosock.agent_id, self._protosock.protocol_version, agent_type )
        self.session_id = None

    def open(self, parameter_file=None, agent_requirements=None, properties=None, **kwargs):
        """Opens the session.

        Arguments:
        parameter_file -- a single parameter file (URI), or a list of parameter files.
        agent_requirements -- dict of the format {'requirement_name': 'requirement_value'}
        properties -- a dict with keys being property names and value being property values (strings).
                      The key 'children', if any, provides nesting capabilities. Its value must be a list of other
                      dicts with the similar format. If 'children' is a session property name, use an alternative
                      dict format: {'properties': [{'name': 'value'}, ...], 'children': [{...}, ...]}

        Raises ValueError, if the session is already opened. May raise socket.error.
        """

        if self.session_id:
            raise ValueError('Session already opened with id=' + self.session_id)

        if properties is None:
            properties = {}
            for key, value in kwargs.items():
                properties[key] = str(value)

        rsp = self._protosock.start_session(self._uri,
                                            dependencies=self._deps,
                                            param_files=_to_list(parameter_file),
                                            requirements=_to_requirements(agent_requirements),
                                            property_group=_to_property_group(properties))
        self.session_id = rsp.sessionId
        return self

    def close(self):
        """Closes the session.

        Does nothing, if the session has not been opened yet. May raise socket.error.
        """

        session_id = self.session_id
        self.session_id = None
        if session_id:
            self._protosock.close_session(session_id)

    def invoke_action(self, action, command=None, parameters=None, response_map=None):
        """Invokes session action or quickcall.

        Generally, you do not need to use this method directly. E.g. instead of calling

            ssh_session.invoke_action('command', 'ls')

        you can just call

            ssh_session.command('ls')

        For Quickcalls, instead of calling

            session.invoke_action('my_quickcall', parameters={'param1': 'value1', 'param2': 123})

        you can just call

            session.my_quickcall(param1='value1', param2=123)

        Arguments:
        action -- session action or QuickCall name. Depends on a session.
                  Widely used actions: 'close' to close the session, 'command' to execute a specific session command.
        command -- command to execute
        parameters -- a dict with keys being parameter names and values being either parameter values, or
                      a dict with two keys: 'value', which is the parameter value, and 'children', which is a dict
                      of the same type as above. Example:
                      {'param1': 'value1', 'param2': {'value': 'value2', 'children': {'child_param1': 'value3'}}}
        responseMap -- URI of the response map file to use.

        Returns action response. Raises ValueError, if the session is not opened. May raise socket.error
        """

        if not self.session_id:
            raise ValueError('Session is not opened')

        resp = self._protosock.invoke_action(self.session_id,
                                             action=action,
                                             command=command,
                                             params=_to_params_list(parameters),
                                             response_map=response_map)
        #if (isinstance(resp, InvokeResponse)):
        #    return resp.reportResult, resp.error
        #else:
        #    return SessionActionResponse(resp)
        return SessionActionResponse(resp)

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.close()

    def __getitem__(self, key):
        return lambda *args, **kwargs: self.invoke_action(key, *args, **_to_invoke_args(kwargs))

    def __getattr__(self, key):
        ret = self[key]
        if not ret:
            raise AttributeError(key)
        return ret
