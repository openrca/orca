from orca.topology.probes import probe


class DeploymentProbe(probe.Probe):

    def run(self):
        while True:
            print("fetching deployments..")
            import time
            time.sleep(1)
