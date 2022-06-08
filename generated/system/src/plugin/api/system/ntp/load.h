#ifndef SYSTEM_PLUGIN_API_SYSTEM_NTP_LOAD_H
#define SYSTEM_PLUGIN_API_SYSTEM_NTP_LOAD_H

#include "plugin/context.h"

int system_ntp_load_server(system_ctx_t *ctx, UT_array **server);
int system_ntp_load_enabled(system_ctx_t *ctx, uint8_t *enabled);

#endif // SYSTEM_PLUGIN_API_SYSTEM_NTP_LOAD_H