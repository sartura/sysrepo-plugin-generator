#include "ly_tree.h"
#include "common.h"

#include <srpc.h>

int system_ly_tree_create_system_state(const struct ly_ctx *ly_ctx, struct lyd_node **system_state_node)
{
    return srpc_ly_tree_create_container(ly_ctx, NULL, system_state_node, "system-state");
}

int system_ly_tree_create_system_state_clock(const struct ly_ctx *ly_ctx, struct lyd_node *system_state_node, struct lyd_node **clock_node)
{
    return srpc_ly_tree_create_container(ly_ctx, system_state_node, clock_node, "clock");
}

int system_ly_tree_create_system_state_clock_boot_datetime(const struct ly_ctx *ly_ctx, struct lyd_node *clock_node, const char *boot_datetime)
{
    return srpc_ly_tree_create_leaf(ly_ctx, clock_node, NULL, "boot-datetime", boot_datetime);
}

int system_ly_tree_create_system_state_clock_current_datetime(const struct ly_ctx *ly_ctx, struct lyd_node *clock_node, const char *current_datetime)
{
    return srpc_ly_tree_create_leaf(ly_ctx, clock_node, NULL, "current-datetime", current_datetime);
}

int system_ly_tree_create_system_state_platform(const struct ly_ctx *ly_ctx, struct lyd_node *system_state_node, struct lyd_node **platform_node)
{
    return srpc_ly_tree_create_container(ly_ctx, system_state_node, platform_node, "platform");
}

int system_ly_tree_create_system_state_platform_machine(const struct ly_ctx *ly_ctx, struct lyd_node *platform_node, const char *machine)
{
    return srpc_ly_tree_create_leaf(ly_ctx, platform_node, NULL, "machine", machine);
}

int system_ly_tree_create_system_state_platform_os_version(const struct ly_ctx *ly_ctx, struct lyd_node *platform_node, const char *os_version)
{
    return srpc_ly_tree_create_leaf(ly_ctx, platform_node, NULL, "os-version", os_version);
}

int system_ly_tree_create_system_state_platform_os_release(const struct ly_ctx *ly_ctx, struct lyd_node *platform_node, const char *os_release)
{
    return srpc_ly_tree_create_leaf(ly_ctx, platform_node, NULL, "os-release", os_release);
}

int system_ly_tree_create_system_state_platform_os_name(const struct ly_ctx *ly_ctx, struct lyd_node *platform_node, const char *os_name)
{
    return srpc_ly_tree_create_leaf(ly_ctx, platform_node, NULL, "os-name", os_name);
}

int system_ly_tree_create_system(const struct ly_ctx *ly_ctx, struct lyd_node **system_node)
{
    return srpc_ly_tree_create_container(ly_ctx, NULL, system_node, "system");
}

int system_ly_tree_create_system_authentication(const struct ly_ctx *ly_ctx, struct lyd_node *system_node, struct lyd_node **authentication_node)
{
    return srpc_ly_tree_create_container(ly_ctx, system_node, authentication_node, "authentication");
}

int system_ly_tree_create_system_authentication_user(const struct ly_ctx *ly_ctx, struct lyd_node *authentication_node, struct lyd_node **user_node, const char *name)
{
    // TODO: fix this for multiple keys with SRPC library
    return srpc_ly_tree_create_list(ly_ctx, authentication_node, user_node, "user", "name", name);
}

int system_ly_tree_create_system_authentication_user_authorized_key(const struct ly_ctx *ly_ctx, struct lyd_node *user_node, struct lyd_node **authorized_key_node, const char *name)
{
    // TODO: fix this for multiple keys with SRPC library
    return srpc_ly_tree_create_list(ly_ctx, user_node, authorized_key_node, "authorized-key", "name", name);
}

int system_ly_tree_create_system_authentication_user_authorized_key_key_data(const struct ly_ctx *ly_ctx, struct lyd_node *authorized_key_node, const char *key_data)
{
    return srpc_ly_tree_create_leaf(ly_ctx, authorized_key_node, NULL, "key-data", key_data);
}

int system_ly_tree_create_system_authentication_user_authorized_key_algorithm(const struct ly_ctx *ly_ctx, struct lyd_node *authorized_key_node, const char *algorithm)
{
    return srpc_ly_tree_create_leaf(ly_ctx, authorized_key_node, NULL, "algorithm", algorithm);
}

int system_ly_tree_create_system_authentication_user_authorized_key_name(const struct ly_ctx *ly_ctx, struct lyd_node *authorized_key_node, const char *name)
{
    return srpc_ly_tree_create_leaf(ly_ctx, authorized_key_node, NULL, "name", name);
}

int system_ly_tree_create_system_authentication_user_password(const struct ly_ctx *ly_ctx, struct lyd_node *user_node, const char *password)
{
    return srpc_ly_tree_create_leaf(ly_ctx, user_node, NULL, "password", password);
}

int system_ly_tree_create_system_authentication_user_name(const struct ly_ctx *ly_ctx, struct lyd_node *user_node, const char *name)
{
    return srpc_ly_tree_create_leaf(ly_ctx, user_node, NULL, "name", name);
}

int system_ly_tree_create_system_authentication_user_authentication_order(const struct ly_ctx *ly_ctx, struct lyd_node *authentication_node, const char *user_authentication_order)
{
    return srpc_ly_tree_append_leaf_list(ly_ctx, authentication_node, NULL, "user-authentication-order", user_authentication_order);
}

int system_ly_tree_create_system_radius(const struct ly_ctx *ly_ctx, struct lyd_node *system_node, struct lyd_node **radius_node)
{
    return srpc_ly_tree_create_container(ly_ctx, system_node, radius_node, "radius");
}

int system_ly_tree_create_system_radius_options(const struct ly_ctx *ly_ctx, struct lyd_node *radius_node, struct lyd_node **options_node)
{
    return srpc_ly_tree_create_container(ly_ctx, radius_node, options_node, "options");
}

int system_ly_tree_create_system_radius_options_attempts(const struct ly_ctx *ly_ctx, struct lyd_node *options_node, const char *attempts)
{
    return srpc_ly_tree_create_leaf(ly_ctx, options_node, NULL, "attempts", attempts);
}

int system_ly_tree_create_system_radius_options_timeout(const struct ly_ctx *ly_ctx, struct lyd_node *options_node, const char *timeout)
{
    return srpc_ly_tree_create_leaf(ly_ctx, options_node, NULL, "timeout", timeout);
}

int system_ly_tree_create_system_radius_server(const struct ly_ctx *ly_ctx, struct lyd_node *radius_node, struct lyd_node **server_node, const char *name)
{
    // TODO: fix this for multiple keys with SRPC library
    return srpc_ly_tree_create_list(ly_ctx, radius_node, server_node, "server", "name", name);
}

int system_ly_tree_create_system_radius_server_authentication_type(const struct ly_ctx *ly_ctx, struct lyd_node *server_node, const char *authentication_type)
{
    return srpc_ly_tree_create_leaf(ly_ctx, server_node, NULL, "authentication-type", authentication_type);
}

int system_ly_tree_create_system_radius_server_udp(const struct ly_ctx *ly_ctx, struct lyd_node *server_node, struct lyd_node **udp_node)
{
    return srpc_ly_tree_create_container(ly_ctx, server_node, udp_node, "udp");
}

int system_ly_tree_create_system_radius_server_udp_shared_secret(const struct ly_ctx *ly_ctx, struct lyd_node *udp_node, const char *shared_secret)
{
    return srpc_ly_tree_create_leaf(ly_ctx, udp_node, NULL, "shared-secret", shared_secret);
}

int system_ly_tree_create_system_radius_server_udp_authentication_port(const struct ly_ctx *ly_ctx, struct lyd_node *udp_node, const char *authentication_port)
{
    return srpc_ly_tree_create_leaf(ly_ctx, udp_node, NULL, "authentication-port", authentication_port);
}

int system_ly_tree_create_system_radius_server_udp_address(const struct ly_ctx *ly_ctx, struct lyd_node *udp_node, const char *address)
{
    return srpc_ly_tree_create_leaf(ly_ctx, udp_node, NULL, "address", address);
}

int system_ly_tree_create_system_radius_server_name(const struct ly_ctx *ly_ctx, struct lyd_node *server_node, const char *name)
{
    return srpc_ly_tree_create_leaf(ly_ctx, server_node, NULL, "name", name);
}

int system_ly_tree_create_system_dns_resolver(const struct ly_ctx *ly_ctx, struct lyd_node *system_node, struct lyd_node **dns_resolver_node)
{
    return srpc_ly_tree_create_container(ly_ctx, system_node, dns_resolver_node, "dns-resolver");
}

int system_ly_tree_create_system_dns_resolver_options(const struct ly_ctx *ly_ctx, struct lyd_node *dns_resolver_node, struct lyd_node **options_node)
{
    return srpc_ly_tree_create_container(ly_ctx, dns_resolver_node, options_node, "options");
}

int system_ly_tree_create_system_dns_resolver_options_attempts(const struct ly_ctx *ly_ctx, struct lyd_node *options_node, const char *attempts)
{
    return srpc_ly_tree_create_leaf(ly_ctx, options_node, NULL, "attempts", attempts);
}

int system_ly_tree_create_system_dns_resolver_options_timeout(const struct ly_ctx *ly_ctx, struct lyd_node *options_node, const char *timeout)
{
    return srpc_ly_tree_create_leaf(ly_ctx, options_node, NULL, "timeout", timeout);
}

int system_ly_tree_create_system_dns_resolver_server(const struct ly_ctx *ly_ctx, struct lyd_node *dns_resolver_node, struct lyd_node **server_node, const char *name)
{
    // TODO: fix this for multiple keys with SRPC library
    return srpc_ly_tree_create_list(ly_ctx, dns_resolver_node, server_node, "server", "name", name);
}

int system_ly_tree_create_system_dns_resolver_server_udp_and_tcp(const struct ly_ctx *ly_ctx, struct lyd_node *server_node, struct lyd_node **udp_and_tcp_node)
{
    return srpc_ly_tree_create_container(ly_ctx, server_node, udp_and_tcp_node, "udp-and-tcp");
}

int system_ly_tree_create_system_dns_resolver_server_udp_and_tcp_port(const struct ly_ctx *ly_ctx, struct lyd_node *udp_and_tcp_node, const char *port)
{
    return srpc_ly_tree_create_leaf(ly_ctx, udp_and_tcp_node, NULL, "port", port);
}

int system_ly_tree_create_system_dns_resolver_server_udp_and_tcp_address(const struct ly_ctx *ly_ctx, struct lyd_node *udp_and_tcp_node, const char *address)
{
    return srpc_ly_tree_create_leaf(ly_ctx, udp_and_tcp_node, NULL, "address", address);
}

int system_ly_tree_create_system_dns_resolver_server_name(const struct ly_ctx *ly_ctx, struct lyd_node *server_node, const char *name)
{
    return srpc_ly_tree_create_leaf(ly_ctx, server_node, NULL, "name", name);
}

int system_ly_tree_create_system_dns_resolver_search(const struct ly_ctx *ly_ctx, struct lyd_node *dns_resolver_node, const char *search)
{
    return srpc_ly_tree_append_leaf_list(ly_ctx, dns_resolver_node, NULL, "search", search);
}

int system_ly_tree_create_system_ntp(const struct ly_ctx *ly_ctx, struct lyd_node *system_node, struct lyd_node **ntp_node)
{
    return srpc_ly_tree_create_container(ly_ctx, system_node, ntp_node, "ntp");
}

int system_ly_tree_create_system_ntp_server(const struct ly_ctx *ly_ctx, struct lyd_node *ntp_node, struct lyd_node **server_node, const char *name)
{
    // TODO: fix this for multiple keys with SRPC library
    return srpc_ly_tree_create_list(ly_ctx, ntp_node, server_node, "server", "name", name);
}

int system_ly_tree_create_system_ntp_server_prefer(const struct ly_ctx *ly_ctx, struct lyd_node *server_node, const char *prefer)
{
    return srpc_ly_tree_create_leaf(ly_ctx, server_node, NULL, "prefer", prefer);
}

int system_ly_tree_create_system_ntp_server_iburst(const struct ly_ctx *ly_ctx, struct lyd_node *server_node, const char *iburst)
{
    return srpc_ly_tree_create_leaf(ly_ctx, server_node, NULL, "iburst", iburst);
}

int system_ly_tree_create_system_ntp_server_association_type(const struct ly_ctx *ly_ctx, struct lyd_node *server_node, const char *association_type)
{
    return srpc_ly_tree_create_leaf(ly_ctx, server_node, NULL, "association-type", association_type);
}

int system_ly_tree_create_system_ntp_server_udp(const struct ly_ctx *ly_ctx, struct lyd_node *server_node, struct lyd_node **udp_node)
{
    return srpc_ly_tree_create_container(ly_ctx, server_node, udp_node, "udp");
}

int system_ly_tree_create_system_ntp_server_udp_port(const struct ly_ctx *ly_ctx, struct lyd_node *udp_node, const char *port)
{
    return srpc_ly_tree_create_leaf(ly_ctx, udp_node, NULL, "port", port);
}

int system_ly_tree_create_system_ntp_server_udp_address(const struct ly_ctx *ly_ctx, struct lyd_node *udp_node, const char *address)
{
    return srpc_ly_tree_create_leaf(ly_ctx, udp_node, NULL, "address", address);
}

int system_ly_tree_create_system_ntp_server_name(const struct ly_ctx *ly_ctx, struct lyd_node *server_node, const char *name)
{
    return srpc_ly_tree_create_leaf(ly_ctx, server_node, NULL, "name", name);
}

int system_ly_tree_create_system_ntp_enabled(const struct ly_ctx *ly_ctx, struct lyd_node *ntp_node, const char *enabled)
{
    return srpc_ly_tree_create_leaf(ly_ctx, ntp_node, NULL, "enabled", enabled);
}

int system_ly_tree_create_system_clock(const struct ly_ctx *ly_ctx, struct lyd_node *system_node, struct lyd_node **clock_node)
{
    return srpc_ly_tree_create_container(ly_ctx, system_node, clock_node, "clock");
}

int system_ly_tree_create_system_clock_timezone_utc_offset(const struct ly_ctx *ly_ctx, struct lyd_node *clock_node, const char *timezone_utc_offset)
{
    return srpc_ly_tree_create_leaf(ly_ctx, clock_node, NULL, "timezone-utc-offset", timezone_utc_offset);
}

int system_ly_tree_create_system_clock_timezone_name(const struct ly_ctx *ly_ctx, struct lyd_node *clock_node, const char *timezone_name)
{
    return srpc_ly_tree_create_leaf(ly_ctx, clock_node, NULL, "timezone-name", timezone_name);
}

int system_ly_tree_create_system_location(const struct ly_ctx *ly_ctx, struct lyd_node *system_node, const char *location)
{
    return srpc_ly_tree_create_leaf(ly_ctx, system_node, NULL, "location", location);
}

int system_ly_tree_create_system_hostname(const struct ly_ctx *ly_ctx, struct lyd_node *system_node, const char *hostname)
{
    return srpc_ly_tree_create_leaf(ly_ctx, system_node, NULL, "hostname", hostname);
}

int system_ly_tree_create_system_contact(const struct ly_ctx *ly_ctx, struct lyd_node *system_node, const char *contact)
{
    return srpc_ly_tree_create_leaf(ly_ctx, system_node, NULL, "contact", contact);
}
