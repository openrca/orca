from orca.topology.probes.k8s import pod
from orca.topology.probes.k8s import deployment
from orca.topology.probes.k8s import service
from orca.topology.probes.k8s import config_map
from orca.topology.probes.k8s import secret
from orca.topology.probes.k8s import replica_set
from orca.topology.probes.k8s import node

PROBES = [
    pod.PodProbe,
    deployment.DeploymentProbe,
    service.ServiceProbe,
    replica_set.ReplicaSetProbe,
    node.NodeProbe,
    config_map.ConfigMapProbe,
    secret.SecretProbe
]

LINKERS = [
    pod.PodToServiceLinker,
    pod.PodToReplicaSetLinker,
    pod.PodToNodeLinker,
    replica_set.ReplicaSetToDeploymentLinker,
    config_map.ConfigMapToPodLinker,
    secret.SecretToPodLinker
]
