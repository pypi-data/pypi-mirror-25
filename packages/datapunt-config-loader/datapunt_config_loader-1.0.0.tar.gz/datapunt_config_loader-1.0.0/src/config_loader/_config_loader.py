# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import pathlib
import string
import typing as T
from collections import ChainMap as _ChainMap

import jsonschema
import os
import yaml


class ConfigError(Exception):
    # language=rst
    """Configuration Error"""


def load(config_file_path: T.Union[pathlib.PurePath, str],
         config_schema_file_path: T.Union[pathlib.PurePath, str]) -> T.Dict[str, T.Any]:
    # language=rst
    """Load, parse and validate the configuration file.

    Raises:
        ConfigError: if something goes wrong
        FileNotFoundError: if something else goes wrong
    """
    if not isinstance(config_file_path, pathlib.PurePath):
        config_file_path = pathlib.Path(config_file_path)
    if not isinstance(config_schema_file_path, pathlib.PurePath):
        config_schema_file_path = pathlib.Path(config_schema_file_path)
    config = _load_yaml(config_file_path)
    config = _interpolate_environment(config)
    _validate(config, config_schema_file_path)
    return config


def _load_yaml(path: pathlib.Path) -> T.Union[T.Dict, T.List]:
    # language=rst
    """Read the config file from ``path``."""
    with path.open() as f:
        try:
            return yaml.load(f)
        except yaml.YAMLError as e:
            error_msg = "Couldn't load yaml file '{}'."
            raise ConfigError(error_msg.format(path)) from e


def _interpolate_environment(config: T.Dict):
    # language=rst
    """Substitute environment variables.

    Recursively find string-type values in the given ``config``,
    and try to substitute them with values from :data:`os.environ`.

    Note:
        If a substituted value is a string containing only digits (i.e.
        :py:meth:`str.isdigit()` is True), then this function will cast
        it to an integer.  It does not try to do any other type conversion.

    :param config: configuration mapping

    """

    def interpolate(value):
        try:
            result = _TemplateWithDefaults(value).substitute(os.environ)
        except KeyError as e:
            error_msg = "Could not substitute: {}"
            raise ConfigError(error_msg.format(value)) from e
        except ValueError as e:
            error_msg = "Invalid substitution: {}"
            raise ConfigError(error_msg.format(value)) from e
        return (result.isdigit() and int(result)) or result

    def interpolate_recursive(obj: T.Union[T.Dict, T.List, str]):
        if isinstance(obj, str):
            return interpolate(obj)
        if isinstance(obj, dict):
            return {key: interpolate_recursive(obj[key]) for key in obj}
        if isinstance(obj, list):
            return [interpolate_recursive(val) for val in obj]
        return obj

    return {key: interpolate_recursive(config[key]) for key in config}


def _validate(config: T.Union[T.Dict, T.List], schemafile: pathlib.Path):
    # language=rst
    """
    Validate the given ``config`` using the JSON schema given in ``schemafile``.

    Raises:
        ConfigError

    """
    schema = _load_yaml(schemafile)
    try:
        jsonschema.validate(config, schema)
    except jsonschema.exceptions.SchemaError as e:
        error_msg = "Invalid JSON schema definition at {}"
        raise ConfigError(error_msg.format(schemafile)) from e
    except jsonschema.exceptions.ValidationError as e:
        raise ConfigError("Schema validation failed.") from e


class _TemplateWithDefaults(string.Template):
    # language=rst
    """
    String template that supports Bash-style default values for interpolation.

    Copied from `Docker Compose
    <https://github.com/docker/compose/blob/master/compose/config/interpolation.py>`_

    """
    # string.Template uses cls.idpattern to define identifiers:
    idpattern = r'[_a-z][_a-z0-9]*(?::?-[^}]+)?'

    # Modified from python2.7/string.py
    def substitute(*args, **kws):
        if not args:
            raise TypeError("descriptor 'substitute' of 'Template' object "
                            "needs an argument")
        self, *args = args  # allow the "self" keyword be passed
        if len(args) > 1:
            raise TypeError('Too many positional arguments')
        if not args:
            mapping = kws
        elif kws:
            mapping = _ChainMap(kws, args[0])
        else:
            mapping = args[0]

        # Helper function for .sub()
        def convert(mo):
            # Check the most common path first.
            named = mo.group('named') or mo.group('braced')
            if named is not None:
                if ':-' in named:
                    var, _, default = named.partition(':-')
                    return mapping.get(var) or default
                if '-' in named:
                    var, _, default = named.partition('-')
                    return mapping.get(var, default)
                val = mapping[named]
                return '%s' % (val,)
            if mo.group('escaped') is not None:
                return self.delimiter
            if mo.group('invalid') is not None:
                self._invalid(mo)
            raise ValueError('Unrecognized named group in pattern',
                             self.pattern)
        return self.pattern.sub(convert, self.template)
