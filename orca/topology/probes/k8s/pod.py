from orca.topology.probes import probe


class PodProbe(probe.Probe):

    def run(self):
        while True:
            print("fetching pods..")
            import time
            time.sleep(1)
