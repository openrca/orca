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

import abc


class UpstreamProxy(abc.ABC):

    """Base class for upstream proxies."""

    def __init__(self, client):
        self._client = client

    @abc.abstractmethod
    def get_all(self):
        """Retrieves all entities from the upstream."""

    @abc.abstractmethod
    def get_events(self, handler=None):
        """Retrieves entity events from the upstream."""


class EventHandler(abc.ABC):

    @abc.abstractmethod
    def on_added(self, entity):
        """Callback triggered when entity has been added in the upstream."""

    @abc.abstractmethod
    def on_updated(self, entity):
        """Callback triggered when entity has been updated in the upstream."""

    @abc.abstractmethod
    def on_deleted(self, entity):
        """Callback triggered when entity has been deleted in the upstream."""
