#ifndef SYSTEM_PLUGIN_API_SYSTEM_NTP_STORE_H
#define SYSTEM_PLUGIN_API_SYSTEM_NTP_STORE_H

#include "plugin/context.h"

int system_ntp_store_server(system_ctx_t *ctx, const UT_array *server);
int system_ntp_store_enabled(system_ctx_t *ctx, const uint8_t enabled);

#endif // SYSTEM_PLUGIN_API_SYSTEM_NTP_STORE_H