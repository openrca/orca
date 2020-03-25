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

from orca.topology import matcher


class Matcher(matcher.Matcher):

    """Base class for Alert matchers."""


class AlertToSourceMatcher(Matcher):

    """Generic matcher for links between Alert and source objects."""

    def are_linked(self, alert, obj):
        source_mapping = alert.properties.source_mapping
        if not source_mapping.origin == obj.origin:
            return False
        if not source_mapping.kind == obj.kind:
            return False
        mapping_items = source_mapping.properties.items()
        obj_items = obj.properties.items()
        return all(item in obj_items for item in mapping_items)
