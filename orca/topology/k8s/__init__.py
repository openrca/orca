from orca.topology.k8s import (cluster, config_map, deployment, node, pod, replica_set, secret,
                               service, stateful_set, daemon_set)

PROBES = [
    pod.PodProbe,
    deployment.DeploymentProbe,
    stateful_set.StatefulSetProbe,
    daemon_set.DaemonSetProbe,
    service.ServiceProbe,
    replica_set.ReplicaSetProbe,
    node.NodeProbe,
    cluster.ClusterProbe,
    config_map.ConfigMapProbe,
    secret.SecretProbe
]

LINKERS = [
    pod.PodToServiceLinker,
    pod.PodToReplicaSetLinker,
    pod.PodToStatefulSetLinker,
    pod.PodToDaemonSetLinker,
    pod.PodToNodeLinker,
    replica_set.ReplicaSetToDeploymentLinker,
    config_map.ConfigMapToPodLinker,
    secret.SecretToPodLinker,
    node.NodeToClusterLinker
]
