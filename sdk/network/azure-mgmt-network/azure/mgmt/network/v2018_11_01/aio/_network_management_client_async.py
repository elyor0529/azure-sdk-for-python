# coding=utf-8
# --------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# Code generated by Microsoft (R) AutoRest Code Generator.
# Changes may cause incorrect behavior and will be lost if the code is regenerated.
# --------------------------------------------------------------------------

from typing import Any, Optional, TYPE_CHECKING

from azure.mgmt.core import AsyncARMPipelineClient
from msrest import Deserializer, Serializer

if TYPE_CHECKING:
    # pylint: disable=unused-import,ungrouped-imports
    from azure.core.credentials_async import AsyncTokenCredential

from ._configuration_async import NetworkManagementClientConfiguration
from .operations_async import ApplicationGatewaysOperations
from .operations_async import ApplicationSecurityGroupsOperations
from .operations_async import AvailableDelegationsOperations
from .operations_async import AvailableResourceGroupDelegationsOperations
from .operations_async import AzureFirewallsOperations
from .operations_async import AzureFirewallFqdnTagsOperations
from .operations_async import NetworkManagementClientOperationsMixin
from .operations_async import DdosCustomPoliciesOperations
from .operations_async import DdosProtectionPlansOperations
from .operations_async import AvailableEndpointServicesOperations
from .operations_async import ExpressRouteCircuitAuthorizationsOperations
from .operations_async import ExpressRouteCircuitPeeringsOperations
from .operations_async import ExpressRouteCircuitConnectionsOperations
from .operations_async import ExpressRouteCircuitsOperations
from .operations_async import ExpressRouteServiceProvidersOperations
from .operations_async import ExpressRouteCrossConnectionsOperations
from .operations_async import ExpressRouteCrossConnectionPeeringsOperations
from .operations_async import ExpressRouteGatewaysOperations
from .operations_async import ExpressRouteConnectionsOperations
from .operations_async import ExpressRoutePortsLocationsOperations
from .operations_async import ExpressRoutePortsOperations
from .operations_async import ExpressRouteLinksOperations
from .operations_async import InterfaceEndpointsOperations
from .operations_async import LoadBalancersOperations
from .operations_async import LoadBalancerBackendAddressPoolsOperations
from .operations_async import LoadBalancerFrontendIPConfigurationsOperations
from .operations_async import InboundNatRulesOperations
from .operations_async import LoadBalancerLoadBalancingRulesOperations
from .operations_async import LoadBalancerOutboundRulesOperations
from .operations_async import LoadBalancerNetworkInterfacesOperations
from .operations_async import LoadBalancerProbesOperations
from .operations_async import NetworkInterfacesOperations
from .operations_async import NetworkInterfaceIPConfigurationsOperations
from .operations_async import NetworkInterfaceLoadBalancersOperations
from .operations_async import NetworkInterfaceTapConfigurationsOperations
from .operations_async import NetworkProfilesOperations
from .operations_async import NetworkSecurityGroupsOperations
from .operations_async import SecurityRulesOperations
from .operations_async import DefaultSecurityRulesOperations
from .operations_async import NetworkWatchersOperations
from .operations_async import PacketCapturesOperations
from .operations_async import ConnectionMonitorsOperations
from .operations_async import Operations
from .operations_async import PublicIPAddressesOperations
from .operations_async import PublicIPPrefixesOperations
from .operations_async import RouteFiltersOperations
from .operations_async import RouteFilterRulesOperations
from .operations_async import RouteTablesOperations
from .operations_async import RoutesOperations
from .operations_async import BgpServiceCommunitiesOperations
from .operations_async import ServiceEndpointPoliciesOperations
from .operations_async import ServiceEndpointPolicyDefinitionsOperations
from .operations_async import UsagesOperations
from .operations_async import VirtualNetworksOperations
from .operations_async import SubnetsOperations
from .operations_async import VirtualNetworkPeeringsOperations
from .operations_async import VirtualNetworkGatewaysOperations
from .operations_async import VirtualNetworkGatewayConnectionsOperations
from .operations_async import LocalNetworkGatewaysOperations
from .operations_async import VirtualNetworkTapsOperations
from .operations_async import VirtualWansOperations
from .operations_async import VpnSitesOperations
from .operations_async import VpnSitesConfigurationOperations
from .operations_async import VirtualHubsOperations
from .operations_async import HubVirtualNetworkConnectionsOperations
from .operations_async import VpnGatewaysOperations
from .operations_async import VpnConnectionsOperations
from .operations_async import P2SVpnServerConfigurationsOperations
from .operations_async import P2SVpnGatewaysOperations
from .. import models


class NetworkManagementClient(NetworkManagementClientOperationsMixin):
    """Network Client.

    :ivar application_gateways: ApplicationGatewaysOperations operations
    :vartype application_gateways: azure.mgmt.network.v2018_11_01.aio.operations_async.ApplicationGatewaysOperations
    :ivar application_security_groups: ApplicationSecurityGroupsOperations operations
    :vartype application_security_groups: azure.mgmt.network.v2018_11_01.aio.operations_async.ApplicationSecurityGroupsOperations
    :ivar available_delegations: AvailableDelegationsOperations operations
    :vartype available_delegations: azure.mgmt.network.v2018_11_01.aio.operations_async.AvailableDelegationsOperations
    :ivar available_resource_group_delegations: AvailableResourceGroupDelegationsOperations operations
    :vartype available_resource_group_delegations: azure.mgmt.network.v2018_11_01.aio.operations_async.AvailableResourceGroupDelegationsOperations
    :ivar azure_firewalls: AzureFirewallsOperations operations
    :vartype azure_firewalls: azure.mgmt.network.v2018_11_01.aio.operations_async.AzureFirewallsOperations
    :ivar azure_firewall_fqdn_tags: AzureFirewallFqdnTagsOperations operations
    :vartype azure_firewall_fqdn_tags: azure.mgmt.network.v2018_11_01.aio.operations_async.AzureFirewallFqdnTagsOperations
    :ivar ddos_custom_policies: DdosCustomPoliciesOperations operations
    :vartype ddos_custom_policies: azure.mgmt.network.v2018_11_01.aio.operations_async.DdosCustomPoliciesOperations
    :ivar ddos_protection_plans: DdosProtectionPlansOperations operations
    :vartype ddos_protection_plans: azure.mgmt.network.v2018_11_01.aio.operations_async.DdosProtectionPlansOperations
    :ivar available_endpoint_services: AvailableEndpointServicesOperations operations
    :vartype available_endpoint_services: azure.mgmt.network.v2018_11_01.aio.operations_async.AvailableEndpointServicesOperations
    :ivar express_route_circuit_authorizations: ExpressRouteCircuitAuthorizationsOperations operations
    :vartype express_route_circuit_authorizations: azure.mgmt.network.v2018_11_01.aio.operations_async.ExpressRouteCircuitAuthorizationsOperations
    :ivar express_route_circuit_peerings: ExpressRouteCircuitPeeringsOperations operations
    :vartype express_route_circuit_peerings: azure.mgmt.network.v2018_11_01.aio.operations_async.ExpressRouteCircuitPeeringsOperations
    :ivar express_route_circuit_connections: ExpressRouteCircuitConnectionsOperations operations
    :vartype express_route_circuit_connections: azure.mgmt.network.v2018_11_01.aio.operations_async.ExpressRouteCircuitConnectionsOperations
    :ivar express_route_circuits: ExpressRouteCircuitsOperations operations
    :vartype express_route_circuits: azure.mgmt.network.v2018_11_01.aio.operations_async.ExpressRouteCircuitsOperations
    :ivar express_route_service_providers: ExpressRouteServiceProvidersOperations operations
    :vartype express_route_service_providers: azure.mgmt.network.v2018_11_01.aio.operations_async.ExpressRouteServiceProvidersOperations
    :ivar express_route_cross_connections: ExpressRouteCrossConnectionsOperations operations
    :vartype express_route_cross_connections: azure.mgmt.network.v2018_11_01.aio.operations_async.ExpressRouteCrossConnectionsOperations
    :ivar express_route_cross_connection_peerings: ExpressRouteCrossConnectionPeeringsOperations operations
    :vartype express_route_cross_connection_peerings: azure.mgmt.network.v2018_11_01.aio.operations_async.ExpressRouteCrossConnectionPeeringsOperations
    :ivar express_route_gateways: ExpressRouteGatewaysOperations operations
    :vartype express_route_gateways: azure.mgmt.network.v2018_11_01.aio.operations_async.ExpressRouteGatewaysOperations
    :ivar express_route_connections: ExpressRouteConnectionsOperations operations
    :vartype express_route_connections: azure.mgmt.network.v2018_11_01.aio.operations_async.ExpressRouteConnectionsOperations
    :ivar express_route_ports_locations: ExpressRoutePortsLocationsOperations operations
    :vartype express_route_ports_locations: azure.mgmt.network.v2018_11_01.aio.operations_async.ExpressRoutePortsLocationsOperations
    :ivar express_route_ports: ExpressRoutePortsOperations operations
    :vartype express_route_ports: azure.mgmt.network.v2018_11_01.aio.operations_async.ExpressRoutePortsOperations
    :ivar express_route_links: ExpressRouteLinksOperations operations
    :vartype express_route_links: azure.mgmt.network.v2018_11_01.aio.operations_async.ExpressRouteLinksOperations
    :ivar interface_endpoints: InterfaceEndpointsOperations operations
    :vartype interface_endpoints: azure.mgmt.network.v2018_11_01.aio.operations_async.InterfaceEndpointsOperations
    :ivar load_balancers: LoadBalancersOperations operations
    :vartype load_balancers: azure.mgmt.network.v2018_11_01.aio.operations_async.LoadBalancersOperations
    :ivar load_balancer_backend_address_pools: LoadBalancerBackendAddressPoolsOperations operations
    :vartype load_balancer_backend_address_pools: azure.mgmt.network.v2018_11_01.aio.operations_async.LoadBalancerBackendAddressPoolsOperations
    :ivar load_balancer_frontend_ip_configurations: LoadBalancerFrontendIPConfigurationsOperations operations
    :vartype load_balancer_frontend_ip_configurations: azure.mgmt.network.v2018_11_01.aio.operations_async.LoadBalancerFrontendIPConfigurationsOperations
    :ivar inbound_nat_rules: InboundNatRulesOperations operations
    :vartype inbound_nat_rules: azure.mgmt.network.v2018_11_01.aio.operations_async.InboundNatRulesOperations
    :ivar load_balancer_load_balancing_rules: LoadBalancerLoadBalancingRulesOperations operations
    :vartype load_balancer_load_balancing_rules: azure.mgmt.network.v2018_11_01.aio.operations_async.LoadBalancerLoadBalancingRulesOperations
    :ivar load_balancer_outbound_rules: LoadBalancerOutboundRulesOperations operations
    :vartype load_balancer_outbound_rules: azure.mgmt.network.v2018_11_01.aio.operations_async.LoadBalancerOutboundRulesOperations
    :ivar load_balancer_network_interfaces: LoadBalancerNetworkInterfacesOperations operations
    :vartype load_balancer_network_interfaces: azure.mgmt.network.v2018_11_01.aio.operations_async.LoadBalancerNetworkInterfacesOperations
    :ivar load_balancer_probes: LoadBalancerProbesOperations operations
    :vartype load_balancer_probes: azure.mgmt.network.v2018_11_01.aio.operations_async.LoadBalancerProbesOperations
    :ivar network_interfaces: NetworkInterfacesOperations operations
    :vartype network_interfaces: azure.mgmt.network.v2018_11_01.aio.operations_async.NetworkInterfacesOperations
    :ivar network_interface_ip_configurations: NetworkInterfaceIPConfigurationsOperations operations
    :vartype network_interface_ip_configurations: azure.mgmt.network.v2018_11_01.aio.operations_async.NetworkInterfaceIPConfigurationsOperations
    :ivar network_interface_load_balancers: NetworkInterfaceLoadBalancersOperations operations
    :vartype network_interface_load_balancers: azure.mgmt.network.v2018_11_01.aio.operations_async.NetworkInterfaceLoadBalancersOperations
    :ivar network_interface_tap_configurations: NetworkInterfaceTapConfigurationsOperations operations
    :vartype network_interface_tap_configurations: azure.mgmt.network.v2018_11_01.aio.operations_async.NetworkInterfaceTapConfigurationsOperations
    :ivar network_profiles: NetworkProfilesOperations operations
    :vartype network_profiles: azure.mgmt.network.v2018_11_01.aio.operations_async.NetworkProfilesOperations
    :ivar network_security_groups: NetworkSecurityGroupsOperations operations
    :vartype network_security_groups: azure.mgmt.network.v2018_11_01.aio.operations_async.NetworkSecurityGroupsOperations
    :ivar security_rules: SecurityRulesOperations operations
    :vartype security_rules: azure.mgmt.network.v2018_11_01.aio.operations_async.SecurityRulesOperations
    :ivar default_security_rules: DefaultSecurityRulesOperations operations
    :vartype default_security_rules: azure.mgmt.network.v2018_11_01.aio.operations_async.DefaultSecurityRulesOperations
    :ivar network_watchers: NetworkWatchersOperations operations
    :vartype network_watchers: azure.mgmt.network.v2018_11_01.aio.operations_async.NetworkWatchersOperations
    :ivar packet_captures: PacketCapturesOperations operations
    :vartype packet_captures: azure.mgmt.network.v2018_11_01.aio.operations_async.PacketCapturesOperations
    :ivar connection_monitors: ConnectionMonitorsOperations operations
    :vartype connection_monitors: azure.mgmt.network.v2018_11_01.aio.operations_async.ConnectionMonitorsOperations
    :ivar operations: Operations operations
    :vartype operations: azure.mgmt.network.v2018_11_01.aio.operations_async.Operations
    :ivar public_ip_addresses: PublicIPAddressesOperations operations
    :vartype public_ip_addresses: azure.mgmt.network.v2018_11_01.aio.operations_async.PublicIPAddressesOperations
    :ivar public_ip_prefixes: PublicIPPrefixesOperations operations
    :vartype public_ip_prefixes: azure.mgmt.network.v2018_11_01.aio.operations_async.PublicIPPrefixesOperations
    :ivar route_filters: RouteFiltersOperations operations
    :vartype route_filters: azure.mgmt.network.v2018_11_01.aio.operations_async.RouteFiltersOperations
    :ivar route_filter_rules: RouteFilterRulesOperations operations
    :vartype route_filter_rules: azure.mgmt.network.v2018_11_01.aio.operations_async.RouteFilterRulesOperations
    :ivar route_tables: RouteTablesOperations operations
    :vartype route_tables: azure.mgmt.network.v2018_11_01.aio.operations_async.RouteTablesOperations
    :ivar routes: RoutesOperations operations
    :vartype routes: azure.mgmt.network.v2018_11_01.aio.operations_async.RoutesOperations
    :ivar bgp_service_communities: BgpServiceCommunitiesOperations operations
    :vartype bgp_service_communities: azure.mgmt.network.v2018_11_01.aio.operations_async.BgpServiceCommunitiesOperations
    :ivar service_endpoint_policies: ServiceEndpointPoliciesOperations operations
    :vartype service_endpoint_policies: azure.mgmt.network.v2018_11_01.aio.operations_async.ServiceEndpointPoliciesOperations
    :ivar service_endpoint_policy_definitions: ServiceEndpointPolicyDefinitionsOperations operations
    :vartype service_endpoint_policy_definitions: azure.mgmt.network.v2018_11_01.aio.operations_async.ServiceEndpointPolicyDefinitionsOperations
    :ivar usages: UsagesOperations operations
    :vartype usages: azure.mgmt.network.v2018_11_01.aio.operations_async.UsagesOperations
    :ivar virtual_networks: VirtualNetworksOperations operations
    :vartype virtual_networks: azure.mgmt.network.v2018_11_01.aio.operations_async.VirtualNetworksOperations
    :ivar subnets: SubnetsOperations operations
    :vartype subnets: azure.mgmt.network.v2018_11_01.aio.operations_async.SubnetsOperations
    :ivar virtual_network_peerings: VirtualNetworkPeeringsOperations operations
    :vartype virtual_network_peerings: azure.mgmt.network.v2018_11_01.aio.operations_async.VirtualNetworkPeeringsOperations
    :ivar virtual_network_gateways: VirtualNetworkGatewaysOperations operations
    :vartype virtual_network_gateways: azure.mgmt.network.v2018_11_01.aio.operations_async.VirtualNetworkGatewaysOperations
    :ivar virtual_network_gateway_connections: VirtualNetworkGatewayConnectionsOperations operations
    :vartype virtual_network_gateway_connections: azure.mgmt.network.v2018_11_01.aio.operations_async.VirtualNetworkGatewayConnectionsOperations
    :ivar local_network_gateways: LocalNetworkGatewaysOperations operations
    :vartype local_network_gateways: azure.mgmt.network.v2018_11_01.aio.operations_async.LocalNetworkGatewaysOperations
    :ivar virtual_network_taps: VirtualNetworkTapsOperations operations
    :vartype virtual_network_taps: azure.mgmt.network.v2018_11_01.aio.operations_async.VirtualNetworkTapsOperations
    :ivar virtual_wans: VirtualWansOperations operations
    :vartype virtual_wans: azure.mgmt.network.v2018_11_01.aio.operations_async.VirtualWansOperations
    :ivar vpn_sites: VpnSitesOperations operations
    :vartype vpn_sites: azure.mgmt.network.v2018_11_01.aio.operations_async.VpnSitesOperations
    :ivar vpn_sites_configuration: VpnSitesConfigurationOperations operations
    :vartype vpn_sites_configuration: azure.mgmt.network.v2018_11_01.aio.operations_async.VpnSitesConfigurationOperations
    :ivar virtual_hubs: VirtualHubsOperations operations
    :vartype virtual_hubs: azure.mgmt.network.v2018_11_01.aio.operations_async.VirtualHubsOperations
    :ivar hub_virtual_network_connections: HubVirtualNetworkConnectionsOperations operations
    :vartype hub_virtual_network_connections: azure.mgmt.network.v2018_11_01.aio.operations_async.HubVirtualNetworkConnectionsOperations
    :ivar vpn_gateways: VpnGatewaysOperations operations
    :vartype vpn_gateways: azure.mgmt.network.v2018_11_01.aio.operations_async.VpnGatewaysOperations
    :ivar vpn_connections: VpnConnectionsOperations operations
    :vartype vpn_connections: azure.mgmt.network.v2018_11_01.aio.operations_async.VpnConnectionsOperations
    :ivar p2_svpn_server_configurations: P2SVpnServerConfigurationsOperations operations
    :vartype p2_svpn_server_configurations: azure.mgmt.network.v2018_11_01.aio.operations_async.P2SVpnServerConfigurationsOperations
    :ivar p2_svpn_gateways: P2SVpnGatewaysOperations operations
    :vartype p2_svpn_gateways: azure.mgmt.network.v2018_11_01.aio.operations_async.P2SVpnGatewaysOperations
    :param credential: Credential needed for the client to connect to Azure.
    :type credential: ~azure.core.credentials_async.AsyncTokenCredential
    :param subscription_id: The subscription credentials which uniquely identify the Microsoft Azure subscription. The subscription ID forms part of the URI for every service call.
    :type subscription_id: str
    :param str base_url: Service URL
    :keyword int polling_interval: Default waiting time between two polls for LRO operations if no Retry-After header is present.
    """

    def __init__(
        self,
        credential: "AsyncTokenCredential",
        subscription_id: str,
        base_url: Optional[str] = None,
        **kwargs: Any
    ) -> None:
        if not base_url:
            base_url = 'https://management.azure.com'
        self._config = NetworkManagementClientConfiguration(credential, subscription_id, **kwargs)
        self._client = AsyncARMPipelineClient(base_url=base_url, config=self._config, **kwargs)

        client_models = {k: v for k, v in models.__dict__.items() if isinstance(v, type)}
        self._serialize = Serializer(client_models)
        self._deserialize = Deserializer(client_models)

        self.application_gateways = ApplicationGatewaysOperations(
            self._client, self._config, self._serialize, self._deserialize)
        self.application_security_groups = ApplicationSecurityGroupsOperations(
            self._client, self._config, self._serialize, self._deserialize)
        self.available_delegations = AvailableDelegationsOperations(
            self._client, self._config, self._serialize, self._deserialize)
        self.available_resource_group_delegations = AvailableResourceGroupDelegationsOperations(
            self._client, self._config, self._serialize, self._deserialize)
        self.azure_firewalls = AzureFirewallsOperations(
            self._client, self._config, self._serialize, self._deserialize)
        self.azure_firewall_fqdn_tags = AzureFirewallFqdnTagsOperations(
            self._client, self._config, self._serialize, self._deserialize)
        self.ddos_custom_policies = DdosCustomPoliciesOperations(
            self._client, self._config, self._serialize, self._deserialize)
        self.ddos_protection_plans = DdosProtectionPlansOperations(
            self._client, self._config, self._serialize, self._deserialize)
        self.available_endpoint_services = AvailableEndpointServicesOperations(
            self._client, self._config, self._serialize, self._deserialize)
        self.express_route_circuit_authorizations = ExpressRouteCircuitAuthorizationsOperations(
            self._client, self._config, self._serialize, self._deserialize)
        self.express_route_circuit_peerings = ExpressRouteCircuitPeeringsOperations(
            self._client, self._config, self._serialize, self._deserialize)
        self.express_route_circuit_connections = ExpressRouteCircuitConnectionsOperations(
            self._client, self._config, self._serialize, self._deserialize)
        self.express_route_circuits = ExpressRouteCircuitsOperations(
            self._client, self._config, self._serialize, self._deserialize)
        self.express_route_service_providers = ExpressRouteServiceProvidersOperations(
            self._client, self._config, self._serialize, self._deserialize)
        self.express_route_cross_connections = ExpressRouteCrossConnectionsOperations(
            self._client, self._config, self._serialize, self._deserialize)
        self.express_route_cross_connection_peerings = ExpressRouteCrossConnectionPeeringsOperations(
            self._client, self._config, self._serialize, self._deserialize)
        self.express_route_gateways = ExpressRouteGatewaysOperations(
            self._client, self._config, self._serialize, self._deserialize)
        self.express_route_connections = ExpressRouteConnectionsOperations(
            self._client, self._config, self._serialize, self._deserialize)
        self.express_route_ports_locations = ExpressRoutePortsLocationsOperations(
            self._client, self._config, self._serialize, self._deserialize)
        self.express_route_ports = ExpressRoutePortsOperations(
            self._client, self._config, self._serialize, self._deserialize)
        self.express_route_links = ExpressRouteLinksOperations(
            self._client, self._config, self._serialize, self._deserialize)
        self.interface_endpoints = InterfaceEndpointsOperations(
            self._client, self._config, self._serialize, self._deserialize)
        self.load_balancers = LoadBalancersOperations(
            self._client, self._config, self._serialize, self._deserialize)
        self.load_balancer_backend_address_pools = LoadBalancerBackendAddressPoolsOperations(
            self._client, self._config, self._serialize, self._deserialize)
        self.load_balancer_frontend_ip_configurations = LoadBalancerFrontendIPConfigurationsOperations(
            self._client, self._config, self._serialize, self._deserialize)
        self.inbound_nat_rules = InboundNatRulesOperations(
            self._client, self._config, self._serialize, self._deserialize)
        self.load_balancer_load_balancing_rules = LoadBalancerLoadBalancingRulesOperations(
            self._client, self._config, self._serialize, self._deserialize)
        self.load_balancer_outbound_rules = LoadBalancerOutboundRulesOperations(
            self._client, self._config, self._serialize, self._deserialize)
        self.load_balancer_network_interfaces = LoadBalancerNetworkInterfacesOperations(
            self._client, self._config, self._serialize, self._deserialize)
        self.load_balancer_probes = LoadBalancerProbesOperations(
            self._client, self._config, self._serialize, self._deserialize)
        self.network_interfaces = NetworkInterfacesOperations(
            self._client, self._config, self._serialize, self._deserialize)
        self.network_interface_ip_configurations = NetworkInterfaceIPConfigurationsOperations(
            self._client, self._config, self._serialize, self._deserialize)
        self.network_interface_load_balancers = NetworkInterfaceLoadBalancersOperations(
            self._client, self._config, self._serialize, self._deserialize)
        self.network_interface_tap_configurations = NetworkInterfaceTapConfigurationsOperations(
            self._client, self._config, self._serialize, self._deserialize)
        self.network_profiles = NetworkProfilesOperations(
            self._client, self._config, self._serialize, self._deserialize)
        self.network_security_groups = NetworkSecurityGroupsOperations(
            self._client, self._config, self._serialize, self._deserialize)
        self.security_rules = SecurityRulesOperations(
            self._client, self._config, self._serialize, self._deserialize)
        self.default_security_rules = DefaultSecurityRulesOperations(
            self._client, self._config, self._serialize, self._deserialize)
        self.network_watchers = NetworkWatchersOperations(
            self._client, self._config, self._serialize, self._deserialize)
        self.packet_captures = PacketCapturesOperations(
            self._client, self._config, self._serialize, self._deserialize)
        self.connection_monitors = ConnectionMonitorsOperations(
            self._client, self._config, self._serialize, self._deserialize)
        self.operations = Operations(
            self._client, self._config, self._serialize, self._deserialize)
        self.public_ip_addresses = PublicIPAddressesOperations(
            self._client, self._config, self._serialize, self._deserialize)
        self.public_ip_prefixes = PublicIPPrefixesOperations(
            self._client, self._config, self._serialize, self._deserialize)
        self.route_filters = RouteFiltersOperations(
            self._client, self._config, self._serialize, self._deserialize)
        self.route_filter_rules = RouteFilterRulesOperations(
            self._client, self._config, self._serialize, self._deserialize)
        self.route_tables = RouteTablesOperations(
            self._client, self._config, self._serialize, self._deserialize)
        self.routes = RoutesOperations(
            self._client, self._config, self._serialize, self._deserialize)
        self.bgp_service_communities = BgpServiceCommunitiesOperations(
            self._client, self._config, self._serialize, self._deserialize)
        self.service_endpoint_policies = ServiceEndpointPoliciesOperations(
            self._client, self._config, self._serialize, self._deserialize)
        self.service_endpoint_policy_definitions = ServiceEndpointPolicyDefinitionsOperations(
            self._client, self._config, self._serialize, self._deserialize)
        self.usages = UsagesOperations(
            self._client, self._config, self._serialize, self._deserialize)
        self.virtual_networks = VirtualNetworksOperations(
            self._client, self._config, self._serialize, self._deserialize)
        self.subnets = SubnetsOperations(
            self._client, self._config, self._serialize, self._deserialize)
        self.virtual_network_peerings = VirtualNetworkPeeringsOperations(
            self._client, self._config, self._serialize, self._deserialize)
        self.virtual_network_gateways = VirtualNetworkGatewaysOperations(
            self._client, self._config, self._serialize, self._deserialize)
        self.virtual_network_gateway_connections = VirtualNetworkGatewayConnectionsOperations(
            self._client, self._config, self._serialize, self._deserialize)
        self.local_network_gateways = LocalNetworkGatewaysOperations(
            self._client, self._config, self._serialize, self._deserialize)
        self.virtual_network_taps = VirtualNetworkTapsOperations(
            self._client, self._config, self._serialize, self._deserialize)
        self.virtual_wans = VirtualWansOperations(
            self._client, self._config, self._serialize, self._deserialize)
        self.vpn_sites = VpnSitesOperations(
            self._client, self._config, self._serialize, self._deserialize)
        self.vpn_sites_configuration = VpnSitesConfigurationOperations(
            self._client, self._config, self._serialize, self._deserialize)
        self.virtual_hubs = VirtualHubsOperations(
            self._client, self._config, self._serialize, self._deserialize)
        self.hub_virtual_network_connections = HubVirtualNetworkConnectionsOperations(
            self._client, self._config, self._serialize, self._deserialize)
        self.vpn_gateways = VpnGatewaysOperations(
            self._client, self._config, self._serialize, self._deserialize)
        self.vpn_connections = VpnConnectionsOperations(
            self._client, self._config, self._serialize, self._deserialize)
        self.p2_svpn_server_configurations = P2SVpnServerConfigurationsOperations(
            self._client, self._config, self._serialize, self._deserialize)
        self.p2_svpn_gateways = P2SVpnGatewaysOperations(
            self._client, self._config, self._serialize, self._deserialize)

    async def close(self) -> None:
        await self._client.close()

    async def __aenter__(self) -> "NetworkManagementClient":
        await self._client.__aenter__()
        return self

    async def __aexit__(self, *exc_details) -> None:
        await self._client.__aexit__(*exc_details)
