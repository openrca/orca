# Copyright 2021 OpenRCA Authors
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

import re

from elastalert.enhancements import BaseEnhancement


class MongoDBHostFailedInReplicaSet(BaseEnhancement):

    def process(self, match):
        data = match["log_processed"]
        host = data["attr"]["host"]
        host_match = re.search(r"^.+-(\w+)-(\d+)\..+$", host)
        rs = host_match.group(1).capitalize()
        member = host_match.group(2).capitalize()
        alert_name = "MongoDBHost%sFailedInReplicaSet%s" % (member, rs)
        match["name"] = alert_name


class MongoDBHeartbeatFailed(BaseEnhancement):

    def process(self, match):
        data = match["log_processed"]
        host = data["attr"]["target"]
        host_match = re.search(r"^.+-(\w+)-(\d+)\..+$", host)
        rs = host_match.group(1).capitalize()
        member = host_match.group(2).capitalize()
        alert_name = "MongoDBHeartbeatFailedToHost%sInReplicaSet%s" % (member, rs)
        match["name"] = alert_name
