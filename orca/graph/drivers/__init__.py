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

from orca.common import config
from orca.graph.drivers import arangodb

CONFIG = config.CONFIG


class DriverFactory(object):
    @staticmethod
    def get(backend):
        if backend == "arangodb":
            return arangodb.ArangoDBDriver(
                host=CONFIG.graph.arangodb.host,
                port=CONFIG.graph.arangodb.port,
                database=CONFIG.graph.arangodb.database,
                username=CONFIG.graph.arangodb.username,
                password=CONFIG.graph.arangodb.password,
            )
