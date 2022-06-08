#ifndef SYSTEM_PLUGIN_API_SYSTEM_STORE_H
#define SYSTEM_PLUGIN_API_SYSTEM_STORE_H

#include "plugin/context.h"

int system_store_location(system_ctx_t *ctx, const char *location);
int system_store_hostname(system_ctx_t *ctx, const char *hostname);
int system_store_contact(system_ctx_t *ctx, const char *contact);

#endif // SYSTEM_PLUGIN_API_SYSTEM_STORE_H