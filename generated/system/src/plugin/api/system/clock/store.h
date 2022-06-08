#ifndef SYSTEM_PLUGIN_API_SYSTEM_CLOCK_STORE_H
#define SYSTEM_PLUGIN_API_SYSTEM_CLOCK_STORE_H

#include "plugin/context.h"

int system_clock_store_timezone_utc_offset(system_ctx_t *ctx, const int16_t timezone_utc_offset);
int system_clock_store_timezone_name(system_ctx_t *ctx, const char *timezone_name);

#endif // SYSTEM_PLUGIN_API_SYSTEM_CLOCK_STORE_H