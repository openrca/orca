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


class Extractor(abc.ABC):

    @abc.abstractmethod
    def get_origin(self):
        """Returns origin of extracted entities."""

    @abc.abstractmethod
    def get_kind(self):
        """Returns kind of extracted entities."""

    @abc.abstractmethod
    def extract(self, entity):
        """Extracts graph node from given raw entity."""

    def get_extended_kind(self):
        return "%s/%s" % (self.get_origin(), self.get_kind())
