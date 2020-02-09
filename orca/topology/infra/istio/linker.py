def match_host_to_service(namespace, host, service):
    host_parts = host.split('.')
    service_name = host_parts[0]
    service_namespace = host_parts[1] if len(host_parts) > 1 else namespace
    match_name = service_name == service.properties.name
    match_namespace = service_namespace == service.properties.namespace
    return match_name and match_namespace
