# Copyright 2020 OpenRCA Authors
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os

import addict as dict_lib
import cerberus

from orca import exceptions
from orca.common import file_utils, str_utils


class Config(object):

    """Configuration proxy."""

    def __init__(self, path, parser):
        self._path = path
        self._parser = parser
        self.__cache = None

    def __getattr__(self, name):
        return self._get(name)

    def __getitem__(self, key):
        return self.__getattr__(key)

    @property
    def _cache(self):
        if not self.__cache:
            self.__cache = self._parser.parse(self._path)
        return self.__cache

    def _get(self, name):
        return getattr(self._cache, name)

    @classmethod
    def get(cls, schema):
        parser = ConfigParser(schema)
        path = os.environ.get("OPENRCA_CONFIG")
        if not path:
            path = "/etc/orca/orca.yaml"
        return cls(path, parser)


class ConfigParser(object):

    """Configuration parser."""

    def __init__(self, schema):
        self._schema = schema

    def parse(self, config_path):
        config_dict = file_utils.load_yaml(config_path)
        validator = cerberus.Validator(self._schema)
        is_valid = validator.validate(config_dict)
        if not is_valid:
            raise exceptions.ConfigParseError(errors=validator.errors)
        return dict_lib.Dict(validator.document)


SCHEMA = {
    "graph": {
        "type": "dict",
        "schema": {
            "driver": {"type": "string", "default": "arangodb"},
            "arangodb": {
                "type": "dict",
                "schema": {
                    "enabled": {
                        "type": "boolean",
                        "coerce": (str, str_utils.to_bool),
                        "default": True,
                    },
                    "host": {"type": "string"},
                    "port": {"type": "integer", "coerce": int, "default": 8529},
                    "database": {"type": "string", "default": "orca"},
                    "username": {"type": "string"},
                    "password": {"type": "string"},
                },
            },
        },
    },
    "topology": {
        "type": "dict",
        "schema": {
            "alerts": {
                "type": "dict",
                "schema": {
                    "mapping_path": {
                        "type": "string",
                        "default": "/etc/orca/alerts-mapping.yaml",
                    }
                },
            },
            "gc": {
                "type": "dict",
                "schema": {
                    "interval": {"type": "integer", "coerce": int, "default": 60}
                },
            },
        },
    },
    "probes": {
        "type": "dict",
        "schema": {
            "kubernetes": {
                "type": "dict",
                "schema": {
                    "enabled": {
                        "type": "boolean",
                        "coerce": (str, str_utils.to_bool),
                        "default": True,
                    },
                    "resync_period": {"type": "integer", "coerce": int, "default": 300},
                },
            },
            "istio": {
                "type": "dict",
                "schema": {
                    "enabled": {
                        "type": "boolean",
                        "coerce": (str, str_utils.to_bool),
                        "default": False,
                    },
                    "resync_period": {"type": "integer", "coerce": int, "default": 300},
                },
            },
            "kiali": {
                "type": "dict",
                "schema": {
                    "enabled": {
                        "type": "boolean",
                        "coerce": (str, str_utils.to_bool),
                        "default": False,
                    },
                    "url": {"type": "string"},
                    "username": {"type": "string"},
                    "password": {"type": "string"},
                    "resync_period": {"type": "integer", "coerce": int, "default": 300},
                },
            },
            "prometheus": {
                "type": "dict",
                "schema": {
                    "enabled": {
                        "type": "boolean",
                        "coerce": (str, str_utils.to_bool),
                        "default": False,
                    },
                    "url": {"type": "string"},
                    "resync_period": {"type": "integer", "coerce": int, "default": 300},
                },
            },
            "zabbix": {
                "type": "dict",
                "schema": {
                    "enabled": {
                        "type": "boolean",
                        "coerce": (str, str_utils.to_bool),
                        "default": False,
                    },
                    "url": {"type": "string"},
                    "username": {"type": "string"},
                    "password": {"type": "string"},
                    "resync_period": {"type": "integer", "coerce": int, "default": 300},
                },
            },
        },
    },
    "ingestors": {
        "type": "dict",
        "schema": {
            "prometheus": {
                "type": "dict",
                "schema": {
                    "enabled": {
                        "type": "boolean",
                        "coerce": (str, str_utils.to_bool),
                        "default": False,
                    },
                },
            },
            "falco": {
                "type": "dict",
                "schema": {
                    "enabled": {
                        "type": "boolean",
                        "coerce": (str, str_utils.to_bool),
                        "default": False,
                    },
                },
            },
            "elastalert": {
                "type": "dict",
                "schema": {
                    "enabled": {
                        "type": "boolean",
                        "coerce": (str, str_utils.to_bool),
                        "default": False,
                    },
                },
            },
        },
    },
    "logging": {
        "type": "dict",
        "schema": {
            "log_level": {
                "type": "string",
                "default": "info",
                "allowed": ["critical", "error", "warning", "info", "debug"],
            }
        },
    },
}

CONFIG = Config.get(SCHEMA)
