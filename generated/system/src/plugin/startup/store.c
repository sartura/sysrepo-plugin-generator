#include "store.h"
#include "plugin/common.h"

#include <libyang/libyang.h>
#include <sysrepo.h>
#include <srpc.h>

static int system_startup_store_contact(void *priv, const struct lyd_node *parent_container);
static int system_startup_store_hostname(void *priv, const struct lyd_node *parent_container);
static int system_startup_store_location(void *priv, const struct lyd_node *parent_container);
static int system_startup_store_clock(void *priv, const struct lyd_node *parent_container);
static int system_startup_store_ntp(void *priv, const struct lyd_node *parent_container);
static int system_startup_store_dns_resolver(void *priv, const struct lyd_node *parent_container);
static int system_startup_store_radius(void *priv, const struct lyd_node *parent_container);
static int system_startup_store_authentication(void *priv, const struct lyd_node *parent_container);

int system_startup_store(system_ctx_t *ctx, sr_session_ctx_t *session)
{
	int error = 0;
	sr_data_t *subtree = NULL;

	error = sr_get_subtree(session, "[ENTER_ROOT_CONFIG_PATH]", 0, &subtree);
	if (error) {
		SRPLG_LOG_ERR(PLUGIN_NAME, "sr_get_subtree() error (%d): %s", error, sr_strerror(error));
		goto error_out;
	}

	srpc_startup_store_t store_values[] = {
		{
			"/ietf-system:system/contact",
			system_startup_store_contact,
		},
		{
			"/ietf-system:system/hostname",
			system_startup_store_hostname,
		},
		{
			"/ietf-system:system/location",
			system_startup_store_location,
		},
		{
			"/ietf-system:system/clock",
			system_startup_store_clock,
		},
		{
			"/ietf-system:system/ntp",
			system_startup_store_ntp,
		},
		{
			"/ietf-system:system/dns-resolver",
			system_startup_store_dns_resolver,
		},
		{
			"/ietf-system:system/radius",
			system_startup_store_radius,
		},
		{
			"/ietf-system:system/authentication",
			system_startup_store_authentication,
		},
	};

	for (size_t i = 0; i < ARRAY_SIZE(store_values); i++) {
		const srpc_startup_store_t *store = &store_values[i];

		error = store->cb(ctx, subtree->tree);
		if (error != 0) {
			SRPLG_LOG_ERR(PLUGIN_NAME, "Startup store callback failed for value %s", store->name);
			goto error_out;
		}
	}

	goto out;

error_out:
	error = -1;

out:
	if (subtree) {
		sr_release_data(subtree);
	}

	return error;
}

static int system_startup_store_contact(void *priv, const struct lyd_node *parent_container)
{
	int error = 0;
	return error;
}

static int system_startup_store_hostname(void *priv, const struct lyd_node *parent_container)
{
	int error = 0;
	return error;
}

static int system_startup_store_location(void *priv, const struct lyd_node *parent_container)
{
	int error = 0;
	return error;
}

static int system_startup_store_clock(void *priv, const struct lyd_node *parent_container)
{
	int error = 0;
	return error;
}

static int system_startup_store_ntp(void *priv, const struct lyd_node *parent_container)
{
	int error = 0;
	return error;
}

static int system_startup_store_dns_resolver(void *priv, const struct lyd_node *parent_container)
{
	int error = 0;
	return error;
}

static int system_startup_store_radius(void *priv, const struct lyd_node *parent_container)
{
	int error = 0;
	return error;
}

static int system_startup_store_authentication(void *priv, const struct lyd_node *parent_container)
{
	int error = 0;
	return error;
}

