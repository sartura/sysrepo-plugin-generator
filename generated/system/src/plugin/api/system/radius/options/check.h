#ifndef SYSTEM_PLUGIN_API_SYSTEM_RADIUS_OPTIONS_CHECK_H
#define SYSTEM_PLUGIN_API_SYSTEM_RADIUS_OPTIONS_CHECK_H

#include "plugin/context.h"

int system_radius_options_check_attempts(system_ctx_t *ctx, const uint8_t attempts);
int system_radius_options_check_timeout(system_ctx_t *ctx, const uint8_t timeout);

#endif // SYSTEM_PLUGIN_API_SYSTEM_RADIUS_OPTIONS_CHECK_H