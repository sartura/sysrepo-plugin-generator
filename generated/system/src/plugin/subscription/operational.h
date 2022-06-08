#ifndef SYSTEM_PLUGIN_SUBSCRIPTION_OPERATIONAL_H
#define SYSTEM_PLUGIN_SUBSCRIPTION_OPERATIONAL_H

#include <sysrepo_types.h>

int system_subscription_operational_system_state_platform_os_name(sr_session_ctx_t *session, uint32_t sub_id, const char *module_name, const char *path, const char *request_xpath, uint32_t request_id, struct lyd_node **parent, void *private_data);
int system_subscription_operational_system_state_platform_os_release(sr_session_ctx_t *session, uint32_t sub_id, const char *module_name, const char *path, const char *request_xpath, uint32_t request_id, struct lyd_node **parent, void *private_data);
int system_subscription_operational_system_state_platform_os_version(sr_session_ctx_t *session, uint32_t sub_id, const char *module_name, const char *path, const char *request_xpath, uint32_t request_id, struct lyd_node **parent, void *private_data);
int system_subscription_operational_system_state_platform_machine(sr_session_ctx_t *session, uint32_t sub_id, const char *module_name, const char *path, const char *request_xpath, uint32_t request_id, struct lyd_node **parent, void *private_data);
int system_subscription_operational_system_state_clock_current_datetime(sr_session_ctx_t *session, uint32_t sub_id, const char *module_name, const char *path, const char *request_xpath, uint32_t request_id, struct lyd_node **parent, void *private_data);
int system_subscription_operational_system_state_clock_boot_datetime(sr_session_ctx_t *session, uint32_t sub_id, const char *module_name, const char *path, const char *request_xpath, uint32_t request_id, struct lyd_node **parent, void *private_data);

#endif // SYSTEM_PLUGIN_SUBSCRIPTION_OPERATIONAL_H