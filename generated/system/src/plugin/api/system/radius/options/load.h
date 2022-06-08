#ifndef SYSTEM_PLUGIN_API_SYSTEM_RADIUS_OPTIONS_LOAD_H
#define SYSTEM_PLUGIN_API_SYSTEM_RADIUS_OPTIONS_LOAD_H

#include "plugin/context.h"

int system_radius_options_load_attempts(system_ctx_t *ctx, uint8_t *attempts);
int system_radius_options_load_timeout(system_ctx_t *ctx, uint8_t *timeout);

#endif // SYSTEM_PLUGIN_API_SYSTEM_RADIUS_OPTIONS_LOAD_H