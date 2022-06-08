#ifndef SYSTEM_PLUGIN_LY_TREE_H
#define SYSTEM_PLUGIN_LY_TREE_H

#include <libyang/libyang.h>

int system_ly_tree_create_system_state(const struct ly_ctx *ly_ctx, struct lyd_node **system_state_node);
int system_ly_tree_create_system_state_clock(const struct ly_ctx *ly_ctx, struct lyd_node *system_state_node, struct lyd_node **clock_node);
int system_ly_tree_create_system_state_clock_boot_datetime(const struct ly_ctx *ly_ctx, struct lyd_node *clock_node, const char *boot_datetime);
int system_ly_tree_create_system_state_clock_current_datetime(const struct ly_ctx *ly_ctx, struct lyd_node *clock_node, const char *current_datetime);
int system_ly_tree_create_system_state_platform(const struct ly_ctx *ly_ctx, struct lyd_node *system_state_node, struct lyd_node **platform_node);
int system_ly_tree_create_system_state_platform_machine(const struct ly_ctx *ly_ctx, struct lyd_node *platform_node, const char *machine);
int system_ly_tree_create_system_state_platform_os_version(const struct ly_ctx *ly_ctx, struct lyd_node *platform_node, const char *os_version);
int system_ly_tree_create_system_state_platform_os_release(const struct ly_ctx *ly_ctx, struct lyd_node *platform_node, const char *os_release);
int system_ly_tree_create_system_state_platform_os_name(const struct ly_ctx *ly_ctx, struct lyd_node *platform_node, const char *os_name);
int system_ly_tree_create_system(const struct ly_ctx *ly_ctx, struct lyd_node **system_node);
int system_ly_tree_create_system_authentication(const struct ly_ctx *ly_ctx, struct lyd_node *system_node, struct lyd_node **authentication_node);
int system_ly_tree_create_system_authentication_user(const struct ly_ctx *ly_ctx, struct lyd_node *authentication_node, struct lyd_node **user_node, const char *name);
int system_ly_tree_create_system_authentication_user_authorized_key(const struct ly_ctx *ly_ctx, struct lyd_node *user_node, struct lyd_node **authorized_key_node, const char *name);
int system_ly_tree_create_system_authentication_user_authorized_key_key_data(const struct ly_ctx *ly_ctx, struct lyd_node *authorized_key_node, const char *key_data);
int system_ly_tree_create_system_authentication_user_authorized_key_algorithm(const struct ly_ctx *ly_ctx, struct lyd_node *authorized_key_node, const char *algorithm);
int system_ly_tree_create_system_authentication_user_authorized_key_name(const struct ly_ctx *ly_ctx, struct lyd_node *authorized_key_node, const char *name);
int system_ly_tree_create_system_authentication_user_password(const struct ly_ctx *ly_ctx, struct lyd_node *user_node, const char *password);
int system_ly_tree_create_system_authentication_user_name(const struct ly_ctx *ly_ctx, struct lyd_node *user_node, const char *name);
int system_ly_tree_create_system_authentication_user_authentication_order(const struct ly_ctx *ly_ctx, struct lyd_node *authentication_node, const char *user_authentication_order);
int system_ly_tree_create_system_radius(const struct ly_ctx *ly_ctx, struct lyd_node *system_node, struct lyd_node **radius_node);
int system_ly_tree_create_system_radius_options(const struct ly_ctx *ly_ctx, struct lyd_node *radius_node, struct lyd_node **options_node);
int system_ly_tree_create_system_radius_options_attempts(const struct ly_ctx *ly_ctx, struct lyd_node *options_node, const char *attempts);
int system_ly_tree_create_system_radius_options_timeout(const struct ly_ctx *ly_ctx, struct lyd_node *options_node, const char *timeout);
int system_ly_tree_create_system_radius_server(const struct ly_ctx *ly_ctx, struct lyd_node *radius_node, struct lyd_node **server_node, const char *name);
int system_ly_tree_create_system_radius_server_authentication_type(const struct ly_ctx *ly_ctx, struct lyd_node *server_node, const char *authentication_type);
int system_ly_tree_create_system_radius_server_udp(const struct ly_ctx *ly_ctx, struct lyd_node *server_node, struct lyd_node **udp_node);
int system_ly_tree_create_system_radius_server_udp_shared_secret(const struct ly_ctx *ly_ctx, struct lyd_node *udp_node, const char *shared_secret);
int system_ly_tree_create_system_radius_server_udp_authentication_port(const struct ly_ctx *ly_ctx, struct lyd_node *udp_node, const char *authentication_port);
int system_ly_tree_create_system_radius_server_udp_address(const struct ly_ctx *ly_ctx, struct lyd_node *udp_node, const char *address);
int system_ly_tree_create_system_radius_server_name(const struct ly_ctx *ly_ctx, struct lyd_node *server_node, const char *name);
int system_ly_tree_create_system_dns_resolver(const struct ly_ctx *ly_ctx, struct lyd_node *system_node, struct lyd_node **dns_resolver_node);
int system_ly_tree_create_system_dns_resolver_options(const struct ly_ctx *ly_ctx, struct lyd_node *dns_resolver_node, struct lyd_node **options_node);
int system_ly_tree_create_system_dns_resolver_options_attempts(const struct ly_ctx *ly_ctx, struct lyd_node *options_node, const char *attempts);
int system_ly_tree_create_system_dns_resolver_options_timeout(const struct ly_ctx *ly_ctx, struct lyd_node *options_node, const char *timeout);
int system_ly_tree_create_system_dns_resolver_server(const struct ly_ctx *ly_ctx, struct lyd_node *dns_resolver_node, struct lyd_node **server_node, const char *name);
int system_ly_tree_create_system_dns_resolver_server_udp_and_tcp(const struct ly_ctx *ly_ctx, struct lyd_node *server_node, struct lyd_node **udp_and_tcp_node);
int system_ly_tree_create_system_dns_resolver_server_udp_and_tcp_port(const struct ly_ctx *ly_ctx, struct lyd_node *udp_and_tcp_node, const char *port);
int system_ly_tree_create_system_dns_resolver_server_udp_and_tcp_address(const struct ly_ctx *ly_ctx, struct lyd_node *udp_and_tcp_node, const char *address);
int system_ly_tree_create_system_dns_resolver_server_name(const struct ly_ctx *ly_ctx, struct lyd_node *server_node, const char *name);
int system_ly_tree_create_system_dns_resolver_search(const struct ly_ctx *ly_ctx, struct lyd_node *dns_resolver_node, const char *search);
int system_ly_tree_create_system_ntp(const struct ly_ctx *ly_ctx, struct lyd_node *system_node, struct lyd_node **ntp_node);
int system_ly_tree_create_system_ntp_server(const struct ly_ctx *ly_ctx, struct lyd_node *ntp_node, struct lyd_node **server_node, const char *name);
int system_ly_tree_create_system_ntp_server_prefer(const struct ly_ctx *ly_ctx, struct lyd_node *server_node, const char *prefer);
int system_ly_tree_create_system_ntp_server_iburst(const struct ly_ctx *ly_ctx, struct lyd_node *server_node, const char *iburst);
int system_ly_tree_create_system_ntp_server_association_type(const struct ly_ctx *ly_ctx, struct lyd_node *server_node, const char *association_type);
int system_ly_tree_create_system_ntp_server_udp(const struct ly_ctx *ly_ctx, struct lyd_node *server_node, struct lyd_node **udp_node);
int system_ly_tree_create_system_ntp_server_udp_port(const struct ly_ctx *ly_ctx, struct lyd_node *udp_node, const char *port);
int system_ly_tree_create_system_ntp_server_udp_address(const struct ly_ctx *ly_ctx, struct lyd_node *udp_node, const char *address);
int system_ly_tree_create_system_ntp_server_name(const struct ly_ctx *ly_ctx, struct lyd_node *server_node, const char *name);
int system_ly_tree_create_system_ntp_enabled(const struct ly_ctx *ly_ctx, struct lyd_node *ntp_node, const char *enabled);
int system_ly_tree_create_system_clock(const struct ly_ctx *ly_ctx, struct lyd_node *system_node, struct lyd_node **clock_node);
int system_ly_tree_create_system_clock_timezone_utc_offset(const struct ly_ctx *ly_ctx, struct lyd_node *clock_node, const char *timezone_utc_offset);
int system_ly_tree_create_system_clock_timezone_name(const struct ly_ctx *ly_ctx, struct lyd_node *clock_node, const char *timezone_name);
int system_ly_tree_create_system_location(const struct ly_ctx *ly_ctx, struct lyd_node *system_node, const char *location);
int system_ly_tree_create_system_hostname(const struct ly_ctx *ly_ctx, struct lyd_node *system_node, const char *hostname);
int system_ly_tree_create_system_contact(const struct ly_ctx *ly_ctx, struct lyd_node *system_node, const char *contact);

#endif // SYSTEM_PLUGIN_LY_TREE_H