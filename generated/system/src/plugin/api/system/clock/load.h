#ifndef SYSTEM_PLUGIN_API_SYSTEM_CLOCK_LOAD_H
#define SYSTEM_PLUGIN_API_SYSTEM_CLOCK_LOAD_H

#include "plugin/context.h"

int system_clock_load_timezone_utc_offset(system_ctx_t *ctx, int16_t *timezone_utc_offset);
int system_clock_load_timezone_name(system_ctx_t *ctx, char **timezone_name);

#endif // SYSTEM_PLUGIN_API_SYSTEM_CLOCK_LOAD_H