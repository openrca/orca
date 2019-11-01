from orca.topology.probes.k8s import probe


class ServiceProbe(probe.K8SProbe):

    def run(self):
        while True:
            print("fetching services..")
            import time
            time.sleep(1)
