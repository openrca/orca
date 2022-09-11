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

import logging
import multiprocessing

import cotyledon
import flask
from flask_cors import CORS

from orca.api import apiv1
from orca.graph import graph


class Manager(cotyledon.ServiceManager):
    def initialize(self):
        graph_lock = multiprocessing.Lock()
        self.add(APIService, workers=1, args=(graph_lock,))


class APIService(cotyledon.Service):
    def __init__(self, worker_id, graph_lock):
        super().__init__(worker_id)
        self._graph_lock = graph_lock
        self.__graph = None

    @property
    def _graph(self):
        if not self.__graph:
            self.__graph = graph.Graph.get(self._graph_lock)
        return self.__graph

    def run(self):
        self._set_logging()
        app = self._init_app()
        CORS(app)
        app.run(host="0.0.0.0")

    def _set_logging(self):
        log = logging.getLogger("werkzeug")
        log.setLevel(logging.ERROR)

    def _init_app(self):
        app = flask.Flask(__name__)
        api_blueprint = apiv1.initialize(self._graph)
        app.register_blueprint(api_blueprint)
        return app
