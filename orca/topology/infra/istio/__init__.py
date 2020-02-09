from orca.topology.infra.istio import (destination_rule, gateway,
                                       virtual_service)

PROBES = [
    virtual_service.VirtualServiceProbe,
    destination_rule.DestinationRuleProbe,
    gateway.GatewayProbe
]

LINKERS = [
    virtual_service.VirtualServiceToGatewayLinker,
    virtual_service.VirtualServiceToServiceLinker,
    destination_rule.DestinationRuleToServiceLinker
]
