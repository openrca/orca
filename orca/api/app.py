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

import multiprocessing

from flask import Flask

from orca import api
from orca.common import config
from orca.graph import drivers as graph_drivers
from orca.graph import graph

CONFIG = config.CONFIG


def create_app():
    graph_lock = multiprocessing.Lock()
    graph_inst = graph.Graph.get(graph_lock)
    app = Flask(__name__)
    app.register_blueprint(api.initialize(graph_inst))
    return app
