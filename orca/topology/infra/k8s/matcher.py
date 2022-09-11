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

    """Base class for Kubernetes matchers."""


class ServiceToPodMatcher(Matcher):

    """Matcher for links between Service and Pod entities."""

    def are_linked(self, service, pod):
        matched_namespace = match_namespace(pod, service)
        matched_selector = match_selector(pod, service.properties.selector)
        return matched_namespace and matched_selector


class ReplicaSetToPodMatcher(Matcher):

    """Matcher for links between ReplicaSet and Pod entities."""

    def are_linked(self, replica_set, pod):
        matched_namespace = match_namespace(pod, replica_set)
        matched_selector = match_selector(pod, replica_set.properties.selector)
        return matched_namespace and matched_selector


class StatefulSetToPodMatcher(Matcher):

    """Matcher for links between Stateful Set and Pod entities."""

    def are_linked(self, stateful_set, pod):
        matched_namespace = match_namespace(pod, stateful_set)
        matched_selector = match_selector(pod, stateful_set.properties.selector)
        return matched_namespace and matched_selector


class DaemonSetToPodMatcher(Matcher):

    """Matcher for links between Daemon Set and Pod entities."""

    def are_linked(self, daemon_set, pod):
        matched_namespace = match_namespace(pod, daemon_set)
        matched_selector = match_selector(pod, daemon_set.properties.selector)
        return matched_namespace and matched_selector


class PodToNodeMatcher(Matcher):

    """Matcher for links between Pod and Node entities."""

    def are_linked(self, pod, node):
        return pod.properties.node == node.properties.name


class ServiceToEndpointsMatcher(Matcher):

    """Matcher for links between Service and Endpoint entities."""

    def are_linked(self, service, endpoints):
        matched_namespace = match_namespace(endpoints, service)
        matched_name = endpoints.properties.name == service.properties.name
        return matched_namespace and matched_name


class DeploymentToReplicaSetMatcher(Matcher):

    """Matcher for links between Deployment and Replica Set entities."""

    def are_linked(self, deployment, replica_set):
        matched_namespace = match_namespace(replica_set, deployment)
        matched_selector = match_selector(replica_set, deployment.properties.selector)
        return matched_namespace and matched_selector


class PodToConfigMapMatcher(Matcher):

    """Matcher for links between Pod and Config Map entities."""

    def are_linked(self, pod, config_map):
        matched_namespace = match_namespace(config_map, pod)
        matched_env = self._match_env(config_map, pod)
        matched_volume = self._match_volume(config_map, pod)
        return matched_namespace and (matched_env or matched_volume)

    def _match_env(self, config_map, pod):
        for container in pod.properties.containers:
            if container.env:
                for env_var in container.env:
                    if (
                        env_var.value_from
                        and env_var.value_from.config_map_key_ref
                        and env_var.value_from.config_map_key_ref.name == config_map.properties.name
                    ):
                        return True
            if container.env_from:
                for env_from in container.env_from:
                    if (
                        env_from.config_map_ref
                        and env_from.config_map_ref.name == config_map.properties.name
                    ):
                        return True
        return False

    def _match_volume(self, config_map, pod):
        for volume in pod.properties.volumes:
            if volume.config_map and volume.config_map.name == config_map.properties.name:
                return True
        return False


class PodToSecretMatcher(Matcher):

    """Matcher for links between Pod and Secret entities."""

    def are_linked(self, pod, secret):
        matched_namespace = match_namespace(secret, pod)
        matched_env = self._match_env(secret, pod)
        matched_volume = self._match_volume(secret, pod)
        return matched_namespace and (matched_env or matched_volume)

    def _match_env(self, secret, pod):
        for container in pod.properties.containers:
            if container.env:
                for env_var in container.env:
                    if (
                        env_var.value_from
                        and env_var.value_from.secret_key_ref
                        and env_var.value_from.secret_key_ref.name == secret.properties.name
                    ):
                        return True
            if container.env_from:
                for env_from in container.env_from:
                    if env_from.secret_ref and env_from.secret_ref.name == secret.properties.name:
                        return True
        return False

    def _match_volume(self, secret, pod):
        for volume in pod.properties.volumes:
            if volume.secret and volume.secret.secret_name == secret.properties.name:
                return True
        return False


class HorizontalPodAutoscalerMatcher(Matcher):

    """Generic matcher for links between Horizontal Pod Autoscaler and related objects."""

    def are_linked(self, hpa, obj):
        matched_namespace = match_namespace(obj, hpa)
        matched_target_ref = self._match_target_ref(obj, hpa)
        return matched_namespace and matched_target_ref

    def _match_target_ref(self, obj, hpa):
        return (
            hpa.properties.target_ref.kind == obj.kind
            and hpa.properties.target_ref.name == obj.properties.name
        )


class PersistentVolumeToStorageClassMatcher(Matcher):

    """Matcher for links between Persistent Volume and Storage Class entities."""

    def are_linked(self, persistent_volume, storage_class):
        if (
            persistent_volume.properties.storage_class
            and persistent_volume.properties.storage_class == storage_class.properties.name
        ):
            return True
        return False


class PersistentVolumeClaimToPersistentVolumeMatcher(Matcher):

    """Matcher for links between Persistent Volume Claim and Persistent Volume entities."""

    def are_linked(self, pvc, pv):
        return pv.properties.name == pvc.properties.volume_name


class PodToPersistentVolumeClaimMatcher(Matcher):

    """Matcher for links between Pod and Persistent Volume Claim entities."""

    def are_linked(self, pod, pvc):
        matched_namespace = match_namespace(pvc, pod)
        matched_volume = self._match_volume(pvc, pod)
        return matched_namespace and matched_volume

    def _match_volume(self, pvc, pod):
        for volume in pod.properties.volumes:
            if (
                volume.persistent_volume_claim
                and volume.persistent_volume_claim.claim_name == pvc.properties.name
            ):
                return True
        return False


class ClusterToNodeMatcher(Matcher):

    """Matcher for links between Cluster and Node entities."""

    def are_linked(self, cluster, node):
        return True


class NamespaceMatcher(Matcher):

    """Generic matcher for links between Namespace and related objects."""

    def are_linked(self, obj, namespace):
        return namespace.properties.name == obj.properties.namespace


class IngressToServiceMatcher(Matcher):

    """Matcher for links between Ingress and Service entities."""

    def are_linked(self, ingress, service):
        matched_namespace = match_namespace(ingress, service)
        matched_service = self._match_rules(ingress, service)
        return matched_namespace and matched_service

    def _match_rules(self, ingress, service):
        for rule in ingress.properties.rules:
            for path in rule.paths:
                if path.service_name == service.properties.name:
                    return True
        return False


class JobToPodMatcher(Matcher):

    """Matcher for links between Job and Pod entities."""

    def are_linked(self, job, pod):
        matched_namespace = match_namespace(job, pod)
        matched_selector = match_selector(pod, job.properties.selector)
        return matched_namespace and matched_selector


class CronJobToJobMatcher(Matcher):

    """Matcher for links between CronJob and Job entities."""

    def are_linked(self, cron_job, job):
        matched_namespace = match_namespace(cron_job, job)
        matched_cron_job = self._match_cron_job(cron_job, job)
        return matched_namespace and matched_cron_job

    def _match_cron_job(self, cron_job, job):
        if job.properties.cron_job_ref:
            if job.properties.cron_job_ref.uid == cron_job.id:
                return True
        return False


def match_namespace(obj_a, obj_b):
    return obj_a.properties.namespace == obj_b.properties.namespace


def match_selector(obj, selector):
    labels = obj.properties.labels
    if selector and labels:
        return all(item in labels.items() for item in selector.items())
    return False
