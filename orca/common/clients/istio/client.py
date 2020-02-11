from orca.common.clients.k8s import client as k8s


class ResourceProxyFactory(object):

    @staticmethod
    def get(k8s_client, kind):
        if kind == 'virtual_service':
            return k8s.CustomResourceProxy(
                k8s_client.CustomObjectsApi().list_cluster_custom_object,
                group="networking.istio.io",
                version="v1alpha3",
                plural="virtualservices")
        elif kind == 'destination_rule':
            return k8s.CustomResourceProxy(
                k8s_client.CustomObjectsApi().list_cluster_custom_object,
                group="networking.istio.io",
                version="v1alpha3",
                plural="destinationrules")
        elif kind == 'gateway':
            return k8s.CustomResourceProxy(
                k8s_client.CustomObjectsApi().list_cluster_custom_object,
                group="networking.istio.io",
                version="v1alpha3",
                plural="gateways")
        else:
            raise Exception("Unknown kind %s" % kind)
