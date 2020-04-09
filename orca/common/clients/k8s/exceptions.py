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

from orca.common.clients import exceptions


class KubernetesClientError(exceptions.APIClientError):

    message = "Failed to perform request to Kubernetes API: %(reason)s."


class WatchError(KubernetesClientError):

    message = "An error occurred in the watch stream: %(reason)s."


class UnknownWatchEvent(KubernetesClientError):

    message = "Encountered an event of unknown type in the watch stream: %(event_type)s."
