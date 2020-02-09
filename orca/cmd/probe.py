from orca.topology import manager


def main():
    probe_manager = manager.Manager()
    probe_manager.initialize()
    probe_manager.run()
