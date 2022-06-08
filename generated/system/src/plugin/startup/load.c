#include "load.h"
#include "plugin/common.h"

#include <libyang/libyang.h>
#include <sysrepo.h>
#include <srpc.h>

static int system_startup_load_contact(void *priv, sr_session_ctx_t *session, const struct ly_ctx *ly_ctx, struct lyd_node *parent_node);
static int system_startup_load_hostname(void *priv, sr_session_ctx_t *session, const struct ly_ctx *ly_ctx, struct lyd_node *parent_node);
static int system_startup_load_location(void *priv, sr_session_ctx_t *session, const struct ly_ctx *ly_ctx, struct lyd_node *parent_node);
static int system_startup_load_clock(void *priv, sr_session_ctx_t *session, const struct ly_ctx *ly_ctx, struct lyd_node *parent_node);
static int system_startup_load_ntp(void *priv, sr_session_ctx_t *session, const struct ly_ctx *ly_ctx, struct lyd_node *parent_node);
static int system_startup_load_dns_resolver(void *priv, sr_session_ctx_t *session, const struct ly_ctx *ly_ctx, struct lyd_node *parent_node);
static int system_startup_load_radius(void *priv, sr_session_ctx_t *session, const struct ly_ctx *ly_ctx, struct lyd_node *parent_node);
static int system_startup_load_authentication(void *priv, sr_session_ctx_t *session, const struct ly_ctx *ly_ctx, struct lyd_node *parent_node);

int system_startup_load(system_ctx_t *ctx, sr_session_ctx_t *session)
{
    int error = 0;

    const struct ly_ctx *ly_ctx = NULL;
    struct lyd_node *root_node = NULL;
    sr_conn_ctx_t *conn_ctx = NULL;

    srpc_startup_load_t load_values[] = {
        {
            "/ietf-system:system/contact",
            system_startup_load_contact,
        },
        {
            "/ietf-system:system/hostname",
            system_startup_load_hostname,
        },
        {
            "/ietf-system:system/location",
            system_startup_load_location,
        },
        {
            "/ietf-system:system/clock",
            system_startup_load_clock,
        },
        {
            "/ietf-system:system/ntp",
            system_startup_load_ntp,
        },
        {
            "/ietf-system:system/dns-resolver",
            system_startup_load_dns_resolver,
        },
        {
            "/ietf-system:system/radius",
            system_startup_load_radius,
        },
        {
            "/ietf-system:system/authentication",
            system_startup_load_authentication,
        },
    };

    conn_ctx = sr_session_get_connection(session);
    ly_ctx = sr_acquire_context(conn_ctx);
    if (ly_ctx == NULL) {
        SRPLG_LOG_ERR(PLUGIN_NAME, "Unable to get ly_ctx variable");
        goto error_out;
    }

    // load system container info
    // [LOAD ROOT NODE HERE]
    for (size_t i = 0; i < ARRAY_SIZE(load_values); i++) {
        const srpc_startup_load_t *load = &load_values[i];

        error = load->cb((void *) ctx, session, ly_ctx, root_node);
        if (error) {
            SRPLG_LOG_ERR(PLUGIN_NAME, "Node creation callback failed for value %s", load->name);
            goto error_out;
        }
    }

    error = sr_edit_batch(session, root_node, "merge");
    if (error != SR_ERR_OK) {
        SRPLG_LOG_ERR(PLUGIN_NAME, "sr_edit_batch() error (%d): %s", error, sr_strerror(error));
        goto error_out;
    }

    error = sr_apply_changes(session, 0);
    if (error != 0) {
        SRPLG_LOG_ERR(PLUGIN_NAME, "sr_apply_changes() error (%d): %s", error, sr_strerror(error));
        goto error_out;
    }

    goto out;

error_out:
    error = -1;

out:
    if (root_node) {
        lyd_free_tree(root_node);
    }
    sr_release_context(conn_ctx);
    return error;
}

static int system_startup_load_contact(void *priv, sr_session_ctx_t *session, const struct ly_ctx *ly_ctx, struct lyd_node *parent_node)
{
    int error = 0;
    return error;
}

static int system_startup_load_hostname(void *priv, sr_session_ctx_t *session, const struct ly_ctx *ly_ctx, struct lyd_node *parent_node)
{
    int error = 0;
    return error;
}

static int system_startup_load_location(void *priv, sr_session_ctx_t *session, const struct ly_ctx *ly_ctx, struct lyd_node *parent_node)
{
    int error = 0;
    return error;
}

static int system_startup_load_clock(void *priv, sr_session_ctx_t *session, const struct ly_ctx *ly_ctx, struct lyd_node *parent_node)
{
    int error = 0;
    return error;
}

static int system_startup_load_ntp(void *priv, sr_session_ctx_t *session, const struct ly_ctx *ly_ctx, struct lyd_node *parent_node)
{
    int error = 0;
    return error;
}

static int system_startup_load_dns_resolver(void *priv, sr_session_ctx_t *session, const struct ly_ctx *ly_ctx, struct lyd_node *parent_node)
{
    int error = 0;
    return error;
}

static int system_startup_load_radius(void *priv, sr_session_ctx_t *session, const struct ly_ctx *ly_ctx, struct lyd_node *parent_node)
{
    int error = 0;
    return error;
}

static int system_startup_load_authentication(void *priv, sr_session_ctx_t *session, const struct ly_ctx *ly_ctx, struct lyd_node *parent_node)
{
    int error = 0;
    return error;
}

