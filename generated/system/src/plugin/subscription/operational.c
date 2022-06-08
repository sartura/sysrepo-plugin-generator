#include "operational.h"
#include "plugin/context.h"
#include "plugin/common.h"

#include <libyang/libyang.h>
#include <sysrepo.h>
#include <srpc.h>

int system_subscription_operational_system_state_platform_os_name(sr_session_ctx_t *session, uint32_t sub_id, const char *module_name, const char *path, const char *request_xpath, uint32_t request_id, struct lyd_node **parent, void *private_data)
{
	int error = SR_ERR_OK;
	const struct ly_ctx *ly_ctx = NULL;

	if (*parent == NULL) {
		ly_ctx = sr_acquire_context(sr_session_get_connection(session));
		if (ly_ctx == NULL) {
			SRPLG_LOG_ERR(PLUGIN_NAME, "sr_acquire_context() failed");
			goto error_out;
		}
	}

	goto out;

error_out:
	error = SR_ERR_CALLBACK_FAILED;

out:
	return error;
}

int system_subscription_operational_system_state_platform_os_release(sr_session_ctx_t *session, uint32_t sub_id, const char *module_name, const char *path, const char *request_xpath, uint32_t request_id, struct lyd_node **parent, void *private_data)
{
	int error = SR_ERR_OK;
	const struct ly_ctx *ly_ctx = NULL;

	if (*parent == NULL) {
		ly_ctx = sr_acquire_context(sr_session_get_connection(session));
		if (ly_ctx == NULL) {
			SRPLG_LOG_ERR(PLUGIN_NAME, "sr_acquire_context() failed");
			goto error_out;
		}
	}

	goto out;

error_out:
	error = SR_ERR_CALLBACK_FAILED;

out:
	return error;
}

int system_subscription_operational_system_state_platform_os_version(sr_session_ctx_t *session, uint32_t sub_id, const char *module_name, const char *path, const char *request_xpath, uint32_t request_id, struct lyd_node **parent, void *private_data)
{
	int error = SR_ERR_OK;
	const struct ly_ctx *ly_ctx = NULL;

	if (*parent == NULL) {
		ly_ctx = sr_acquire_context(sr_session_get_connection(session));
		if (ly_ctx == NULL) {
			SRPLG_LOG_ERR(PLUGIN_NAME, "sr_acquire_context() failed");
			goto error_out;
		}
	}

	goto out;

error_out:
	error = SR_ERR_CALLBACK_FAILED;

out:
	return error;
}

int system_subscription_operational_system_state_platform_machine(sr_session_ctx_t *session, uint32_t sub_id, const char *module_name, const char *path, const char *request_xpath, uint32_t request_id, struct lyd_node **parent, void *private_data)
{
	int error = SR_ERR_OK;
	const struct ly_ctx *ly_ctx = NULL;

	if (*parent == NULL) {
		ly_ctx = sr_acquire_context(sr_session_get_connection(session));
		if (ly_ctx == NULL) {
			SRPLG_LOG_ERR(PLUGIN_NAME, "sr_acquire_context() failed");
			goto error_out;
		}
	}

	goto out;

error_out:
	error = SR_ERR_CALLBACK_FAILED;

out:
	return error;
}

int system_subscription_operational_system_state_clock_current_datetime(sr_session_ctx_t *session, uint32_t sub_id, const char *module_name, const char *path, const char *request_xpath, uint32_t request_id, struct lyd_node **parent, void *private_data)
{
	int error = SR_ERR_OK;
	const struct ly_ctx *ly_ctx = NULL;

	if (*parent == NULL) {
		ly_ctx = sr_acquire_context(sr_session_get_connection(session));
		if (ly_ctx == NULL) {
			SRPLG_LOG_ERR(PLUGIN_NAME, "sr_acquire_context() failed");
			goto error_out;
		}
	}

	goto out;

error_out:
	error = SR_ERR_CALLBACK_FAILED;

out:
	return error;
}

int system_subscription_operational_system_state_clock_boot_datetime(sr_session_ctx_t *session, uint32_t sub_id, const char *module_name, const char *path, const char *request_xpath, uint32_t request_id, struct lyd_node **parent, void *private_data)
{
	int error = SR_ERR_OK;
	const struct ly_ctx *ly_ctx = NULL;

	if (*parent == NULL) {
		ly_ctx = sr_acquire_context(sr_session_get_connection(session));
		if (ly_ctx == NULL) {
			SRPLG_LOG_ERR(PLUGIN_NAME, "sr_acquire_context() failed");
			goto error_out;
		}
	}

	goto out;

error_out:
	error = SR_ERR_CALLBACK_FAILED;

out:
	return error;
}

