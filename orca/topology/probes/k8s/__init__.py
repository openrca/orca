from orca.topology.probes.k8s import pod
from orca.topology.probes.k8s import deployment
from orca.topology.probes.k8s import service
from orca.topology.probes.k8s import replica_set
from orca.topology.probes.k8s import node

PROBES = [
    pod.PodProbe,
    deployment.DeploymentProbe,
    service.ServiceProbe,
    replica_set.ReplicaSetProbe,
    node.NodeProbe
]

LINKERS = [
    pod.PodToServiceLinker,
    pod.PodToDeploymentLinker,
    pod.PodToNodeLinker,
    replica_set.ReplicaSetToDeploymentLinker
]
