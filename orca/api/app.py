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

from flask import Flask

from orca import api
from orca.graph import graph
from orca.graph import drivers as graph_drivers


def create_app():
    # TODO: read graph backend from config
    graph_client = graph_drivers.DriverFactory.get('neo4j')
    graph_inst = graph.Graph(graph_client)

    app = Flask(__name__)
    app.register_blueprint(api.initialize(graph_inst))
    return app
