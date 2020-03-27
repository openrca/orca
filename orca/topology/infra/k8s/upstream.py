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

from orca.topology import upstream


class UpstreamProxy(upstream.UpstreamProxy):

    """Upstream proxy for Kubernetes."""

    def get_all(self):
        return self._client.get_all()

    def get_events(self, handler):
        for event in self._client.watch():
            event_type = event['type']
            entity = event['object']
            if event_type == "ADDED":
                handler.on_added(entity)
            elif event_type == "MODIFIED":
                handler.on_updated(entity)
            elif event_type == "DELETED":
                handler.on_deleted(entity)
            else:
                raise Exception("Unknown event type: %s" % event_type)
