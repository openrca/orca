from orca.topology.probes.k8s import (cluster, config_map, deployment, node,
                                      pod, replica_set, secret, service)

PROBES = [
    pod.PodProbe,
    deployment.DeploymentProbe,
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
    pod.PodToNodeLinker,
    replica_set.ReplicaSetToDeploymentLinker,
    config_map.ConfigMapToPodLinker,
    secret.SecretToPodLinker,
    node.NodeToClusterLinker
]
