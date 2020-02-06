from orca.topology.infra.istio import virtual_service, destination_rule

PROBES = [
    virtual_service.VirtualServiceProbe,
    destination_rule.DestinationRuleProbe
]
