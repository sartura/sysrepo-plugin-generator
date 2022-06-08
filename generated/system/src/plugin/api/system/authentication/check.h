#ifndef SYSTEM_PLUGIN_API_SYSTEM_AUTHENTICATION_CHECK_H
#define SYSTEM_PLUGIN_API_SYSTEM_AUTHENTICATION_CHECK_H

#include "plugin/context.h"

int system_authentication_check_user(system_ctx_t *ctx, const UT_array *user);
int system_authentication_check_user_authentication_order(system_ctx_t *ctx, const UT_array *user_authentication_order);

#endif // SYSTEM_PLUGIN_API_SYSTEM_AUTHENTICATION_CHECK_H