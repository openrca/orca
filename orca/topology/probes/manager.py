import cotyledon

from orca.topology import probes


class Manager(cotyledon.ServiceManager):

    def __init__(self):
        super().__init__()
        for name, subprobes in probes.PROBES.items():
            print(name)
            for probe in subprobes:
                self.add(probe, workers=1)
