from orca.topology.probes.k8s import pod
from orca.topology.probes.k8s import deployment
from orca.topology.probes.k8s import service

PROBES = [
    pod.PodProbe,
    deployment.DeploymentProbe,
    service.ServiceProbe
]

LINKERS = [
    pod.PodToServiceLinker
]
