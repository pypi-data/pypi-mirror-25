# Copyright 2014-present, Apstra, Inc. All rights reserved.
#
# This source code is licensed under End User License Agreement found in the
# LICENSE file at http://www.apstra.com/community/eula


import os

from apstra.aosom.exc import (
    LoginServerUnreachableError, LoginError,
    NoLoginError, LoginNoServerError, SessionRqstError)
from apstra.aosom.utils.dynmodldr import DynamicModuleOwner
from .session_api import Api

__all__ = ['Session']


class Session(DynamicModuleOwner):
    """
    The Session class is used to create a client connection with the AOS-server.  The general
    process to create a connection is as follows::

        from apstra.aosom.session import Session

        aos = Session('aos-session')                  # hostname or ip-addr of AOS-server
        aos.login()                                   # username/password uses defaults

    This module will use your environment variables to provide the default login values,
    if they are set.  Refer to :data:`~Session.ENV` for specific values.

    This module will use value defaults as defined in :data:`~Session.DEFAULTS`.

    Once you have an active session with the AOS-server you use the modules defined in the
    :data:`~Session.ModuleCatalog`.

    The following are the available public attributes of a Session instance:
        * `api` - an instance of the :class:`Session.Api` that provides HTTP access capabilities.
        * `server` - the provided AOS-server hostname/ip-addr value.
        * `user` - the provided AOS login user-name

    The following are the available user-shell environment variables that are used by the Session instance:
        * :data:`AOS_SERVER` - the AOS-server hostname/ip-addr
        * :data:`AOS_USER` - the login user-name, defaults to :data:`~DEFAULTS[\"USER\"]`.
        * :data:`AOS_PASSWD` - the login user-password, defaults to :data:`~DEFAULTS[\"PASSWD\"]`.
        * :data:`AOS_SESSION_TOKEN` - a pre-existing API session-token to avoid user login/authentication.
    """

    DynamicModuleConf = [{
        'package': __package__,
        'dirs': [
            'blueprints',
            'design_elements',
            'resource_pools',
            'system_elements'
        ]
    }]

    ENV = {
        'SERVER': 'AOS_SERVER',
        'PORT': 'AOS_SERVER_PORT',
        'TOKEN': 'AOS_SESSION_TOKEN',
        'USER': 'AOS_USER',
        'PASSWD': 'AOS_PASSWD'
    }

    DEFAULTS = {
        'USER': 'admin',
        'PASSWD': 'admin',
        'PORT': 443
    }

    Api = Api

    def __init__(self, target=None, **kwargs):
        """
        Create a Session instance that will connect to an AOS-server, `server`.  Additional
        keyword arguments can be provided that override the default values, as defined
        in :data:`~Session.DEFAULTS`, or the values that are taken from the callers shell
        environment, as defined in :data:`~Session.ENV`.  Once a Session instance has been
        created, the caller can complete the login process by invoking :meth:`login`.

        Parameters
        ----------
        target : str
            URL to the AOS-Server.  The target value must be in the form of
            <scheme>://<aos-server>[:port].  For example:

                https://aos-server
                http://aos-server
                http://aos-server:8888

        user : str
            User login name

        passwd : str
            User login password
        """
        self.api = Session.Api(self)
        self._target = target
        self.user, self.passwd = (None, None)
        self._set_login(target, **kwargs)

    # ### ---------------------------------------------------------------------
    # ### PROPERTY: url
    # ### ---------------------------------------------------------------------

    @property
    def url(self):
        """
        Returns
        -------
        Return the current AOS-server API URL.  If this value is
        not set, then an exception is raised.  The raise here is important
        because other code depends on this behavior.

        Raises
        ------
        NoLoginError: URL does not exist
        """
        if not self.api.url:
            raise NoLoginError(
                "not logged into server '{}:{}'".format(self.server, self.port))

        return self.api.url

    # ### ---------------------------------------------------------------------
    # ### PROPERTY: token
    # ### ---------------------------------------------------------------------

    @property
    def token(self):
        """
        Returns
        -------
        str
            Authentication token from existing session.

        Raises
        ------
        NoLoginError
            When no token is present.

        """
        try:
            return self.api.token
        except:
            raise NoLoginError()

    # ### ---------------------------------------------------------------------
    # ### PROPERTY: server (hostname) and port
    # ### ---------------------------------------------------------------------

    @property
    def server(self):
        return self.api.server

    @property
    def port(self):
        return self.api.port

    # ### ---------------------------------------------------------------------
    # ### PROPERTY: session
    # ### ---------------------------------------------------------------------

    @property
    def session(self):
        """
        When used as a `setter` attempts to resume an existing session with the AOS-server using the provided session
        data. If there is an error, an exception is raised.

        Returns
        -------
        dict
            The session data that can be used for a future resume.

        Raises
        ------
            See the :meth:`login` for details.
        """
        return {
            'target': self._target,
            'token': self.token
        }

    @session.setter
    def session(self, prev_session):
        try:
            self._target = prev_session['target']
            token = prev_session['token']
        except KeyError as exc:
            raise LoginError("Invalid session data, missing '{}'".format(exc.message))

        self.api.init()
        self.api.token = token
        self.api.resume()

    @property
    def version(self):
        got = self.api.requests.get(self.api.url + "/version")
        if not got.ok:
            raise SessionRqstError(got, message='Unable to obtain version info')
        return got.json()

    @property
    def valid(self):
        """
        Returns bool if this session is valid; i.e. we have a valid login/token.

        Returns
        -------
        True if valid
        False if not valid.
        """
        return self.api.verify_token()

    @property
    def build_version(self):
        got = self.api.requests.get(self.api.url + "/versions/build")
        if not got.ok:
            raise SessionRqstError(got, message='Unable to obtain build version info')
        return got.json()

    # ### ---------------------------------------------------------------------
    # ###
    # ###                         PUBLIC METHODS
    # ###
    # ### ---------------------------------------------------------------------

    def login(self):
        """
        Login to the AOS-server, obtaining a session token for use with later
        calls to the API.

        Raises
        ------
        LoginAuthError
            The provided user credentials are not valid.  Check the user/password
            or session token values provided.

        LoginServerUnreachableError
            The API is not able to connect to the AOS-server via the API. This
            could be due to any number of networking related issues. For example,
            the :attr:`port` is blocked by a firewall, or the :attr:`server` value is IP unreachable.

        LoginNoServerError
            The instance does not have :attr:`server` configured.
        """
        self.api.init()

        if not self.server:
            raise LoginNoServerError()

        if not self.api.probe():
            raise LoginServerUnreachableError()

        self.api.login(self.user, self.passwd)

    # ### ---------------------------------------------------------------------
    # ###
    # ###                         PRIVATE METHODS
    # ###
    # ### ---------------------------------------------------------------------

    def _set_login(self, target, **kwargs):
        self.user = kwargs.get('user') \
            or os.getenv(Session.ENV['USER']) \
            or Session.DEFAULTS['USER']

        self.passwd = kwargs.get('passwd') \
            or os.getenv(Session.ENV['PASSWD']) \
            or Session.DEFAULTS['PASSWD']

        if target:
            self._target = target
            return

        server = kwargs.get('server') \
            or os.getenv(Session.ENV['SERVER'])

        port = (kwargs.get('port') or
                os.getenv(Session.ENV['PORT']) or
                Session.DEFAULTS['PORT'])

        if server and port:
            if port == 443:
                self._target = "https://%s" % server
            else:
                self._target = "http://{}:{}".format(server, port)
