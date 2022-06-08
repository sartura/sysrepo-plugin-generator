#ifndef SYSTEM_PLUGIN_API_SYSTEM_RADIUS_OPTIONS_STORE_H
#define SYSTEM_PLUGIN_API_SYSTEM_RADIUS_OPTIONS_STORE_H

#include "plugin/context.h"

int system_radius_options_store_attempts(system_ctx_t *ctx, const uint8_t attempts);
int system_radius_options_store_timeout(system_ctx_t *ctx, const uint8_t timeout);

#endif // SYSTEM_PLUGIN_API_SYSTEM_RADIUS_OPTIONS_STORE_H