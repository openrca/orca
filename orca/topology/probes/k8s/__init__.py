from orca.topology.probes.k8s import pod
from orca.topology.probes.k8s import deployment
from orca.topology.probes.k8s import service
from orca.topology.probes.k8s import replica_set

PROBES = [
    pod.PodProbe,
    deployment.DeploymentProbe,
    service.ServiceProbe,
    replica_set.ReplicaSetProbe
]

LINKERS = [
    pod.PodToServiceLinker,
    pod.PodToDeploymentLinker,
    replica_set.ReplicaSetToDeploymentLinker
]
