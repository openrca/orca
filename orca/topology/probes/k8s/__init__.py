from orca.topology.probes import probe
from orca.topology.probes.k8s import pod
from orca.topology.probes.k8s import deployment
from orca.topology.probes.k8s import service


NAME = 'k8s'
SUBPROBES = [
    pod.PodProbe,
    deployment.DeploymentProbe,
    service.ServiceProbe
]
