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

def match_host_to_service(namespace, host, service):
    host_parts = host.split('.')
    service_name = host_parts[0]
    service_namespace = host_parts[1] if len(host_parts) > 1 else namespace
    match_name = service_name == service.properties.name
    match_namespace = service_namespace == service.properties.namespace
    return match_name and match_namespace
