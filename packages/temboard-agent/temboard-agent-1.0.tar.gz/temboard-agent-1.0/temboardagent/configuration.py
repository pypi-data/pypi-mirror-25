import logging

try:
    import configparser
except ImportError:
    import ConfigParser as configparser

import os.path
import json
import re
from temboardagent.errors import ConfigurationError
from temboardagent.logger import LOG_FACILITIES, LOG_LEVELS, LOG_METHODS


logger = logging.getLogger(__name__)


class BaseConfiguration(configparser.RawConfigParser):
    """
    Common configuration parser.
    """
    def __init__(self, configfile, *args, **kwargs):
        configparser.RawConfigParser.__init__(self, *args, **kwargs)
        self.configfile = os.path.realpath(configfile)
        self.confdir = os.path.dirname(self.configfile)

        # Default configuration values
        self.temboard = {
            'port': 2345,
            'address': '0.0.0.0',
            'users': '/etc/temboard-agent/users',
            'ssl_cert_file': None,
            'ssl_key_file': None,
            'plugins': [
                "monitoring",
                "dashboard",
                "pgconf",
                "administration",
                "activity"
            ],
            'home': os.environ.get('HOME', '/var/lib/temboard-agent'),
            'hostname': None,
            'key': None
        }
        self.logging = {
            'method': 'syslog',
            'facility': 'local0',
            'destination': '/dev/log',
            'level': 'INFO'
        }
        self.postgresql = {
            'host': '/var/run/postgresql',
            'user': 'postgres',
            'port': 5432,
            'password': None,
            'dbname': 'postgres',
            'pg_config': '/usr/bin/pg_config',
            'instance': 'main'
        }
        try:
            with open(self.configfile) as fd:
                self.readfp(fd)
        except IOError:
            raise ConfigurationError("Configuration file %s can't be opened."
                                     % (self.configfile))
        except configparser.MissingSectionHeaderError:
            raise ConfigurationError(
                    "Configuration file does not contain section headers.")

    def check_section(self, section):
        if not self.has_section(section):
            raise ConfigurationError(
                    "Section '%s' not found in configuration file %s"
                    % (section, self.configfile))

    def abspath(self, path):
        if path.startswith('/'):
            return path
        else:
            return os.path.realpath('/'.join([self.confdir, path]))

    def getfile(self, section, name):
        path = self.abspath(self.get(section, name))
        try:
            with open(path) as fd:
                fd.read()
        except Exception as e:
            logger.warn("Failed to open %s: %s", path, e)
            raise ConfigurationError("%s file can't be opened." % (path,))
        return path


class Configuration(BaseConfiguration):
    """
    Customized configuration parser.
    """
    def __init__(self, configfile, *args, **kwargs):
        BaseConfiguration.__init__(self, configfile, *args, **kwargs)
        self.plugins = {}
        # Test if 'temboard' section exists.
        self.check_section('temboard')

        try:
            if not (self.getint('temboard', 'port') >= 0
                    and self.getint('temboard', 'port') <= 65535):
                raise ValueError()
            self.temboard['port'] = self.getint('temboard', 'port')
        except ValueError:
            raise ConfigurationError("'port' option must be an integer "
                                     "[0-65535] in %s." % (self.configfile))
        except configparser.NoOptionError:
            pass
        try:
            if not re.match(r'(?:[3-9]\d?|2(?:5[0-5]|[0-4]?\d)?|1\d{0,2}|\d)'
                            '(\.(?:[3-9]\d?|2(?:5[0-5]|[0-4]?\d)?|1\d{0,2}|\d'
                            ')){3}$', self.get('temboard', 'address')):
                raise ValueError()
            self.temboard['address'] = self.get('temboard', 'address')
        except ValueError:
            raise ConfigurationError("'address' option must be a valid IPv4 "
                                     "address in %s." % (self.configfile))
        except configparser.NoOptionError:
            pass

        try:
            self.temboard['users'] = self.getfile('temboard', 'users')
        except configparser.NoOptionError:
            pass

        try:
            plugins = json.loads(self.get('temboard', 'plugins'))
            if not type(plugins) == list:
                raise ValueError()
            for plugin in plugins:
                if not re.match('^[a-zA-Z0-9]+$', str(plugin)):
                    raise ValueError
            self.temboard['plugins'] = plugins
        except configparser.NoOptionError:
            pass
        except ValueError:
            raise ConfigurationError("'plugins' option must be a list of "
                                     "string (alphanum only) in %s." % (
                                         self.configfile))
        try:
            self.temboard['key'] = self.get('temboard', 'key')
        except configparser.NoOptionError:
            pass

        try:
            self.temboard['ssl_cert_file'] = (
                self.getfile('temboard', 'ssl_cert_file'))
        except configparser.NoOptionError:
            pass

        try:
            self.temboard['ssl_key_file'] = (
                self.getfile('temboard', 'ssl_key_file'))
        except configparser.NoOptionError:
            pass

        try:
            home = self.get('temboard', 'home')
            if not os.access(home, os.W_OK):
                raise Exception()
            self.temboard['home'] = self.get('temboard', 'home')
        except configparser.NoOptionError:
            pass
        except Exception:
            raise ConfigurationError("Home directory %s not writable."
                                     % (self.get('temboard', 'home')))

        try:
            hostname = self.get('temboard', 'hostname')
            self.temboard['hostname'] = hostname
        except configparser.NoOptionError:
            pass

        # Test if 'logging' section exists.
        self.check_section('logging')
        try:
            if not self.get('logging', 'method') in LOG_METHODS:
                raise ValueError()
            self.logging['method'] = self.get('logging', 'method')
        except ValueError:
            raise ConfigurationError("Invalid 'method' option in 'logging' "
                                     "section in %s." % (self.configfile))
        except configparser.NoOptionError:
            pass
        try:
            if not self.get('logging', 'facility') in LOG_FACILITIES:
                raise ValueError()
            self.logging['facility'] = self.get('logging', 'facility')
        except ValueError:
            raise ConfigurationError("Invalid 'facility' option in 'logging' "
                                     "section in %s." % (self.configfile))
        except configparser.NoOptionError:
            pass
        try:
            self.logging['destination'] = self.get('logging', 'destination')
        except configparser.NoOptionError:
            pass
        try:
            if not self.get('logging', 'level') in LOG_LEVELS:
                raise ValueError()
            self.logging['level'] = self.get('logging', 'level')
        except ValueError:
            raise ConfigurationError("Invalid 'level' option in 'logging' "
                                     "section in %s." % (self.configfile))
        except configparser.NoOptionError:
            pass

        # Test if 'postgresql' section exists.
        self.check_section('postgresql')
        try:
            from os import path
            if not path.exists(self.get('postgresql', 'host')):
                raise ValueError()
            self.postgresql['host'] = self.get('postgresql', 'host')
        except ValueError:
            raise ConfigurationError("'host' option must be a valid directory"
                                     " path containing PostgreSQL's local unix"
                                     " socket in %s." % (self.configfile))
        except configparser.NoOptionError:
            pass

        try:
            self.postgresql['user'] = self.get('postgresql', 'user')
        except configparser.NoOptionError:
            pass

        try:
            if not (self.getint('postgresql', 'port') >= 0
                    and self.getint('postgresql', 'port') <= 65535):
                raise ValueError()
            self.postgresql['port'] = self.getint('postgresql', 'port')
        except ValueError:
            raise ConfigurationError("'port' option must be an integer "
                                     "[0-65535] in 'postgresql' section in %s."
                                     % (self.configfile))
        except configparser.NoOptionError:
            pass

        try:
            self.postgresql['password'] = self.get('postgresql', 'password')
        except configparser.NoOptionError:
            pass

        try:
            self.postgresql['dbname'] = self.get('postgresql', 'dbname')
        except configparser.NoOptionError:
            pass
        try:
            self.postgresql['instance'] = self.get('postgresql', 'instance')
        except configparser.NoOptionError:
            pass


class PluginConfiguration(configparser.RawConfigParser):
    """
    Customized configuration parser for plugins.
    """
    def __init__(self, configfile, *args, **kwargs):
        configparser.RawConfigParser.__init__(self, *args, **kwargs)
        self.configfile = configfile
        self.confdir = os.path.dirname(self.configfile)

        try:
            with open(self.configfile) as fd:
                self.readfp(fd)
        except IOError:
            raise ConfigurationError("Configuration file %s can't be opened."
                                     % (self.configfile))
        except configparser.MissingSectionHeaderError:
            raise ConfigurationError("Configuration file does not contain "
                                     "section headers.")

    def check_section(self, section):
        if not self.has_section(section):
            raise ConfigurationError("Section '%s' not found in configuration "
                                     "file %s" % (section, self.configfile))

    def abspath(self, path):
        if path.startswith('/'):
            return path
        else:
            return os.path.realpath('/'.join([self.confdir, path]))

    def getfile(self, section, name):
        path = self.abspath(self.get(section, name))
        try:
            with open(path) as fd:
                fd.read()
        except Exception as e:
            logger.warn("Failed to open %s: %s", path, e)
            raise ConfigurationError("%s file can't be opened." % (path,))
        return path


class LazyConfiguration(BaseConfiguration):
    """
    Customized configuration parser.
    """
    def __init__(self, configfile, *args, **kwargs):
        BaseConfiguration.__init__(self, configfile, *args, **kwargs)
        # Test if 'temboard' section exists.
        self.check_section('temboard')
        for k, v in self.temboard.iteritems():
            try:
                self.temboard[k] = self.get('temboard', k)
            except configparser.NoOptionError:
                pass
        # Test if 'logging' section exists.
        self.check_section('logging')
        for k, v in self.logging.iteritems():
            try:
                self.logging[k] = self.get('logging', k)
            except configparser.NoOptionError:
                pass
        # Test if 'postgresql' section exists.
        self.check_section('postgresql')
        for k, v in self.logging.iteritems():
            try:
                self.postgresql[k] = self.get('postgresql', k)
            except configparser.NoOptionError:
                pass
