# Copyright 2012 Red Hat, Inc.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

r"""
Configuration options may be set on the command line or in config files.

The schema for each option is defined using the
:class:`Opt` class or its sub-classes, for example:

::

    from oslo_config import cfg
    from oslo_config import types

    PortType = types.Integer(1, 65535)

    common_opts = [
        cfg.StrOpt('bind_host',
                   default='0.0.0.0',
                   help='IP address to listen on.'),
        cfg.Opt('bind_port',
                type=PortType,
                default=9292,
                help='Port number to listen on.')
    ]

Option Types
------------

Options can have arbitrary types via the `type` parameter to the :class:`Opt`
constructor. The `type` parameter is a callable object that takes a string and
either returns a value of that particular type or raises :class:`ValueError` if
the value can not be converted.

For convenience, there are predefined option subclasses in
:mod:`oslo_config.cfg` that set the option `type` as in the following table:

======================================  ======
Type                                    Option
======================================  ======
:class:`oslo_config.types.String`       :class:`oslo_config.cfg.StrOpt`
:class:`oslo_config.types.String`       :class:`oslo_config.cfg.SubCommandOpt`
:class:`oslo_config.types.Boolean`      :class:`oslo_config.cfg.BoolOpt`
:class:`oslo_config.types.Integer`      :class:`oslo_config.cfg.IntOpt`
:class:`oslo_config.types.Float`        :class:`oslo_config.cfg.FloatOpt`
:class:`oslo_config.types.Port`         :class:`oslo_config.cfg.PortOpt`
:class:`oslo_config.types.List`         :class:`oslo_config.cfg.ListOpt`
:class:`oslo_config.types.Dict`         :class:`oslo_config.cfg.DictOpt`
:class:`oslo_config.types.IPAddress`    :class:`oslo_config.cfg.IPOpt`
:class:`oslo_config.types.Hostname`     :class:`oslo_config.cfg.HostnameOpt`
:class:`oslo_config.types.HostAddress`  :class:`oslo_config.cfg.HostAddressOpt`
:class:`oslo_config.types.URI`          :class:`oslo_config.cfg.URIOpt`
======================================  ======

For :class:`oslo_config.cfg.MultiOpt` the `item_type` parameter defines
the type of the values. For convenience, :class:`oslo_config.cfg.MultiStrOpt`
is :class:`~oslo_config.cfg.MultiOpt` with the `item_type` parameter set to
:class:`oslo_config.types.MultiString`.

The following example defines options using the convenience classes::

    enabled_apis_opt = cfg.ListOpt('enabled_apis',
                                   default=['ec2', 'osapi_compute'],
                                   help='List of APIs to enable by default.')

    DEFAULT_EXTENSIONS = [
        'nova.api.openstack.compute.contrib.standard_extensions'
    ]
    osapi_compute_extension_opt = cfg.MultiStrOpt('osapi_compute_extension',
                                                  default=DEFAULT_EXTENSIONS)

Registering Options
-------------------

Option schemas are registered with the config manager at runtime, but before
the option is referenced::

    class ExtensionManager(object):

        enabled_apis_opt = cfg.ListOpt(...)

        def __init__(self, conf):
            self.conf = conf
            self.conf.register_opt(enabled_apis_opt)
            ...

        def _load_extensions(self):
            for ext_factory in self.conf.osapi_compute_extension:
                ....

A common usage pattern is for each option schema to be defined in the module or
class which uses the option::

    opts = ...

    def add_common_opts(conf):
        conf.register_opts(opts)

    def get_bind_host(conf):
        return conf.bind_host

    def get_bind_port(conf):
        return conf.bind_port

An option may optionally be made available via the command line. Such options
must be registered with the config manager before the command line is parsed
(for the purposes of --help and CLI arg validation)::

    cli_opts = [
        cfg.BoolOpt('verbose',
                    short='v',
                    default=False,
                    help='Print more verbose output.'),
        cfg.BoolOpt('debug',
                    short='d',
                    default=False,
                    help='Print debugging output.'),
    ]

    def add_common_opts(conf):
        conf.register_cli_opts(cli_opts)

Loading Config Files
--------------------

The config manager has two CLI options defined by default, --config-file
and --config-dir::

    class ConfigOpts(object):

        def __call__(self, ...):

            opts = [
                MultiStrOpt('config-file',
                        ...),
                StrOpt('config-dir',
                       ...),
            ]

            self.register_cli_opts(opts)

Option values are parsed from any supplied config files using
oslo_config.iniparser. If none are specified, a default set is used
for example glance-api.conf and glance-common.conf::

    glance-api.conf:
      [DEFAULT]
      bind_port = 9292

    glance-common.conf:
      [DEFAULT]
      bind_host = 0.0.0.0

Lines in a configuration file should not start with whitespace. A
configuration file also supports comments, which must start with '#' or ';'.
Option values in config files and those on the command line are parsed
in order. The same option (includes deprecated option name and current
option name) can appear many times, in config files or on the command line.
Later values always override earlier ones.

The order of configuration files inside the same configuration directory is
defined by the alphabetic sorting order of their file names.

The parsing of CLI args and config files is initiated by invoking the config
manager for example::

    conf = cfg.ConfigOpts()
    conf.register_opt(cfg.BoolOpt('verbose', ...))
    conf(sys.argv[1:])
    if conf.verbose:
        ...

Option Groups
-------------

Options can be registered as belonging to a group::

    rabbit_group = cfg.OptGroup(name='rabbit',
                                title='RabbitMQ options')

    rabbit_host_opt = cfg.StrOpt('host',
                                 default='localhost',
                                 help='IP/hostname to listen on.'),
    rabbit_port_opt = cfg.PortOpt('port',
                                  default=5672,
                                  help='Port number to listen on.')

    def register_rabbit_opts(conf):
        conf.register_group(rabbit_group)
        # options can be registered under a group in either of these ways:
        conf.register_opt(rabbit_host_opt, group=rabbit_group)
        conf.register_opt(rabbit_port_opt, group='rabbit')

If no group attributes are required other than the group name, the group
need not be explicitly registered for example::

    def register_rabbit_opts(conf):
        # The group will automatically be created, equivalent calling::
        #   conf.register_group(OptGroup(name='rabbit'))
        conf.register_opt(rabbit_port_opt, group='rabbit')

If no group is specified, options belong to the 'DEFAULT' section of config
files::

    glance-api.conf:
      [DEFAULT]
      bind_port = 9292
      ...

      [rabbit]
      host = localhost
      port = 5672
      use_ssl = False
      userid = guest
      password = guest
      virtual_host = /

Command-line options in a group are automatically prefixed with the
group name::

    --rabbit-host localhost --rabbit-port 9999

Dynamic Groups
--------------

Groups can be registered dynamically by application code. This
introduces a challenge for the sample generator, discovery mechanisms,
and validation tools, since they do not know in advance the names of
all of the groups. The ``dynamic_group_owner`` parameter to the
constructor specifies the full name of an option registered in another
group that controls repeated instances of a dynamic group. This option
is usually a MultiStrOpt.

For example, Cinder supports multiple storage backend devices and
services. To configure Cinder to communicate with multiple backends,
the ``enabled_backends`` option is set to the list of names of
backends. Each backend group includes the options for communicating
with that device or service.

Driver Groups
-------------

Groups can have dynamic sets of options, usually based on a driver
that has unique requirements. This works at runtime because the code
registers options before it uses them, but it introduces a challenge
for the sample generator, discovery mechanisms, and validation tools
because they do not know in advance the correct options for a group.

To address this issue, the driver option for a group can be named
using the ``driver_option`` parameter.  Each driver option should
define its own discovery entry point namespace to return the set of
options for that driver, named using the prefix
``"oslo.config.opts."`` followed by the driver option name.

In the Cinder case described above, a ``volume_backend_name`` option
is part of the static definition of the group, so ``driver_option``
should be set to ``"volume_backend_name"``. And plugins should be
registered under ``"oslo.config.opts.volume_backend_name"`` using the
same names as the main plugin registered with
``"oslo.config.opts"``. The drivers residing within the Cinder code
base have an entry point named ``"cinder"`` registered.

Accessing Option Values In Your Code
------------------------------------

Option values in the default group are referenced as attributes/properties on
the config manager; groups are also attributes on the config manager, with
attributes for each of the options associated with the group::

    server.start(app, conf.bind_port, conf.bind_host, conf)

    self.connection = kombu.connection.BrokerConnection(
        hostname=conf.rabbit.host,
        port=conf.rabbit.port,
        ...)

Option Value Interpolation
--------------------------

Option values may reference other values using PEP 292 string substitution::

    opts = [
        cfg.StrOpt('state_path',
                   default=os.path.join(os.path.dirname(__file__), '../'),
                   help='Top-level directory for maintaining nova state.'),
        cfg.StrOpt('sqlite_db',
                   default='nova.sqlite',
                   help='File name for SQLite.'),
        cfg.StrOpt('sql_connection',
                   default='sqlite:///$state_path/$sqlite_db',
                   help='Connection string for SQL database.'),
    ]

.. note::

  Interpolation can be avoided by using `$$`.

.. note::

  You can use `.` to delimit option from other groups, e.g.
  ${mygroup.myoption}.

Special Handling Instructions
-----------------------------

Options may be declared as required so that an error is raised if the user
does not supply a value for the option::

    opts = [
        cfg.StrOpt('service_name', required=True),
        cfg.StrOpt('image_id', required=True),
        ...
    ]

Options may be declared as secret so that their values are not leaked into
log files::

     opts = [
        cfg.StrOpt('s3_store_access_key', secret=True),
        cfg.StrOpt('s3_store_secret_key', secret=True),
        ...
     ]

Dictionary Options
------------------

If you need end users to specify a dictionary of key/value pairs, then you can
use the DictOpt::

    opts = [
        cfg.DictOpt('foo',
                    default={})
    ]

The end users can then specify the option foo in their configuration file
as shown below:

.. code-block:: ini

    [DEFAULT]
    foo = k1:v1,k2:v2


Global ConfigOpts
-----------------

This module also contains a global instance of the ConfigOpts class
in order to support a common usage pattern in OpenStack::

    from oslo_config import cfg

    opts = [
        cfg.StrOpt('bind_host', default='0.0.0.0'),
        cfg.PortOpt('bind_port', default=9292),
    ]

    CONF = cfg.CONF
    CONF.register_opts(opts)

    def start(server, app):
        server.start(app, CONF.bind_port, CONF.bind_host)

Positional Command Line Arguments
---------------------------------

Positional command line arguments are supported via a 'positional' Opt
constructor argument::

    >>> conf = cfg.ConfigOpts()
    >>> conf.register_cli_opt(cfg.MultiStrOpt('bar', positional=True))
    True
    >>> conf(['a', 'b'])
    >>> conf.bar
    ['a', 'b']

Sub-Parsers
-----------

It is also possible to use argparse "sub-parsers" to parse additional
command line arguments using the SubCommandOpt class:

    >>> def add_parsers(subparsers):
    ...     list_action = subparsers.add_parser('list')
    ...     list_action.add_argument('id')
    ...
    >>> conf = cfg.ConfigOpts()
    >>> conf.register_cli_opt(cfg.SubCommandOpt('action', handler=add_parsers))
    True
    >>> conf(args=['list', '10'])
    >>> conf.action.name, conf.action.id
    ('list', '10')

Advanced Option
---------------

Use if you need to label an option as advanced in sample files, indicating the
option is not normally used by the majority of users and might have a
significant effect on stability and/or performance::

    from oslo_config import cfg

    opts = [
        cfg.StrOpt('option1', default='default_value',
                    advanced=True, help='This is help '
                    'text.'),
        cfg.PortOpt('option2', default='default_value',
                     help='This is help text.'),
    ]

    CONF = cfg.CONF
    CONF.register_opts(opts)

This will result in the option being pushed to the bottom of the
namespace and labeled as advanced in the sample files, with a notation
about possible effects::

    [DEFAULT]
    ...
    # This is help text. (string value)
    # option2 = default_value
    ...
    <pushed to bottom of section>
    ...
    # This is help text. (string value)
    # Advanced Option: intended for advanced users and not used
    # by the majority of users, and might have a significant
    # effect on stability and/or performance.
    # option1 = default_value

Option Deprecation
------------------

If you want to rename some options, move them to another group or remove
completely, you may change their declarations using `deprecated_name`,
`deprecated_group`  and `deprecated_for_removal` parameters to the :class:`Opt`
constructor::

    from oslo_config import cfg

    conf = cfg.ConfigOpts()

    opt_1 = cfg.StrOpt('opt_1', default='foo', deprecated_name='opt1')
    opt_2 = cfg.StrOpt('opt_2', default='spam', deprecated_group='DEFAULT')
    opt_3 = cfg.BoolOpt('opt_3', default=False, deprecated_for_removal=True)

    conf.register_opt(opt_1, group='group_1')
    conf.register_opt(opt_2, group='group_2')
    conf.register_opt(opt_3)

    conf(['--config-file', 'config.conf'])

    assert conf.group_1.opt_1 == 'bar'
    assert conf.group_2.opt_2 == 'eggs'
    assert conf.opt_3

Assuming that the file config.conf has the following content::

    [group_1]
    opt1 = bar

    [DEFAULT]
    opt_2 = eggs
    opt_3 = True

the script will succeed, but will log three respective warnings about the
given deprecated options.

There are also `deprecated_reason` and `deprecated_since` parameters for
specifying some additional information about a deprecation.

All the mentioned parameters can be mixed together in any combinations.

"""

import argparse
import collections
import copy
import errno
import functools
import glob
import itertools
import logging
import os
import string
import sys

from debtcollector import removals
import six


from oslo_config import iniparser
from oslo_config import types

LOG = logging.getLogger(__name__)


class Error(Exception):
    """Base class for cfg exceptions."""

    def __init__(self, msg=None):
        self.msg = msg

    def __str__(self):
        return self.msg


class NotInitializedError(Error):
    """Raised if parser is not initialized yet."""

    def __str__(self):
        return "call expression on parser has not been invoked"


class ArgsAlreadyParsedError(Error):
    """Raised if a CLI opt is registered after parsing."""

    def __str__(self):
        ret = "arguments already parsed"
        if self.msg:
            ret += ": " + self.msg
        return ret


class NoSuchOptError(Error, AttributeError):
    """Raised if an opt which doesn't exist is referenced."""

    def __init__(self, opt_name, group=None):
        self.opt_name = opt_name
        self.group = group

    def __str__(self):
        group_name = 'DEFAULT' if self.group is None else self.group.name
        return "no such option %s in group [%s]" % (self.opt_name, group_name)


class NoSuchGroupError(Error):
    """Raised if a group which doesn't exist is referenced."""

    def __init__(self, group_name):
        self.group_name = group_name

    def __str__(self):
        return "no such group [%s]" % self.group_name


class DuplicateOptError(Error):
    """Raised if multiple opts with the same name are registered."""

    def __init__(self, opt_name):
        self.opt_name = opt_name

    def __str__(self):
        return "duplicate option: %s" % self.opt_name


class RequiredOptError(Error):
    """Raised if an option is required but no value is supplied by the user."""

    def __init__(self, opt_name, group=None):
        self.opt_name = opt_name
        self.group = group

    def __str__(self):
        group_name = 'DEFAULT' if self.group is None else self.group.name
        return "value required for option %s in group [%s]" % (self.opt_name,
                                                               group_name)


class TemplateSubstitutionError(Error):
    """Raised if an error occurs substituting a variable in an opt value."""

    def __str__(self):
        return "template substitution error: %s" % self.msg


class ConfigFilesNotFoundError(Error):
    """Raised if one or more config files are not found."""

    def __init__(self, config_files):
        self.config_files = config_files

    def __str__(self):
        return ('Failed to find some config files: %s' %
                ",".join(self.config_files))


class ConfigFilesPermissionDeniedError(Error):
    """Raised if one or more config files are not readable."""

    def __init__(self, config_files):
        self.config_files = config_files

    def __str__(self):
        return ('Failed to open some config files: %s' %
                ",".join(self.config_files))


class ConfigDirNotFoundError(Error):
    """Raised if the requested config-dir is not found."""

    def __init__(self, config_dir):
        self.config_dir = config_dir

    def __str__(self):
        return ('Failed to read config file directory: %s' % self.config_dir)


class ConfigFileParseError(Error):
    """Raised if there is an error parsing a config file."""

    def __init__(self, config_file, msg):
        self.config_file = config_file
        self.msg = msg

    def __str__(self):
        return 'Failed to parse %s: %s' % (self.config_file, self.msg)


class ConfigFileValueError(Error, ValueError):
    """Raised if a config file value does not match its opt type."""
    pass


class DefaultValueError(Error, ValueError):
    """Raised if a default config type does not fit the opt type."""


def _fixpath(p):
    """Apply tilde expansion and absolutization to a path."""
    return os.path.abspath(os.path.expanduser(p))


def _get_config_dirs(project=None):
    """Return a list of directories where config files may be located.

    :param project: an optional project name

    If a project is specified, following directories are returned::

      ~/.${project}/
      ~/
      /etc/${project}/
      /etc/

    If a project is specified and installed from a snap package, following
    directories are also returned:

      ${SNAP}/etc/${project}
      ${SNAP_COMMON}/etc/${project}

    Otherwise, if project is not specified, these directories are returned:

      ~/
      /etc/
    """
    snap = os.environ.get('SNAP')
    snap_c = os.environ.get('SNAP_COMMON')

    cfg_dirs = [
        _fixpath(os.path.join('~', '.' + project)) if project else None,
        _fixpath('~'),
        os.path.join('/etc', project) if project else None,
        '/etc',
        os.path.join(snap, "etc", project) if snap and project else None,
        os.path.join(snap_c, "etc", project) if snap_c and project else None,
    ]
    return [x for x in cfg_dirs if x]


def _search_dirs(dirs, basename, extension=""):
    """Search a list of directories for a given filename or directory name.

    Iterator over the supplied directories, returning the first file
    found with the supplied name and extension.

    :param dirs: a list of directories
    :param basename: the filename or directory name, for example 'glance-api'
    :param extension: the file extension, for example '.conf'
    :returns: the path to a matching file or directory, or None
    """
    for d in dirs:
        path = os.path.join(d, '%s%s' % (basename, extension))
        if os.path.exists(path):
            return path


def _find_config_files(project, prog, extension):
    if prog is None:
        prog = os.path.basename(sys.argv[0])
        if prog.endswith(".py"):
            prog = prog[:-3]

    cfg_dirs = _get_config_dirs(project)
    config_files = (_search_dirs(cfg_dirs, p, extension)
                    for p in [project, prog] if p)

    return [x for x in config_files if x]


def find_config_files(project=None, prog=None, extension='.conf'):
    """Return a list of default configuration files.

    :param project: an optional project name
    :param prog: the program name, defaulting to the basename of
        sys.argv[0], without extension .py
    :param extension: the type of the config file

    We default to two config files: [${project}.conf, ${prog}.conf]

    And we look for those config files in the following directories::

      ~/.${project}/
      ~/
      /etc/${project}/
      /etc/
      ${SNAP}/etc/${project}
      ${SNAP_COMMON}/etc/${project}

    We return an absolute path for (at most) one of each the default config
    files, for the topmost directory it exists in.

    For example, if project=foo, prog=bar and /etc/foo/foo.conf, /etc/bar.conf
    and ~/.foo/bar.conf all exist, then we return ['/etc/foo/foo.conf',
    '~/.foo/bar.conf']

    If no project name is supplied, we only look for ${prog}.conf.
    """
    return _find_config_files(project, prog, extension)


def find_config_dirs(project=None, prog=None, extension='.conf.d'):
    """Return a list of default configuration dirs.

    :param project: an optional project name
    :param prog: the program name, defaulting to the basename of
        sys.argv[0], without extension .py
    :param extension: the type of the config directory. Defaults to '.conf.d'

    We default to two config dirs: [${project}.conf.d/, ${prog}.conf.d/].
    If no project name is supplied, we only look for ${prog.conf.d/}.

    And we look for those config dirs in the following directories::

      ~/.${project}/
      ~/
      /etc/${project}/
      /etc/
      ${SNAP}/etc/${project}
      ${SNAP_COMMON}/etc/${project}

    We return an absolute path for each of the two config dirs,
    in the first place we find it (iff we find it).

    For example, if project=foo, prog=bar and /etc/foo/foo.conf.d/,
    /etc/bar.conf.d/ and ~/.foo/bar.conf.d/ all exist, then we return
    ['/etc/foo/foo.conf.d/', '~/.foo/bar.conf.d/']
    """
    return _find_config_files(project, prog, extension)


def _is_opt_registered(opts, opt):
    """Check whether an opt with the same name is already registered.

    The same opt may be registered multiple times, with only the first
    registration having any effect. However, it is an error to attempt
    to register a different opt with the same name.

    :param opts: the set of opts already registered
    :param opt: the opt to be registered
    :returns: True if the opt was previously registered, False otherwise
    :raises: DuplicateOptError if a naming conflict is detected
    """
    if opt.dest in opts:
        if opts[opt.dest]['opt'] != opt:
            raise DuplicateOptError(opt.name)
        return True
    else:
        return False


def set_defaults(opts, **kwargs):
    for opt in opts:
        if opt.dest in kwargs:
            opt.default = kwargs[opt.dest]


def _normalize_group_name(group_name):
    if group_name == 'DEFAULT':
        return group_name
    return group_name.lower()


@functools.total_ordering
class Opt(object):

    """Base class for all configuration options.

    The only required parameter is the option's name. However, it is
    common to also supply a default and help string for all options.

    :param name: the option's name
    :param type: the option's type. Must be a callable object that takes string
                 and returns converted and validated value
    :param dest: the name of the corresponding :class:`.ConfigOpts` property
    :param short: a single character CLI option name
    :param default: the default value of the option
    :param positional: True if the option is a positional CLI argument
    :param metavar: the option argument to show in --help
    :param help: an explanation of how the option is used
    :param secret: true if the value should be obfuscated in log output
    :param required: true if a value must be supplied for this option
    :param deprecated_name: deprecated name option.  Acts like an alias
    :param deprecated_group: the group containing a deprecated alias
    :param deprecated_opts: list of :class:`.DeprecatedOpt`
    :param sample_default: a default string for sample config files
    :param deprecated_for_removal: indicates whether this opt is planned for
                                   removal in a future release
    :param deprecated_reason: indicates why this opt is planned for removal in
                              a future release. Silently ignored if
                              deprecated_for_removal is False
    :param deprecated_since: indicates which release this opt was deprecated
                             in. Accepts any string, though valid version
                             strings are encouraged. Silently ignored if
                             deprecated_for_removal is False
    :param mutable: True if this option may be reloaded
    :param advanced: a bool True/False value if this option has advanced usage
                             and is not normally used by the majority of users

    An Opt object has no public methods, but has a number of public properties:

    .. py:attribute:: name

        the name of the option, which may include hyphens

    .. py:attribute:: type

        a callable object that takes string and returns converted and
        validated value.  Default types are available from
        :class:`oslo_config.types`

    .. py:attribute:: dest

        the (hyphen-less) :class:`.ConfigOpts` property which contains the
        option value

    .. py:attribute:: short

        a single character CLI option name

    .. py:attribute:: default

        the default value of the option

    .. py:attribute:: sample_default

        a sample default value string to include in sample config files

    .. py:attribute:: positional

        True if the option is a positional CLI argument

    .. py:attribute:: metavar

        the name shown as the argument to a CLI option in --help output

    .. py:attribute:: help

        a string explaining how the option's value is used

    .. py:attribute:: advanced

        in sample files, a bool value indicating the option is advanced

    .. versionchanged:: 1.2
       Added *deprecated_opts* parameter.

    .. versionchanged:: 1.4
       Added *sample_default* parameter.

    .. versionchanged:: 1.9
       Added *deprecated_for_removal* parameter.

    .. versionchanged:: 2.7
       An exception is now raised if the default value has the wrong type.

    .. versionchanged:: 3.2
       Added *deprecated_reason* parameter.

    .. versionchanged:: 3.5
       Added *mutable* parameter.

    .. versionchanged:: 3.12
       Added *deprecated_since* parameter.

    .. versionchanged:: 3.15
       Added *advanced* parameter and attribute.
    """
    multi = False

    def __init__(self, name, type=None, dest=None, short=None,
                 default=None, positional=False, metavar=None, help=None,
                 secret=False, required=False,
                 deprecated_name=None, deprecated_group=None,
                 deprecated_opts=None, sample_default=None,
                 deprecated_for_removal=False, deprecated_reason=None,
                 deprecated_since=None, mutable=False, advanced=False):
        if name.startswith('_'):
            raise ValueError('illegal name %s with prefix _' % (name,))
        self.name = name

        if type is None:
            type = types.String()

        if not callable(type):
            raise TypeError('type must be callable')
        self.type = type

        if dest is None:
            self.dest = self.name.replace('-', '_')
        else:
            self.dest = dest
        self.short = short
        self.default = default
        self.sample_default = sample_default
        self.positional = positional
        self.metavar = metavar
        self.help = help
        self.secret = secret
        self.required = required
        self.deprecated_for_removal = deprecated_for_removal
        self.deprecated_reason = deprecated_reason
        self.deprecated_since = deprecated_since
        self._logged_deprecation = False

        self.deprecated_opts = copy.deepcopy(deprecated_opts) or []
        for o in self.deprecated_opts:
            if '-' in o.name:
                self.deprecated_opts.append(DeprecatedOpt(
                    o.name.replace('-', '_'),
                    group=o.group))
        if deprecated_name is not None or deprecated_group is not None:
            self.deprecated_opts.append(DeprecatedOpt(deprecated_name,
                                                      group=deprecated_group))
            if deprecated_name and '-' in deprecated_name:
                self.deprecated_opts.append(DeprecatedOpt(
                    deprecated_name.replace('-', '_'),
                    group=deprecated_group))
        self._check_default()

        self.mutable = mutable
        self.advanced = advanced

    def _default_is_ref(self):
        """Check if default is a reference to another var."""
        if isinstance(self.default, six.string_types):
            tmpl = self.default.replace(r'\$', '').replace('$$', '')
            return '$' in tmpl
        return False

    def _check_default(self):
        if (self.default is not None
                and not self._default_is_ref()):
            try:
                self.type(self.default)
            except Exception:
                raise DefaultValueError("Error processing default value "
                                        "%(default)s for Opt type of %(opt)s."
                                        % {'default': self.default,
                                           'opt': self.type})

    def __ne__(self, another):
        return vars(self) != vars(another)

    def __eq__(self, another):
        return vars(self) == vars(another)

    __hash__ = object.__hash__

    def _get_from_namespace(self, namespace, group_name):
        """Retrieves the option value from a _Namespace object.

        :param namespace: a _Namespace object
        :param group_name: a group name
        """
        names = [(group_name, self.dest)]
        current_name = (group_name, self.name)

        for opt in self.deprecated_opts:
            dname, dgroup = opt.name, opt.group
            if dname or dgroup:
                names.append((dgroup if dgroup else group_name,
                              dname if dname else self.dest))

        value = namespace._get_value(
            names, multi=self.multi,
            positional=self.positional, current_name=current_name)
        # The previous line will raise a KeyError if no value is set in the
        # config file, so we'll only log deprecations for set options.
        if self.deprecated_for_removal and not self._logged_deprecation:
            self._logged_deprecation = True
            pretty_group = group_name or 'DEFAULT'
            if self.deprecated_reason:
                pretty_reason = ' ({})'.format(self.deprecated_reason)
            else:
                pretty_reason = ''
            LOG.warning('Option "%(option)s" from group "%(group)s" is '
                        'deprecated for removal%(reason)s.  Its value may be '
                        'silently ignored in the future.',
                        {'option': self.dest,
                         'group': pretty_group,
                         'reason': pretty_reason})
        return value

    def _add_to_cli(self, parser, group=None):
        """Makes the option available in the command line interface.

        This is the method ConfigOpts uses to add the opt to the CLI interface
        as appropriate for the opt type. Some opt types may extend this method,
        others may just extend the helper methods it uses.

        :param parser: the CLI option parser
        :param group: an optional OptGroup object
        """
        container = self._get_argparse_container(parser, group)
        kwargs = self._get_argparse_kwargs(group)
        prefix = self._get_argparse_prefix('', group.name if group else None)
        deprecated_names = []
        for opt in self.deprecated_opts:
            deprecated_name = self._get_deprecated_cli_name(opt.name,
                                                            opt.group)
            if deprecated_name is not None:
                deprecated_names.append(deprecated_name)
        self._add_to_argparse(parser, container, self.name, self.short,
                              kwargs, prefix,
                              self.positional, deprecated_names)

    def _add_to_argparse(self, parser, container, name, short, kwargs,
                         prefix='', positional=False, deprecated_names=None):
        """Add an option to an argparse parser or group.

        :param container: an argparse._ArgumentGroup object
        :param name: the opt name
        :param short: the short opt name
        :param kwargs: the keyword arguments for add_argument()
        :param prefix: an optional prefix to prepend to the opt name
        :param positional: whether the option is a positional CLI argument
        :param deprecated_names: list of deprecated option names
        """
        def hyphen(arg):
            return arg if not positional else ''

        args = [hyphen('--') + prefix + name]
        if short:
            args.append(hyphen('-') + short)
        for deprecated_name in deprecated_names:
            args.append(hyphen('--') + deprecated_name)

        parser.add_parser_argument(container, *args, **kwargs)

    def _get_argparse_container(self, parser, group):
        """Returns an argparse._ArgumentGroup.

        :param parser: an argparse.ArgumentParser
        :param group: an (optional) OptGroup object
        :returns: an argparse._ArgumentGroup if group is given, else parser
        """
        if group is not None:
            return group._get_argparse_group(parser)
        else:
            return parser

    def _get_argparse_kwargs(self, group, **kwargs):
        r"""Build a dict of keyword arguments for argparse's add_argument().

        Most opt types extend this method to customize the behaviour of the
        options added to argparse.

        :param group: an optional group
        :param \*\*kwargs: optional keyword arguments to add to
        :returns: a dict of keyword arguments
        """
        if not self.positional:
            dest = self.dest
            if group is not None:
                dest = group.name + '_' + dest
            kwargs['dest'] = dest
        else:
            kwargs['nargs'] = '?'
        kwargs.update({'default': None,
                       'metavar': self.metavar,
                       'help': self.help, })
        return kwargs

    def _get_argparse_prefix(self, prefix, group_name):
        """Build a prefix for the CLI option name, if required.

        CLI options in a group are prefixed with the group's name in order
        to avoid conflicts between similarly named options in different
        groups.

        :param prefix: an existing prefix to append to (for example 'no' or '')
        :param group_name: an optional group name
        :returns: a CLI option prefix including the group name, if appropriate
        """
        if group_name is not None:
            return group_name + '-' + prefix
        else:
            return prefix

    def _get_deprecated_cli_name(self, dname, dgroup, prefix=''):
        """Build a CLi arg name for deprecated options.

        Either a deprecated name or a deprecated group or both or
        neither can be supplied:

          dname, dgroup -> dgroup + '-' + dname
          dname         -> dname
          dgroup        -> dgroup + '-' + self.name
          neither        -> None

        :param dname: a deprecated name, which can be None
        :param dgroup: a deprecated group, which can be None
        :param prefix: an prefix to append to (for example 'no' or '')
        :returns: a CLI argument name
        """
        if dgroup == 'DEFAULT':
            dgroup = None

        if dname is None and dgroup is None:
            return None

        if dname is None:
            dname = self.name

        return self._get_argparse_prefix(prefix, dgroup) + dname

    def __lt__(self, another):
        return hash(self) < hash(another)


class DeprecatedOpt(object):

    """Represents a Deprecated option.

    Here's how you can use it::

        oldopts = [cfg.DeprecatedOpt('oldopt1', group='group1'),
                   cfg.DeprecatedOpt('oldopt2', group='group2')]
        cfg.CONF.register_group(cfg.OptGroup('group1'))
        cfg.CONF.register_opt(cfg.StrOpt('newopt', deprecated_opts=oldopts),
                              group='group1')

    For options which have a single value (like in the example above),
    if the new option is present ("[group1]/newopt" above), it will override
    any deprecated options present ("[group1]/oldopt1" and "[group2]/oldopt2"
    above).

    If no group is specified for a DeprecatedOpt option (i.e. the group is
    None), lookup will happen within the same group the new option is in.
    For example, if no group was specified for the second option 'oldopt2' in
    oldopts list::

        oldopts = [cfg.DeprecatedOpt('oldopt1', group='group1'),
                   cfg.DeprecatedOpt('oldopt2')]
        cfg.CONF.register_group(cfg.OptGroup('group1'))
        cfg.CONF.register_opt(cfg.StrOpt('newopt', deprecated_opts=oldopts),
                              group='group1')

    then lookup for that option will happen in group 'group1'.

    If the new option is not present and multiple deprecated options are
    present, the option corresponding to the first element of deprecated_opts
    will be chosen.

    Multi-value options will return all new and deprecated
    options. So if we have a multi-value option "[group1]/opt1" whose
    deprecated option is "[group2]/opt2", and the conf file has both these
    options specified like so::

        [group1]
        opt1=val10,val11

        [group2]
        opt2=val21,val22

    Then the value of "[group1]/opt1" will be ['val11', 'val12', 'val21',
    'val22'].

    .. versionadded:: 1.2
    """

    def __init__(self, name, group=None):
        """Constructs an DeprecatedOpt object.

        :param name: the name of the option
        :param group: the group of the option
        """
        self.name = name
        self.group = group

    def __key(self):
        return (self.name, self.group)

    def __eq__(self, other):
        return self.__key() == other.__key()

    def __hash__(self):
        return hash(self.__key())


class StrOpt(Opt):
    r"""Option with String type

    Option with ``type`` :class:`oslo_config.types.String`

    :param name: the option's name
    :param choices: Optional sequence of valid values.
    :param quotes: If True and string is enclosed with single or double
                   quotes, will strip those quotes.
    :param regex: Optional regular expression (string or compiled
                  regex) that the value must match on an unanchored
                  search.
    :param ignore_case: If True case differences (uppercase vs. lowercase)
                        between 'choices' or 'regex' will be ignored.
    :param max_length: If positive integer, the value must be less than or
                       equal to this parameter.
    :param \*\*kwargs: arbitrary keyword arguments passed to :class:`Opt`

    .. versionchanged:: 2.7
       Added *quotes* parameter

    .. versionchanged:: 2.7
       Added *regex* parameter

    .. versionchanged:: 2.7
       Added *ignore_case* parameter

    .. versionchanged:: 2.7
       Added *max_length* parameter
    """

    def __init__(self, name, choices=None, quotes=None,
                 regex=None, ignore_case=None, max_length=None, **kwargs):
        super(StrOpt, self).__init__(name,
                                     type=types.String(
                                         choices=choices,
                                         quotes=quotes,
                                         regex=regex,
                                         ignore_case=ignore_case,
                                         max_length=max_length),
                                     **kwargs)


class BoolOpt(Opt):

    r"""Boolean options.

    Bool opts are set to True or False on the command line using --optname or
    --nooptname respectively.

    In config files, boolean values are cast with Boolean type.

    :param name: the option's name
    :param \*\*kwargs: arbitrary keyword arguments passed to :class:`Opt`
    """

    def __init__(self, name, **kwargs):
        if 'positional' in kwargs:
            raise ValueError('positional boolean args not supported')
        super(BoolOpt, self).__init__(name, type=types.Boolean(), **kwargs)

    def _add_to_cli(self, parser, group=None):
        """Extends the base class method to add the --nooptname option."""
        super(BoolOpt, self)._add_to_cli(parser, group)
        self._add_inverse_to_argparse(parser, group)

    def _add_inverse_to_argparse(self, parser, group):
        """Add the --nooptname option to the option parser."""
        container = self._get_argparse_container(parser, group)
        kwargs = self._get_argparse_kwargs(group, action='store_false')
        prefix = self._get_argparse_prefix('no', group.name if group else None)
        deprecated_names = []
        for opt in self.deprecated_opts:
            deprecated_name = self._get_deprecated_cli_name(opt.name,
                                                            opt.group,
                                                            prefix='no')
            if deprecated_name is not None:
                deprecated_names.append(deprecated_name)
        kwargs["help"] = "The inverse of --" + self.name
        self._add_to_argparse(parser, container, self.name, None, kwargs,
                              prefix, self.positional, deprecated_names)

    def _get_argparse_kwargs(self, group, action='store_true', **kwargs):
        """Extends the base argparse keyword dict for boolean options."""

        kwargs = super(BoolOpt, self)._get_argparse_kwargs(group, **kwargs)
        # type has no effect for BoolOpt, it only matters for
        # values that came from config files
        if 'type' in kwargs:
            del kwargs['type']

        # metavar has no effect for BoolOpt
        if 'metavar' in kwargs:
            del kwargs['metavar']

        kwargs['action'] = action

        return kwargs


class IntOpt(Opt):

    r"""Option with Integer type

    Option with ``type`` :class:`oslo_config.types.Integer`

    :param name: the option's name
    :param min: minimum value the integer can take
    :param max: maximum value the integer can take
    :param \*\*kwargs: arbitrary keyword arguments passed to :class:`Opt`

    .. versionchanged:: 1.15

       Added *min* and *max* parameters.
    """

    def __init__(self, name, min=None, max=None, **kwargs):
        super(IntOpt, self).__init__(name, type=types.Integer(min, max),
                                     **kwargs)


class FloatOpt(Opt):

    r"""Option with Float type

    Option with ``type`` :class:`oslo_config.types.Float`

    :param name: the option's name
    :param min: minimum value the float can take
    :param max: maximum value the float can take
    :param \*\*kwargs: arbitrary keyword arguments passed to :class:`Opt`

    .. versionchanged:: 3.14

       Added *min* and *max* parameters.
    """

    def __init__(self, name, min=None, max=None, **kwargs):
        super(FloatOpt, self).__init__(name, type=types.Float(min, max),
                                       **kwargs)


class ListOpt(Opt):

    r"""Option with List(String) type

    Option with ``type`` :class:`oslo_config.types.List`

    :param name: the option's name
    :param item_type: type of items (see :class:`oslo_config.types`)
    :param bounds: if True the value should be inside "[" and "]" pair
    :param \*\*kwargs: arbitrary keyword arguments passed to :class:`Opt`

    .. versionchanged:: 2.5
       Added *item_type* and *bounds* parameters.
    """

    def __init__(self, name, item_type=None, bounds=None, **kwargs):
        super(ListOpt, self).__init__(name,
                                      type=types.List(item_type=item_type,
                                                      bounds=bounds),
                                      **kwargs)


class DictOpt(Opt):

    r"""Option with Dict(String) type

    Option with ``type`` :class:`oslo_config.types.Dict`

    :param name: the option's name
    :param \*\*kwargs: arbitrary keyword arguments passed to :class:`Opt`

    .. versionadded:: 1.2
    """

    def __init__(self, name, **kwargs):
        super(DictOpt, self).__init__(name, type=types.Dict(), **kwargs)


class IPOpt(Opt):

    r"""Opt with IPAddress type

    Option with ``type`` :class:`oslo_config.types.IPAddress`

    :param name: the option's name
    :param version: one of either ``4``, ``6``, or ``None`` to specify
       either version.
    :param \*\*kwargs: arbitrary keyword arguments passed to :class:`Opt`

    .. versionadded:: 1.4
    """

    def __init__(self, name, version=None, **kwargs):
        super(IPOpt, self).__init__(name, type=types.IPAddress(version),
                                    **kwargs)


class PortOpt(Opt):

    r"""Option for a TCP/IP port number.  Ports can range from 0 to 65535.

    Option with ``type`` :class:`oslo_config.types.Integer`

    :param name: the option's name
    :param min: minimum value the port can take
    :param max: maximum value the port can take
    :param choices: Optional sequence of valid values.
    :param \*\*kwargs: arbitrary keyword arguments passed to :class:`Opt`

    .. versionadded:: 2.6
    .. versionchanged:: 3.2
       Added *choices* parameter.
    .. versionchanged:: 3.4
       Allow port number with 0.
    .. versionchanged:: 3.16
       Added *min* and *max* parameters.
    """

    def __init__(self, name, min=None, max=None, choices=None, **kwargs):
        type = types.Port(min=min, max=max, choices=choices,
                          type_name='port value')
        super(PortOpt, self).__init__(name, type=type, **kwargs)


class HostnameOpt(Opt):

    r"""Option for a hostname.  Only accepts valid hostnames.

    Option with ``type`` :class:`oslo_config.types.Hostname`

    :param name: the option's name
    :param \*\*kwargs: arbitrary keyword arguments passed to :class:`Opt`

    .. versionadded:: 3.8
    """

    def __init__(self, name, **kwargs):
        super(HostnameOpt, self).__init__(name, type=types.Hostname(),
                                          **kwargs)


class HostAddressOpt(Opt):

    r"""Option for either an IP or a hostname.

    Accepts valid hostnames and valid IP addresses.

    Option with ``type`` :class:`oslo_config.types.HostAddress`

    :param name: the option's name
    :param version: one of either ``4``, ``6``, or ``None`` to specify
       either version.
    :param \*\*kwargs: arbitrary keyword arguments passed to :class:`Opt`

    .. versionadded:: 3.22
    """

    def __init__(self, name, version=None, **kwargs):
        super(HostAddressOpt, self).__init__(name,
                                             type=types.HostAddress(version),
                                             **kwargs)


class URIOpt(Opt):

    r"""Opt with URI type

    Option with ``type`` :class:`oslo_config.types.URI`

    :param name: the option's name
    :param max_length: If positive integer, the value must be less than or
                       equal to this parameter.
    :param schemes: list of valid URI schemes, e.g. 'https', 'ftp', 'git'
    :param \*\*kwargs: arbitrary keyword arguments passed to :class:`Opt`

    .. versionadded:: 3.12

    .. versionchanged:: 3.14
       Added *max_length* parameter
    .. versionchanged:: 3.18
       Added *schemes* parameter
    """

    def __init__(self, name, max_length=None, schemes=None, **kwargs):
        type = types.URI(max_length=max_length, schemes=schemes)
        super(URIOpt, self).__init__(name, type=type, **kwargs)


class MultiOpt(Opt):

    r"""Multi-value option.

    Multi opt values are typed opts which may be specified multiple times.
    The opt value is a list containing all the values specified.

    :param name: the option's name
    :param item_type: Type of items (see :class:`oslo_config.types`)
    :param \*\*kwargs: arbitrary keyword arguments passed to :class:`Opt`

    For example::

       cfg.MultiOpt('foo',
                    item_type=types.Integer(),
                    default=None,
                    help="Multiple foo option")

    The command line ``--foo=1 --foo=2`` would result in ``cfg.CONF.foo``
    containing ``[1,2]``

    .. versionadded:: 1.3
    """
    multi = True

    def __init__(self, name, item_type, **kwargs):
        super(MultiOpt, self).__init__(name, item_type, **kwargs)

    def _get_argparse_kwargs(self, group, **kwargs):
        """Extends the base argparse keyword dict for multi value options."""
        kwargs = super(MultiOpt, self)._get_argparse_kwargs(group)
        if not self.positional:
            kwargs['action'] = 'append'
        else:
            kwargs['nargs'] = '*'
        return kwargs


class MultiStrOpt(MultiOpt):

    r"""MultiOpt with a MultiString ``item_type``.

    MultiOpt with a default :class:`oslo_config.types.MultiString` item
    type.

    :param name: the option's name
    :param \*\*kwargs: arbitrary keyword arguments passed to :class:`MultiOpt`
    """

    def __init__(self, name, **kwargs):
        super(MultiStrOpt, self).__init__(name,
                                          item_type=types.MultiString(),
                                          **kwargs)


class SubCommandOpt(Opt):

    """Sub-command options.

    Sub-command options allow argparse sub-parsers to be used to parse
    additional command line arguments.

    The handler argument to the SubCommandOpt constructor is a callable
    which is supplied an argparse subparsers object. Use this handler
    callable to add sub-parsers.

    The opt value is SubCommandAttr object with the name of the chosen
    sub-parser stored in the 'name' attribute and the values of other
    sub-parser arguments available as additional attributes.

    :param name: the option's name
    :param dest: the name of the corresponding :class:`.ConfigOpts` property
    :param handler: callable which is supplied subparsers object when invoked
    :param title: title of the sub-commands group in help output
    :param description: description of the group in help output
    :param help: a help string giving an overview of available sub-commands
    """

    def __init__(self, name, dest=None, handler=None,
                 title=None, description=None, help=None):
        """Construct an sub-command parsing option.

        This behaves similarly to other Opt sub-classes but adds a
        'handler' argument. The handler is a callable which is supplied
        an subparsers object when invoked. The add_parser() method on
        this subparsers object can be used to register parsers for
        sub-commands.
        """
        super(SubCommandOpt, self).__init__(name, type=types.String(),
                                            dest=dest, help=help)
        self.handler = handler
        self.title = title
        self.description = description

    def _add_to_cli(self, parser, group=None):
        """Add argparse sub-parsers and invoke the handler method."""
        dest = self.dest
        if group is not None:
            dest = group.name + '_' + dest

        subparsers = parser.add_subparsers(dest=dest,
                                           title=self.title,
                                           description=self.description,
                                           help=self.help)
        # NOTE(jd) Set explicitly to True for Python 3
        # See http://bugs.python.org/issue9253 for context
        subparsers.required = True

        if self.handler is not None:
            self.handler(subparsers)


class _ConfigFileOpt(Opt):

    """The --config-file option.

    This is an private option type which handles the special processing
    required for --config-file options.

    As each --config-file option is encountered on the command line, we
    parse the file and store the parsed values in the _Namespace object.
    This allows us to properly handle the precedence of --config-file
    options over previous command line arguments, but not over subsequent
    arguments.

    .. versionadded:: 1.2
    """

    class ConfigFileAction(argparse.Action):

        """An argparse action for --config-file.

        As each --config-file option is encountered, this action adds the
        value to the config_file attribute on the _Namespace object but also
        parses the configuration file and stores the values found also in
        the _Namespace object.
        """

        def __call__(self, parser, namespace, values, option_string=None):
            """Handle a --config-file command line argument.

            :raises: ConfigFileParseError, ConfigFileValueError
            """
            if getattr(namespace, self.dest, None) is None:
                setattr(namespace, self.dest, [])
            items = getattr(namespace, self.dest)
            items.append(values)

            ConfigParser._parse_file(values, namespace)

    def __init__(self, name, **kwargs):
        super(_ConfigFileOpt, self).__init__(name, lambda x: x, **kwargs)

    def _get_argparse_kwargs(self, group, **kwargs):
        """Extends the base argparse keyword dict for the config file opt."""
        kwargs = super(_ConfigFileOpt, self)._get_argparse_kwargs(group)
        kwargs['action'] = self.ConfigFileAction
        return kwargs


class _ConfigDirOpt(Opt):

    """The --config-dir option.

    This is an private option type which handles the special processing
    required for --config-dir options.

    As each --config-dir option is encountered on the command line, we
    parse the files in that directory and store the parsed values in the
    _Namespace object. This allows us to properly handle the precedence of
    --config-dir options over previous command line arguments, but not
    over subsequent arguments.

    .. versionadded:: 1.2
    """

    class ConfigDirAction(argparse.Action):

        """An argparse action for --config-dir.

        As each --config-dir option is encountered, this action sets the
        config_dir attribute on the _Namespace object but also parses the
        configuration files and stores the values found also in the
        _Namespace object.
        """

        def __call__(self, parser, namespace, values, option_string=None):
            """Handle a --config-dir command line argument.

            :raises: ConfigFileParseError, ConfigFileValueError,
                     ConfigDirNotFoundError
            """
            namespace._config_dirs.append(values)
            setattr(namespace, self.dest, values)

            values = os.path.expanduser(values)

            if not os.path.exists(values):
                raise ConfigDirNotFoundError(values)

            config_dir_glob = os.path.join(values, '*.conf')

            for config_file in sorted(glob.glob(config_dir_glob)):
                ConfigParser._parse_file(config_file, namespace)

    def __init__(self, name, **kwargs):
        super(_ConfigDirOpt, self).__init__(name, type=types.List(),
                                            **kwargs)

    def _get_argparse_kwargs(self, group, **kwargs):
        """Extends the base argparse keyword dict for the config dir option."""
        kwargs = super(_ConfigDirOpt, self)._get_argparse_kwargs(group)
        kwargs['action'] = self.ConfigDirAction
        return kwargs


class OptGroup(object):

    """Represents a group of opts.

    CLI opts in the group are automatically prefixed with the group name.

    Each group corresponds to a section in config files.

    An OptGroup object has no public methods, but has a number of public string
    properties:

    .. py:attribute:: name

        the name of the group

    .. py:attribute:: title

        the group title as displayed in --help

    .. py:attribute:: help

        the group description as displayed in --help

    :param name: the group name
    :type name: str
    :param title: the group title for --help
    :type title: str
    :param help: the group description for --help
    :type help: str
    :param dynamic_group_owner: The name of the option that controls
                                repeated instances of this group.
    :type dynamic_group_owner: str
    :param driver_option: The name of the option within the group that
                          controls which driver will register options.
    :type driver_option: str

    """

    def __init__(self, name, title=None, help=None,
                 dynamic_group_owner='',
                 driver_option=''):
        """Constructs an OptGroup object."""
        self.name = name
        self.title = "%s options" % name if title is None else title
        self.help = help
        self.dynamic_group_owner = dynamic_group_owner
        self.driver_option = driver_option

        self._opts = {}  # dict of dicts of (opt:, override:, default:)
        self._argparse_group = None
        self._driver_opts = {}  # populated by the config generator

    def _save_driver_opts(self, opts):
        """Save known driver opts.

        :param opts: mapping between driver name and list of opts
        :type opts: dict

        """
        self._driver_opts.update(opts)

    def _get_generator_data(self):
        "Return a dict with data for the sample generator."
        return {
            'help': self.help or '',
            'dynamic_group_owner': self.dynamic_group_owner,
            'driver_option': self.driver_option,
            'driver_opts': self._driver_opts,
        }

    def _register_opt(self, opt, cli=False):
        """Add an opt to this group.

        :param opt: an Opt object
        :param cli: whether this is a CLI option
        :returns: False if previously registered, True otherwise
        :raises: DuplicateOptError if a naming conflict is detected
        """
        if _is_opt_registered(self._opts, opt):
            return False

        self._opts[opt.dest] = {'opt': opt, 'cli': cli}

        return True

    def _unregister_opt(self, opt):
        """Remove an opt from this group.

        :param opt: an Opt object
        """
        if opt.dest in self._opts:
            del self._opts[opt.dest]

    def _get_argparse_group(self, parser):
        if self._argparse_group is None:
            """Build an argparse._ArgumentGroup for this group."""
            self._argparse_group = parser.add_argument_group(self.title,
                                                             self.help)
        return self._argparse_group

    def _clear(self):
        """Clear this group's option parsing state."""
        self._argparse_group = None


class ParseError(iniparser.ParseError):
    def __init__(self, msg, lineno, line, filename):
        super(ParseError, self).__init__(msg, lineno, line)
        self.filename = filename

    def __str__(self):
        return 'at %s:%d, %s: %r' % (self.filename, self.lineno,
                                     self.msg, self.line)


class ConfigParser(iniparser.BaseParser):
    """Parses a single config file, populating 'sections' to look like:

        {'DEFAULT': {'key': [value, ...], ...},
         ...}

       Also populates self._normalized which looks the same but with normalized
       section names.
    """

    def __init__(self, filename, sections):
        super(ConfigParser, self).__init__()
        self.filename = filename
        self.sections = sections
        self._normalized = None
        self.section = None

    def _add_normalized(self, normalized):
        self._normalized = normalized

    def parse(self):
        with open(self.filename) as f:
            return super(ConfigParser, self).parse(f)

    def new_section(self, section):
        self.section = section
        self.sections.setdefault(self.section, {})

        if self._normalized is not None:
            self._normalized.setdefault(_normalize_group_name(self.section),
                                        {})

    def assignment(self, key, value):
        if not self.section:
            raise self.error_no_section()

        value = '\n'.join(value)

        def append(sections, section):
            sections[section].setdefault(key, [])
            sections[section][key].append(value)

        append(self.sections, self.section)
        if self._normalized is not None:
            append(self._normalized, _normalize_group_name(self.section))

    def parse_exc(self, msg, lineno, line=None):
        return ParseError(msg, lineno, line, self.filename)

    def error_no_section(self):
        return self.parse_exc('Section must be started before assignment',
                              self.lineno)

    @classmethod
    def _parse_file(cls, config_file, namespace):
        """Parse a config file and store any values in the namespace.

        :raises: ConfigFileParseError, ConfigFileValueError
        """
        config_file = _fixpath(config_file)

        sections = {}
        normalized = {}
        parser = cls(config_file, sections)
        parser._add_normalized(normalized)

        try:
            parser.parse()
        except iniparser.ParseError as pe:
            raise ConfigFileParseError(pe.filename, str(pe))
        except IOError as err:
            if err.errno == errno.ENOENT:
                namespace._file_not_found(config_file)
                return
            if err.errno == errno.EACCES:
                namespace._file_permission_denied(config_file)
                return
            raise

        namespace._add_parsed_config_file(sections, normalized)
        namespace._parse_cli_opts_from_config_file(sections, normalized)


@removals.remove(version='3.4', removal_version='4.0')
class MultiConfigParser(object):
    """A ConfigParser which handles multi-opts.

    All methods in this class which accept config names should treat a section
    name of None as 'DEFAULT'.

    This class was deprecated in Mitaka and should be removed in Ocata.
    _Namespace holds values, ConfigParser._parse_file reads one file into a
    _Namespace and ConfigOpts._parse_config_files reads multiple files into a
    _Namespace.
    """

    _deprecated_opt_message = ('Option "%(dep_option)s" from group '
                               '"%(dep_group)s" is deprecated. Use option '
                               '"%(option)s" from group "%(group)s".')

    def __init__(self):
        self.parsed = []
        self._normalized = []
        self._emitted_deprecations = set()

    def read(self, config_files):
        read_ok = []

        for filename in config_files:
            sections = {}
            normalized = {}
            parser = ConfigParser(filename, sections)
            parser._add_normalized(normalized)

            try:
                parser.parse()
            except IOError:
                continue
            self._add_parsed_config_file(sections, normalized)
            read_ok.append(filename)

        return read_ok

    def _add_parsed_config_file(self, sections, normalized):
        """Add a parsed config file to the list of parsed files.

        :param sections: a mapping of section name to dicts of config values
        :param normalized: sections mapping with section names normalized
        :raises: ConfigFileValueError
        """
        self.parsed.insert(0, sections)
        self._normalized.insert(0, normalized)

    def get(self, names, multi=False):
        return self._get(names, multi=multi)

    def _get(self, names, multi=False, normalized=False, current_name=None):
        """Fetch a config file value from the parsed files.

        :param names: a list of (section, name) tuples
        :param multi: a boolean indicating whether to return multiple values
        :param normalized: whether to normalize group names to lowercase
        :param current_name: current name in tuple being checked
        """
        rvalue = []

        def normalize(name):
            if name is None:
                name = 'DEFAULT'
            return _normalize_group_name(name) if normalized else name

        names = [(normalize(section), name) for section, name in names]

        for sections in (self._normalized if normalized else self.parsed):
            for section, name in names:
                if section not in sections:
                    continue
                if name in sections[section]:
                    current_name = current_name or names[0]
                    self._check_deprecated((section, name), current_name,
                                           names[1:])
                    val = sections[section][name]
                    if multi:
                        rvalue = val + rvalue
                    else:
                        return val
        if multi and rvalue != []:
            return rvalue
        raise KeyError

    def _check_deprecated(self, name, current, deprecated):
        """Check for usage of deprecated names.

        :param name: A tuple of the form (group, name) representing the group
                     and name where an opt value was found.
        :param current: A tuple of the form (group, name) representing the
                        current name for an option.
        :param deprecated: A list of tuples with the same format as the name
                    param which represent any deprecated names for an option.
                    If the name param matches any entries in this list a
                    deprecation warning will be logged.
        """
        if name in deprecated and name not in self._emitted_deprecations:
            self._emitted_deprecations.add(name)
            current = (current[0] or 'DEFAULT', current[1])
            # NOTE(bnemec): Not using versionutils for this to avoid a
            # circular dependency between oslo.config and whatever library
            # versionutils ends up in.
            LOG.warning(self._deprecated_opt_message,
                        {'dep_option': name[1], 'dep_group': name[0],
                         'option': current[1], 'group': current[0]})


class _Namespace(argparse.Namespace):
    """An argparse namespace which also stores config file values.

    As we parse command line arguments, the values get set as attributes
    on a namespace object. However, we also want to parse config files as
    they are specified on the command line and collect the values alongside
    the option values parsed from the command line.

    Note, we don't actually assign values from config files as attributes
    on the namespace because config file options be registered after the
    command line has been parsed, so we may not know how to properly parse
    or convert a config file value at this point.
    """

    _deprecated_opt_message = ('Option "%(dep_option)s" from group '
                               '"%(dep_group)s" is deprecated. Use option '
                               '"%(option)s" from group "%(group)s".')

    def __init__(self, conf):
        self._conf = conf
        self._parsed = []
        self._normalized = []
        self._emitted_deprecations = set()
        self._files_not_found = []
        self._files_permission_denied = []
        self._config_dirs = []

    def _parse_cli_opts_from_config_file(self, sections, normalized):
        """Parse CLI options from a config file.

        CLI options are special - we require they be registered before the
        command line is parsed. This means that as we parse config files, we
        can go ahead and apply the appropriate option-type specific conversion
        to the values in config files for CLI options. We can't do this for
        non-CLI options, because the schema describing those options may not be
        registered until after the config files are parsed.

        This method relies on that invariant in order to enforce proper
        priority of option values - i.e. that the order in which an option
        value is parsed, whether the value comes from the CLI or a config file,
        determines which value specified for a given option wins.

        The way we implement this ordering is that as we parse each config
        file, we look for values in that config file for CLI options only. Any
        values for CLI options found in the config file are treated like they
        had appeared on the command line and set as attributes on the namespace
        objects. Values in later config files or on the command line will
        override values found in this file.
        """
        namespace = _Namespace(self._conf)
        namespace._add_parsed_config_file(sections, normalized)

        for opt, group in self._conf._all_cli_opts():
            group_name = group.name if group is not None else None
            try:
                value = opt._get_from_namespace(namespace, group_name)
            except KeyError:
                continue
            except ValueError as ve:
                raise ConfigFileValueError(
                    "Value for option %s is not valid: %s"
                    % (opt.name, str(ve)))

            if group_name is None:
                dest = opt.dest
            else:
                dest = group_name + '_' + opt.dest

            if opt.multi:
                if getattr(self, dest, None) is None:
                    setattr(self, dest, [])
                values = getattr(self, dest)
                values.extend(value)
            else:
                setattr(self, dest, value)

    def _add_parsed_config_file(self, sections, normalized):
        """Add a parsed config file to the list of parsed files.

        :param sections: a mapping of section name to dicts of config values
        :param normalized: sections mapping with section names normalized
        :raises: ConfigFileValueError
        """
        self._parsed.insert(0, sections)
        self._normalized.insert(0, normalized)

    def _file_not_found(self, config_file):
        """Record that we were unable to open a config file.

        :param config_file: the path to the failed file
        """
        self._files_not_found.append(config_file)

    def _file_permission_denied(self, config_file):
        """Record that we have no permission to open a config file.

        :param config_file: the path to the failed file
        """
        self._files_permission_denied.append(config_file)

    def _get_cli_value(self, names, positional=False):
        """Fetch a CLI option value.

        Look up the value of a CLI option. The value itself may have come from
        parsing the command line or parsing config files specified on the
        command line. Type conversion have already been performed for CLI
        options at this point.

        :param names: a list of (section, name) tuples
        :param positional: whether this is a positional option
        """
        for group_name, name in names:
            name = name if group_name is None else group_name + '_' + name
            value = getattr(self, name, None)
            if value is not None:
                # argparse ignores default=None for nargs='*' and returns []
                if positional and not value:
                    continue

                return value

        raise KeyError

    def _get_file_value(
            self, names, multi=False, normalized=False, current_name=None):
        """Fetch a config file value from the parsed files.

        :param names: a list of (section, name) tuples
        :param multi: a boolean indicating whether to return multiple values
        :param normalized: whether to normalize group names to lowercase
        :param current_name: current name in tuple being checked
        """
        rvalue = []

        def normalize(name):
            if name is None:
                name = 'DEFAULT'
            return _normalize_group_name(name) if normalized else name

        names = [(normalize(section), name) for section, name in names]

        for sections in (self._normalized if normalized else self._parsed):
            for section, name in names:
                if section not in sections:
                    continue
                if name in sections[section]:
                    current_name = current_name or names[0]
                    self._check_deprecated((section, name), current_name,
                                           names[1:])
                    val = sections[section][name]
                    if multi:
                        rvalue = val + rvalue
                    else:
                        return val
        if multi and rvalue != []:
            return rvalue
        raise KeyError

    def _check_deprecated(self, name, current, deprecated):
        """Check for usage of deprecated names.

        :param name: A tuple of the form (group, name) representing the group
                     and name where an opt value was found.
        :param current: A tuple of the form (group, name) representing the
                        current name for an option.
        :param deprecated: A list of tuples with the same format as the name
                    param which represent any deprecated names for an option.
                    If the name param matches any entries in this list a
                    deprecation warning will be logged.
        """
        if name in deprecated and name not in self._emitted_deprecations:
            self._emitted_deprecations.add(name)
            current = (current[0] or 'DEFAULT', current[1])
            # NOTE(bnemec): Not using versionutils for this to avoid a
            # circular dependency between oslo.config and whatever library
            # versionutils ends up in.
            LOG.warning(self._deprecated_opt_message,
                        {'dep_option': name[1], 'dep_group': name[0],
                         'option': current[1], 'group': current[0]})

    def _get_value(self, names, multi=False, positional=False,
                   current_name=None, normalized=True):
        """Fetch a value from config files.

        Multiple names for a given configuration option may be supplied so
        that we can transparently handle files containing deprecated option
        names or groups.

        :param names: a list of (section, name) tuples
        :param positional: whether this is a positional option
        :param multi: a boolean indicating whether to return multiple values
        :param normalized: whether to normalize group names to lowercase
        """
        try:
            return self._get_cli_value(names, positional)
        except KeyError:
            names = [(g if g is not None else 'DEFAULT', n) for g, n in names]
            values = self._get_file_value(
                names, multi=multi, normalized=normalized,
                current_name=current_name)
            return values if multi else values[-1]

    def _sections(self):
        for sections in self._parsed:
            for section in sections:
                yield section


class _CachedArgumentParser(argparse.ArgumentParser):

    """class for caching/collecting command line arguments.

    It also sorts the arguments before initializing the ArgumentParser.
    We need to do this since ArgumentParser by default does not sort
    the argument options and the only way to influence the order of
    arguments in '--help' is to ensure they are added in the sorted
    order.
    """

    def __init__(self, prog=None, usage=None, **kwargs):
        super(_CachedArgumentParser, self).__init__(prog, usage, **kwargs)
        self._args_cache = {}

    def add_parser_argument(self, container, *args, **kwargs):
        values = []
        if container in self._args_cache:
            values = self._args_cache[container]
        values.append({'args': args, 'kwargs': kwargs})
        self._args_cache[container] = values

    def initialize_parser_arguments(self):
        # NOTE(mfedosin): The code below looks a little bit weird, but
        # it's done because we need to sort only optional opts and do
        # not touch positional. For the reason optional opts go first in
        # the values we only need to find an index of the first positional
        # option and then sort the values slice.
        for container, values in self._args_cache.items():
            index = 0
            has_positional = False
            for index, argument in enumerate(values):
                if not argument['args'][0].startswith('-'):
                    has_positional = True
                    break
            size = index if has_positional else len(values)
            values[:size] = sorted(values[:size], key=lambda x: x['args'])
            for argument in values:
                try:
                    container.add_argument(*argument['args'],
                                           **argument['kwargs'])
                except argparse.ArgumentError:
                    options = ','.join(argument['args'])
                    raise DuplicateOptError(options)
        self._args_cache = {}

    def parse_args(self, args=None, namespace=None):
        self.initialize_parser_arguments()
        return super(_CachedArgumentParser, self).parse_args(args, namespace)

    def print_help(self, file=None):
        self.initialize_parser_arguments()
        super(_CachedArgumentParser, self).print_help(file)

    def print_usage(self, file=None):
        self.initialize_parser_arguments()
        super(_CachedArgumentParser, self).print_usage(file)


class ConfigOpts(collections.Mapping):

    """Config options which may be set on the command line or in config files.

    ConfigOpts is a configuration option manager with APIs for registering
    option schemas, grouping options, parsing option values and retrieving
    the values of options.

    It has built-in support for :oslo.config:option:`config_file` and
    :oslo.config:option:`config_dir` options.

    """
    disallow_names = ('project', 'prog', 'version',
                      'usage', 'default_config_files', 'default_config_dirs')

    def __init__(self):
        """Construct a ConfigOpts object."""
        self._opts = {}  # dict of dicts of (opt:, override:, default:)
        self._groups = {}
        self._deprecated_opts = {}

        self._args = None

        self._oparser = None
        self._namespace = None
        self._mutable_ns = None
        self._mutate_hooks = set([])
        self.__cache = {}
        self._config_opts = []
        self._cli_opts = collections.deque()
        self._validate_default_values = False

    def _pre_setup(self, project, prog, version, usage, description, epilog,
                   default_config_files, default_config_dirs):
        """Initialize a ConfigCliParser object for option parsing."""

        if prog is None:
            prog = os.path.basename(sys.argv[0])
            if prog.endswith(".py"):
                prog = prog[:-3]

        if default_config_files is None:
            default_config_files = find_config_files(project, prog)

        if default_config_dirs is None:
            default_config_dirs = find_config_dirs(project, prog)

        self._oparser = _CachedArgumentParser(
            prog=prog, usage=usage, description=description, epilog=epilog)

        if version is not None:
            self._oparser.add_parser_argument(self._oparser,
                                              '--version',
                                              action='version',
                                              version=version)

        return prog, default_config_files, default_config_dirs

    @staticmethod
    def _make_config_options(default_config_files, default_config_dirs):
        return [
            _ConfigFileOpt('config-file',
                           default=default_config_files,
                           metavar='PATH',
                           help=('Path to a config file to use. Multiple '
                                 'config files can be specified, with values '
                                 'in later files taking precedence. Defaults '
                                 'to %(default)s.')),
            _ConfigDirOpt('config-dir',
                          metavar='DIR',
                          default=default_config_dirs,
                          help='Path to a config directory to pull `*.conf` '
                               'files from. This file set is sorted, so as to '
                               'provide a predictable parse order if '
                               'individual options are over-ridden. The set '
                               'is parsed after the file(s) specified via '
                               'previous --config-file, arguments hence '
                               'over-ridden options in the directory take '
                               'precedence.'),
        ]

    def _setup(self, project, prog, version, usage, default_config_files,
               default_config_dirs):
        """Initialize a ConfigOpts object for option parsing."""
        self._config_opts = self._make_config_options(default_config_files,
                                                      default_config_dirs)
        self.register_cli_opts(self._config_opts)

        self.project = project
        self.prog = prog
        self.version = version
        self.usage = usage
        self.default_config_files = default_config_files
        self.default_config_dirs = default_config_dirs

    def __clear_cache(f):
        @functools.wraps(f)
        def __inner(self, *args, **kwargs):
            if kwargs.pop('clear_cache', True):
                result = f(self, *args, **kwargs)
                self.__cache.clear()
                return result
            else:
                return f(self, *args, **kwargs)

        return __inner

    def __call__(self,
                 args=None,
                 project=None,
                 prog=None,
                 version=None,
                 usage=None,
                 default_config_files=None,
                 default_config_dirs=None,
                 validate_default_values=False,
                 description=None,
                 epilog=None):
        """Parse command line arguments and config files.

        Calling a ConfigOpts object causes the supplied command line arguments
        and config files to be parsed, causing opt values to be made available
        as attributes of the object.

        The object may be called multiple times, each time causing the previous
        set of values to be overwritten.

        Automatically registers the --config-file option with either a supplied
        list of default config files, or a list from find_config_files().

        If the --config-dir option is set, any *.conf files from this
        directory are pulled in, after all the file(s) specified by the
        --config-file option.

        :param args: command line arguments (defaults to sys.argv[1:])
        :param project: the toplevel project name, used to locate config files
        :param prog: the name of the program (defaults to sys.argv[0]
            basename, without extension .py)
        :param version: the program version (for --version)
        :param usage: a usage string (%prog will be expanded)
        :param description: A description of what the program does
        :param epilog: Text following the argument descriptions
        :param default_config_files: config files to use by default
        :param default_config_dirs: config dirs to use by default
        :param validate_default_values: whether to validate the default values
        :raises: SystemExit, ConfigFilesNotFoundError, ConfigFileParseError,
                 ConfigFilesPermissionDeniedError,
                 RequiredOptError, DuplicateOptError
        """
        self.clear()

        self._validate_default_values = validate_default_values

        prog, default_config_files, default_config_dirs = self._pre_setup(
            project, prog, version, usage, description, epilog,
            default_config_files, default_config_dirs)

        self._setup(project, prog, version, usage, default_config_files,
                    default_config_dirs)

        self._namespace = self._parse_cli_opts(args if args is not None
                                               else sys.argv[1:])
        if self._namespace._files_not_found:
            raise ConfigFilesNotFoundError(self._namespace._files_not_found)
        if self._namespace._files_permission_denied:
            raise ConfigFilesPermissionDeniedError(
                self._namespace._files_permission_denied)

        self._check_required_opts()

    def __getattr__(self, name):
        """Look up an option value and perform string substitution.

        :param name: the opt name (or 'dest', more precisely)
        :returns: the option value (after string substitution) or a GroupAttr
        :raises: ValueError or NoSuchOptError
        """
        try:
            return self._get(name)
        except ValueError:
            raise
        except Exception:
            raise NoSuchOptError(name)

    def __getitem__(self, key):
        """Look up an option value and perform string substitution."""
        return self.__getattr__(key)

    def __contains__(self, key):
        """Return True if key is the name of a registered opt or group."""
        return key in self._opts or key in self._groups

    def __iter__(self):
        """Iterate over all registered opt and group names."""
        for key in itertools.chain(self._opts.keys(), self._groups.keys()):
            yield key

    def __len__(self):
        """Return the number of options and option groups."""
        return len(self._opts) + len(self._groups)

    def reset(self):
        """Clear the object state and unset overrides and defaults."""
        self._unset_defaults_and_overrides()
        self.clear()

    @__clear_cache
    def clear(self):
        """Reset the state of the object to before options were registered.

        This method removes all registered options and discards the data
        from the command line and configuration files.

        Any subparsers added using the add_cli_subparsers() will also be
        removed as a side-effect of this method.
        """
        self._args = None
        self._oparser = None
        self._namespace = None
        self._mutable_ns = None
        # Keep _mutate_hooks
        self._validate_default_values = False
        self.unregister_opts(self._config_opts)
        for group in self._groups.values():
            group._clear()

    def _add_cli_opt(self, opt, group):
        if {'opt': opt, 'group': group} in self._cli_opts:
            return
        if opt.positional:
            self._cli_opts.append({'opt': opt, 'group': group})
        else:
            self._cli_opts.appendleft({'opt': opt, 'group': group})

    def _track_deprecated_opts(self, opt, group=None):
        if hasattr(opt, 'deprecated_opts'):
            for dep_opt in opt.deprecated_opts:
                dep_group = dep_opt.group or 'DEFAULT'
                dep_dest = dep_opt.name
                if dep_dest:
                    dep_dest = dep_dest.replace('-', '_')
                if dep_group not in self._deprecated_opts:
                    self._deprecated_opts[dep_group] = {
                        dep_dest: {
                            'opt': opt,
                            'group': group
                        }
                    }
                else:
                    self._deprecated_opts[dep_group][dep_dest] = {
                        'opt': opt,
                        'group': group
                    }

    @__clear_cache
    def register_opt(self, opt, group=None, cli=False):
        """Register an option schema.

        Registering an option schema makes any option value which is previously
        or subsequently parsed from the command line or config files available
        as an attribute of this object.

        :param opt: an instance of an Opt sub-class
        :param group: an optional OptGroup object or group name
        :param cli: whether this is a CLI option
        :return: False if the opt was already registered, True otherwise
        :raises: DuplicateOptError
        """
        if group is not None:
            group = self._get_group(group, autocreate=True)
            if cli:
                self._add_cli_opt(opt, group)
            self._track_deprecated_opts(opt, group=group)
            return group._register_opt(opt, cli)

        # NOTE(gcb) We can't use some names which are same with attributes of
        # Opts in default group. They includes project, prog, version, usage,
        # default_config_files and default_config_dirs.
        if group is None:
            if opt.name in self.disallow_names:
                raise ValueError('Name %s was reserved for oslo.config.'
                                 % opt.name)

        if cli:
            self._add_cli_opt(opt, None)

        if _is_opt_registered(self._opts, opt):
            return False

        self._opts[opt.dest] = {'opt': opt, 'cli': cli}
        self._track_deprecated_opts(opt)
        return True

    @__clear_cache
    def register_opts(self, opts, group=None):
        """Register multiple option schemas at once."""
        for opt in opts:
            self.register_opt(opt, group, clear_cache=False)

    @__clear_cache
    def register_cli_opt(self, opt, group=None):
        """Register a CLI option schema.

        CLI option schemas must be registered before the command line and
        config files are parsed. This is to ensure that all CLI options are
        shown in --help and option validation works as expected.

        :param opt: an instance of an Opt sub-class
        :param group: an optional OptGroup object or group name
        :return: False if the opt was already registered, True otherwise
        :raises: DuplicateOptError, ArgsAlreadyParsedError
        """
        if self._args is not None:
            raise ArgsAlreadyParsedError("cannot register CLI option")

        return self.register_opt(opt, group, cli=True, clear_cache=False)

    @__clear_cache
    def register_cli_opts(self, opts, group=None):
        """Register multiple CLI option schemas at once."""
        for opt in opts:
            self.register_cli_opt(opt, group, clear_cache=False)

    def register_group(self, group):
        """Register an option group.

        An option group must be registered before options can be registered
        with the group.

        :param group: an OptGroup object
        """
        if group.name in self._groups:
            return

        self._groups[group.name] = copy.copy(group)

    @__clear_cache
    def unregister_opt(self, opt, group=None):
        """Unregister an option.

        :param opt: an Opt object
        :param group: an optional OptGroup object or group name
        :raises: ArgsAlreadyParsedError, NoSuchGroupError
        """
        if self._args is not None:
            raise ArgsAlreadyParsedError("reset before unregistering options")

        remitem = None
        for item in self._cli_opts:
            if (item['opt'].dest == opt.dest and
                (group is None or
                    self._get_group(group).name == item['group'].name)):
                remitem = item
                break
        if remitem is not None:
            self._cli_opts.remove(remitem)

        if group is not None:
            self._get_group(group)._unregister_opt(opt)
        elif opt.dest in self._opts:
            del self._opts[opt.dest]

    @__clear_cache
    def unregister_opts(self, opts, group=None):
        """Unregister multiple CLI option schemas at once."""
        for opt in opts:
            self.unregister_opt(opt, group, clear_cache=False)

    def import_opt(self, name, module_str, group=None):
        """Import an option definition from a module.

        Import a module and check that a given option is registered.

        This is intended for use with global configuration objects
        like cfg.CONF where modules commonly register options with
        CONF at module load time. If one module requires an option
        defined by another module it can use this method to explicitly
        declare the dependency.

        :param name: the name/dest of the opt
        :param module_str: the name of a module to import
        :param group: an option OptGroup object or group name
        :raises: NoSuchOptError, NoSuchGroupError
        """
        __import__(module_str)
        self._get_opt_info(name, group)

    def import_group(self, group, module_str):
        """Import an option group from a module.

        Import a module and check that a given option group is registered.

        This is intended for use with global configuration objects
        like cfg.CONF where modules commonly register options with
        CONF at module load time. If one module requires an option group
        defined by another module it can use this method to explicitly
        declare the dependency.

        :param group: an option OptGroup object or group name
        :param module_str: the name of a module to import
        :raises: ImportError, NoSuchGroupError
        """
        __import__(module_str)
        self._get_group(group)

    @removals.removed_kwarg('enforce_type', "The argument enforce_type has "
                            "changed its default value to True and then will"
                            " be removed completely.",
                            version='4.0', removal_version='5.0')
    @__clear_cache
    def set_override(self, name, override, group=None, enforce_type=True):
        """Override an opt value.

        Override the command line, config file and default values of a
        given option.

        :param name: the name/dest of the opt
        :param override: the override value
        :param group: an option OptGroup object or group name
        :param enforce_type: a boolean whether to convert the override
         value to the option's type, None is *not* converted even
         if enforce_type is True.
        :raises: NoSuchOptError, NoSuchGroupError
        """
        opt_info = self._get_opt_info(name, group)
        opt_info['override'] = self._get_enforced_type_value(
            opt_info['opt'], override, enforce_type)

    @removals.removed_kwarg('enforce_type', "The argument enforce_type has "
                            "changed its default value to True and then will"
                            " be removed completely.",
                            version='4.0', removal_version='5.0')
    @__clear_cache
    def set_default(self, name, default, group=None, enforce_type=True):
        """Override an opt's default value.

        Override the default value of given option. A command line or
        config file value will still take precedence over this default.

        :param name: the name/dest of the opt
        :param default: the default value
        :param group: an option OptGroup object or group name
        :param enforce_type: a boolean whether to convert the default
         value to the option's type, None is *not* converted even
         if enforce_type is True.
        :raises: NoSuchOptError, NoSuchGroupError
        """
        opt_info = self._get_opt_info(name, group)
        opt_info['default'] = self._get_enforced_type_value(
            opt_info['opt'], default, enforce_type)

    def _get_enforced_type_value(self, opt, value, enforce_type):
        if value is None:
            return None
        try:
            converted = self._convert_value(value, opt)
        except (ValueError, TypeError):
            if enforce_type:
                raise
        if enforce_type:
            return converted
        else:
            return value

    @__clear_cache
    def clear_override(self, name, group=None):
        """Clear an override an opt value.

        Clear a previously set override of the command line, config file
        and default values of a given option.

        :param name: the name/dest of the opt
        :param group: an option OptGroup object or group name
        :raises: NoSuchOptError, NoSuchGroupError
        """
        opt_info = self._get_opt_info(name, group)
        opt_info.pop('override', None)

    @__clear_cache
    def clear_default(self, name, group=None):
        """Clear an override an opt's default value.

        Clear a previously set override of the default value of given option.

        :param name: the name/dest of the opt
        :param group: an option OptGroup object or group name
        :raises: NoSuchOptError, NoSuchGroupError
        """
        opt_info = self._get_opt_info(name, group)
        opt_info.pop('default', None)

    def _all_opt_infos(self):
        """A generator function for iteration opt infos."""
        for info in self._opts.values():
            yield info, None
        for group in self._groups.values():
            for info in group._opts.values():
                yield info, group

    def _all_cli_opts(self):
        """A generator function for iterating CLI opts."""
        for item in self._cli_opts:
            yield item['opt'], item['group']

    def _unset_defaults_and_overrides(self):
        """Unset any default or override on all options."""
        for info, group in self._all_opt_infos():
            info.pop('default', None)
            info.pop('override', None)

    @property
    def config_dirs(self):
        if self._namespace is None:
            return []
        return self._namespace._config_dirs

    def find_file(self, name):
        """Locate a file located alongside the config files.

        Search for a file with the supplied basename in the directories
        which we have already loaded config files from and other known
        configuration directories.

        The directory, if any, supplied by the config_dir option is
        searched first. Then the config_file option is iterated over
        and each of the base directories of the config_files values
        are searched. Failing both of these, the standard directories
        searched by the module level find_config_files() function is
        used. The first matching file is returned.

        :param name: the filename, for example 'policy.json'
        :returns: the path to a matching file, or None
        """
        if not self._namespace:
            raise NotInitializedError()
        dirs = []
        if self._namespace._config_dirs:
            for directory in self._namespace._config_dirs:
                dirs.append(_fixpath(directory))

        for cf in reversed(self.config_file):
            dirs.append(os.path.dirname(_fixpath(cf)))

        dirs.extend(_get_config_dirs(self.project))

        return _search_dirs(dirs, name)

    def log_opt_values(self, logger, lvl):
        """Log the value of all registered opts.

        It's often useful for an app to log its configuration to a log file at
        startup for debugging. This method dumps to the entire config state to
        the supplied logger at a given log level.

        :param logger: a logging.Logger object
        :param lvl: the log level (for example logging.DEBUG) arg to
                    logger.log()
        """
        logger.log(lvl, "*" * 80)
        logger.log(lvl, "Configuration options gathered from:")
        logger.log(lvl, "command line args: %s", self._args)
        logger.log(lvl, "config files: %s",
                   hasattr(self, 'config_file') and self.config_file or [])
        logger.log(lvl, "=" * 80)

        def _sanitize(opt, value):
            """Obfuscate values of options declared secret."""
            return value if not opt.secret else '*' * 4

        for opt_name in sorted(self._opts):
            opt = self._get_opt_info(opt_name)['opt']
            logger.log(lvl, "%-30s = %s", opt_name,
                       _sanitize(opt, getattr(self, opt_name)))

        for group_name in self._groups:
            group_attr = self.GroupAttr(self, self._get_group(group_name))
            for opt_name in sorted(self._groups[group_name]._opts):
                opt = self._get_opt_info(opt_name, group_name)['opt']
                logger.log(lvl, "%-30s = %s",
                           "%s.%s" % (group_name, opt_name),
                           _sanitize(opt, getattr(group_attr, opt_name)))

        logger.log(lvl, "*" * 80)

    def print_usage(self, file=None):
        """Print the usage message for the current program.

        This method is for use after all CLI options are known
        registered using __call__() method. If this method is called
        before the __call__() is invoked, it throws NotInitializedError

        :param file: the File object (if None, output is on sys.stdout)
        :raises: NotInitializedError
        """
        if not self._oparser:
            raise NotInitializedError()
        self._oparser.print_usage(file)

    def print_help(self, file=None):
        """Print the help message for the current program.

        This method is for use after all CLI options are known
        registered using __call__() method. If this method is called
        before the __call__() is invoked, it throws NotInitializedError

        :param file: the File object (if None, output is on sys.stdout)
        :raises: NotInitializedError
        """
        if not self._oparser:
            raise NotInitializedError()
        self._oparser.print_help(file)

    def _get(self, name, group=None, namespace=None):
        if isinstance(group, OptGroup):
            key = (group.name, name)
        else:
            key = (group, name)
        if namespace is None:
            try:
                return self.__cache[key]
            except KeyError:  # nosec: Valid control flow instruction
                pass
        value = self._do_get(name, group, namespace)
        self.__cache[key] = value
        return value

    def _do_get(self, name, group=None, namespace=None):
        """Look up an option value.

        :param name: the opt name (or 'dest', more precisely)
        :param group: an OptGroup
        :param namespace: the namespace object to get the option value from
        :returns: the option value, or a GroupAttr object
        :raises: NoSuchOptError, NoSuchGroupError, ConfigFileValueError,
                 TemplateSubstitutionError
        """
        if group is None and name in self._groups:
            return self.GroupAttr(self, self._get_group(name))

        info = self._get_opt_info(name, group)
        opt = info['opt']

        if isinstance(opt, SubCommandOpt):
            return self.SubCommandAttr(self, group, opt.dest)

        if 'override' in info:
            return self._substitute(info['override'])

        def convert(value):
            return self._convert_value(
                self._substitute(value, group, namespace), opt)

        if opt.mutable and namespace is None:
            namespace = self._mutable_ns
        if namespace is None:
            namespace = self._namespace
        if namespace is not None:
            group_name = group.name if group else None
            try:
                return convert(opt._get_from_namespace(namespace, group_name))
            except KeyError:  # nosec: Valid control flow instruction
                pass
            except ValueError as ve:
                raise ConfigFileValueError(
                    "Value for option %s is not valid: %s"
                    % (opt.name, str(ve)))

        if 'default' in info:
            return self._substitute(info['default'])

        if self._validate_default_values:
            if opt.default is not None:
                try:
                    convert(opt.default)
                except ValueError as e:
                    raise ConfigFileValueError(
                        "Default value for option %s is not valid: %s"
                        % (opt.name, str(e)))

        if opt.default is not None:
            return convert(opt.default)

        return None

    def _substitute(self, value, group=None, namespace=None):
        """Perform string template substitution.

        Substitute any template variables (for example $foo, ${bar}) in
        the supplied string value(s) with opt values.

        :param value: the string value, or list of string values
        :param group: the group that retrieves the option value from
        :param namespace: the namespace object that retrieves the option
                          value from
        :returns: the substituted string(s)
        """
        if isinstance(value, list):
            return [self._substitute(i, group=group, namespace=namespace)
                    for i in value]
        elif isinstance(value, str):
            # Treat a backslash followed by the dollar sign "\$"
            # the same as the string template escape "$$" as it is
            # a bit more natural for users
            if r'\$' in value:
                value = value.replace(r'\$', '$$')
            tmpl = self.Template(value)
            ret = tmpl.safe_substitute(
                self.StrSubWrapper(self, group=group, namespace=namespace))
            return ret
        elif isinstance(value, dict):
            # Substitute template variables in both key and value
            return {self._substitute(key, group=group, namespace=namespace):
                    self._substitute(val, group=group, namespace=namespace)
                    for key, val in value.items()}
        else:
            return value

    class Template(string.Template):
        idpattern = r'[_a-z][\._a-z0-9]*'

    def _convert_value(self, value, opt):
        """Perform value type conversion.

        Converts values using option's type. Handles cases when value is
        actually a list of values (for example for multi opts).

        :param value: the string value, or list of string values
        :param opt: option definition (instance of Opt class or its subclasses)
        :returns: converted value
        """
        if opt.multi:
            return [opt.type(v) for v in value]
        else:
            return opt.type(value)

    def _get_group(self, group_or_name, autocreate=False):
        """Looks up a OptGroup object.

        Helper function to return an OptGroup given a parameter which can
        either be the group's name or an OptGroup object.

        The OptGroup object returned is from the internal dict of OptGroup
        objects, which will be a copy of any OptGroup object that users of
        the API have access to.

        If autocreate is True, the group will be created if it's not found. If
        group is an instance of OptGroup, that same instance will be
        registered, otherwise a new instance of OptGroup will be created.

        :param group_or_name: the group's name or the OptGroup object itself
        :param autocreate: whether to auto-create the group if it's not found
        :raises: NoSuchGroupError
        """
        group = group_or_name if isinstance(group_or_name, OptGroup) else None
        group_name = group.name if group else group_or_name

        if group_name not in self._groups:
            if not autocreate:
                raise NoSuchGroupError(group_name)

            self.register_group(group or OptGroup(name=group_name))

        return self._groups[group_name]

    def _find_deprecated_opts(self, opt_name, group=None):
        real_opt_name = None
        real_group_name = None
        group_name = group or 'DEFAULT'
        if hasattr(group_name, 'name'):
            group_name = group_name.name
        dep_group = self._deprecated_opts.get(group_name)
        if dep_group:
            real_opt_dict = dep_group.get(opt_name)
            if real_opt_dict:
                real_opt_name = real_opt_dict['opt'].name
                if real_opt_dict['group']:
                    real_group_name = real_opt_dict['group'].name
        return real_opt_name, real_group_name

    def _get_opt_info(self, opt_name, group=None):
        """Return the (opt, override, default) dict for an opt.

        :param opt_name: an opt name/dest
        :param group: an optional group name or OptGroup object
        :raises: NoSuchOptError, NoSuchGroupError
        """
        if group is None:
            opts = self._opts
        else:
            group = self._get_group(group)
            opts = group._opts

        if opt_name not in opts:
            real_opt_name, real_group_name = self._find_deprecated_opts(
                opt_name, group=group)
            if not real_opt_name:
                raise NoSuchOptError(opt_name, group)
            log_real_group_name = real_group_name or 'DEFAULT'
            dep_message = ('Config option %(dep_group)s.%(dep_option)s '
                           ' is deprecated. Use option %(group)s.'
                           '%(option)s instead.')
            LOG.warning(dep_message, {'dep_option': opt_name,
                                      'dep_group': group,
                                      'option': real_opt_name,
                                      'group': log_real_group_name})
            opt_name = real_opt_name
            if real_group_name:
                group = self._get_group(real_group_name)
                opts = group._opts

        return opts[opt_name]

    def _check_required_opts(self, namespace=None):
        """Check that all opts marked as required have values specified.

        :param namespace: the namespace object be checked the required options
        :raises: RequiredOptError
        """
        for info, group in self._all_opt_infos():
            opt = info['opt']

            if opt.required:
                if 'default' in info or 'override' in info:
                    continue

                if self._get(opt.dest, group, namespace) is None:
                    raise RequiredOptError(opt.name, group)

    def _parse_cli_opts(self, args):
        """Parse command line options.

        Initializes the command line option parser and parses the supplied
        command line arguments.

        :param args: the command line arguments
        :returns: a _Namespace object containing the parsed option values
        :raises: SystemExit, DuplicateOptError
                 ConfigFileParseError, ConfigFileValueError

        """
        self._args = args
        for opt, group in self._all_cli_opts():
            opt._add_to_cli(self._oparser, group)

        return self._parse_config_files()

    def _parse_config_files(self):
        """Parse configure files options.

        :raises: SystemExit, ConfigFilesNotFoundError, ConfigFileParseError,
                 ConfigFilesPermissionDeniedError,
                 RequiredOptError, DuplicateOptError
        """
        namespace = _Namespace(self)

        # handle --config-file args or the default_config_files
        for arg in self._args:
            if arg == '--config-file' or arg.startswith('--config-file='):
                break
        else:
            for config_file in self.default_config_files:
                ConfigParser._parse_file(config_file, namespace)

        # handle --config-dir args or the default_config_dirs
        for arg in self._args:
            if arg == '--config-dir' or arg.startswith('--config-dir='):
                break
        else:
            for config_dir in self.default_config_dirs:
                # for the default config-dir directories we just continue
                # if the directories do not exist. This is different to the
                # case where --config-dir is given on the command line.
                if not os.path.exists(config_dir):
                    continue

                config_dir_glob = os.path.join(config_dir, '*.conf')

                for config_file in sorted(glob.glob(config_dir_glob)):
                    ConfigParser._parse_file(config_file, namespace)

        self._oparser.parse_args(self._args, namespace)

        self._validate_cli_options(namespace)

        return namespace

    def _validate_cli_options(self, namespace):
        for opt, group in sorted(self._all_cli_opts(),
                                 key=lambda x: x[0].name):
            group_name = group.name if group else None
            try:
                value = opt._get_from_namespace(namespace, group_name)
            except KeyError:
                continue

            value = self._substitute(value, group=group, namespace=namespace)

            try:
                self._convert_value(value, opt)
            except ValueError:
                sys.stderr.write("argument --%s: Invalid %s value: %s\n" % (
                    opt.dest, repr(opt.type), value))
                raise SystemExit

    def _reload_config_files(self):
        namespace = self._parse_config_files()
        if namespace._files_not_found:
            raise ConfigFilesNotFoundError(namespace._files_not_found)
        if namespace._files_permission_denied:
            raise ConfigFilesPermissionDeniedError(
                namespace._files_permission_denied)
        self._check_required_opts(namespace)
        return namespace

    @__clear_cache
    def reload_config_files(self):
        """Reload configure files and parse all options

        :return: False if reload configure files failed or else return True
        """

        try:
            namespace = self._reload_config_files()
        except SystemExit as exc:
            LOG.warning("Caught SystemExit while reloading configure "
                        "files with exit code: %d", exc.code)
            return False
        except Error as err:
            LOG.warning("Caught Error while reloading configure files: "
                        "%s", err)
            return False
        else:
            self._namespace = namespace
            return True

    def register_mutate_hook(self, hook):
        """Registers a hook to be called by mutate_config_files.

        :param hook: a function accepting this ConfigOpts object and a dict of
                     config mutations, as returned by mutate_config_files.
        :return: None
        """
        self._mutate_hooks.add(hook)

    def mutate_config_files(self):
        """Reload configure files and parse all options.

        Only options marked as 'mutable' will appear to change.

        Hooks are called in a NON-DETERMINISTIC ORDER. Do not expect hooks to
        be called in the same order as they were added.

        :return: {(None or 'group', 'optname'): (old_value, new_value), ... }
        :raises: Error if reloading fails
        """
        self.__cache.clear()

        old_mutate_ns = self._mutable_ns or self._namespace
        self._mutable_ns = self._reload_config_files()
        self._warn_immutability()
        fresh = self._diff_ns(old_mutate_ns, self._mutable_ns)

        def key_fn(item):
            # Py3 won't sort heterogeneous types. Sort None as TAB which has a
            # very low ASCII value.
            (groupname, optname) = item[0]
            return item[0] if groupname else ('\t', optname)
        sorted_fresh = sorted(fresh.items(), key=key_fn)
        for (groupname, optname), (old, new) in sorted_fresh:
            groupname = groupname if groupname else 'DEFAULT'
            LOG.info("Option %(group)s.%(option)s changed from "
                     "[%(old_val)s] to [%(new_val)s]",
                     {'group': groupname,
                      'option': optname,
                      'old_val': old,
                      'new_val': new})
        for hook in self._mutate_hooks:
            hook(self, fresh)
        return fresh

    def _warn_immutability(self):
        """Check immutable opts have not changed.

        _do_get won't return the new values but presumably someone changed the
        config file expecting them to change so we should warn them they won't.
        """
        for info, group in self._all_opt_infos():
            opt = info['opt']
            if opt.mutable:
                continue
            groupname = group.name if group else 'DEFAULT'
            try:
                old = opt._get_from_namespace(self._namespace, groupname)
            except KeyError:
                old = None
            try:
                new = opt._get_from_namespace(self._mutable_ns, groupname)
            except KeyError:
                new = None
            if old != new:
                LOG.warning("Ignoring change to immutable option "
                            "%(group)s.%(option)s",
                            {"group": groupname, "option": opt.name})

    def _diff_ns(self, old_ns, new_ns):
        """Compare mutable option values between two namespaces.

        This can be used to only reconfigure stateful sessions when necessary.

        :return {(None or 'group', 'optname'): (old_value, new_value), ... }
        """
        diff = {}
        for info, group in self._all_opt_infos():
            opt = info['opt']
            if not opt.mutable:
                continue
            groupname = group.name if group else None
            try:
                old = opt._get_from_namespace(old_ns, groupname)
            except KeyError:
                old = None
            try:
                new = opt._get_from_namespace(new_ns, groupname)
            except KeyError:
                new = None
            if old != new:
                diff[(groupname, opt.name)] = (old, new)
        return diff

    def list_all_sections(self):
        """List all sections from the configuration.

        Returns a sorted list of all section names found in the
        configuration files, whether declared beforehand or not.
        """
        s = set([])
        if self._mutable_ns:
            s |= set(self._mutable_ns._sections())
        if self._namespace:
            s |= set(self._namespace._sections())
        return sorted(s)

    class GroupAttr(collections.Mapping):

        """Helper class.

        Represents the option values of a group as a mapping and attributes.
        """

        def __init__(self, conf, group):
            """Construct a GroupAttr object.

            :param conf: a ConfigOpts object
            :param group: an OptGroup object
            """
            self._conf = conf
            self._group = group

        def __getattr__(self, name):
            """Look up an option value and perform template substitution."""
            return self._conf._get(name, self._group)

        def __getitem__(self, key):
            """Look up an option value and perform string substitution."""
            return self.__getattr__(key)

        def __contains__(self, key):
            """Return True if key is the name of a registered opt or group."""
            return key in self._group._opts

        def __iter__(self):
            """Iterate over all registered opt and group names."""
            for key in self._group._opts.keys():
                yield key

        def __len__(self):
            """Return the number of options and option groups."""
            return len(self._group._opts)

    class SubCommandAttr(object):

        """Helper class.

        Represents the name and arguments of an argparse sub-parser.
        """

        def __init__(self, conf, group, dest):
            """Construct a SubCommandAttr object.

            :param conf: a ConfigOpts object
            :param group: an OptGroup object
            :param dest: the name of the sub-parser
            """
            self._conf = conf
            self._group = group
            self._dest = dest

        def __getattr__(self, name):
            """Look up a sub-parser name or argument value."""
            if name == 'name':
                name = self._dest
                if self._group is not None:
                    name = self._group.name + '_' + name
                return getattr(self._conf._namespace, name)

            if name in self._conf:
                raise DuplicateOptError(name)

            try:
                return getattr(self._conf._namespace, name)
            except AttributeError:
                raise NoSuchOptError(name)

    class StrSubWrapper(object):

        """Helper class.

        Exposes opt values as a dict for string substitution.
        """

        def __init__(self, conf, group=None, namespace=None):
            """Construct a StrSubWrapper object.

            :param conf: a ConfigOpts object
            :param group: an OptGroup object
            :param namespace: the namespace object that retrieves the option
                              value from
            """
            self.conf = conf
            self.group = group
            self.namespace = namespace

        def __getitem__(self, key):
            """Look up an opt value from the ConfigOpts object.

            :param key: an opt name
            :returns: an opt value
            """
            try:
                group_name, option = key.split(".", 1)
            except ValueError:
                group = self.group
                option = key
            else:
                group = OptGroup(name=group_name)
            try:
                value = self.conf._get(option, group=group,
                                       namespace=self.namespace)
            except NoSuchOptError:
                value = self.conf._get(key, namespace=self.namespace)
            if isinstance(value, self.conf.GroupAttr):
                raise TemplateSubstitutionError(
                    'substituting group %s not supported' % key)
            if value is None:
                return ''
            return value


CONF = ConfigOpts()
