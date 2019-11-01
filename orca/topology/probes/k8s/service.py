from orca.topology.probes import probe


class ServiceProbe(probe.Probe):

    def run(self):
        while True:
            print("fetching services..")
            import time
            time.sleep(1)
