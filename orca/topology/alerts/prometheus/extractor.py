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

import dateparser

from orca.common import str_utils, utils
from orca.topology.alerts import extractor
from orca.topology.alerts import properties as alert_props


class Extractor(extractor.Extractor):

    """Base class for Prometheus extractors."""

    @property
    def origin(self):
        return "prometheus"

    @classmethod
    def get(cls):
        return super().get("prometheus")


class AlertExtractor(Extractor):

    """Extractor for Alert entities retrieved from Prometheus API."""

    def _extract_name(self, entity):
        labels = self._extract_labels(entity)
        return labels["alertname"]

    def _extract_status(self, entity):
        if entity["state"] == "firing":
            return alert_props.AlertStatus.UP
        return alert_props.AlertStatus.DOWN

    def _extract_activation_time(self, entity):
        return int(dateparser.parse(entity["activeAt"]).timestamp())

    def _extract_source_labels(self, entity):
        labels = self._extract_labels(entity)
        return utils.flatten_dict(labels, sep=".")

    def _extract_properties(self, entity):
        properties = {}
        properties["severity"] = self._extract_severity(entity)
        properties["message"] = self._extract_message(entity)
        properties["labels"] = self._extract_labels(entity)
        properties["annotations"] = self._extract_annotations(entity)
        return properties

    def _extract_severity(self, entity):
        labels = self._extract_labels(entity)
        return labels.get("severity")

    def _extract_message(self, entity):
        annotations = self._extract_annotations(entity)
        message = annotations.get("message")
        if not message:
            message = annotations.get("summary")
        if message:
            return str_utils.escape(message)

    def _extract_labels(self, entity):
        return entity["labels"]

    def _extract_annotations(self, entity):
        return entity["annotations"]


class AlertEventExtractor(AlertExtractor):

    """Extractor for Alert events received from Alertmanager."""

    def _extract_status(self, entity):
        return entity["status"]

    def _extract_activation_time(self, entity):
        return int(dateparser.parse(entity["startsAt"]).timestamp())
