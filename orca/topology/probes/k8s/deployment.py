from orca.topology.probes.k8s import probe


class DeploymentProbe(probe.K8SProbe):

    def run(self):
        while True:
            print("fetching deployments..")
            import time
            time.sleep(1)
