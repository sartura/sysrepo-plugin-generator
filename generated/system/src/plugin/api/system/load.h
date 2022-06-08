#ifndef SYSTEM_PLUGIN_API_SYSTEM_LOAD_H
#define SYSTEM_PLUGIN_API_SYSTEM_LOAD_H

#include "plugin/context.h"

int system_load_location(system_ctx_t *ctx, char **location);
int system_load_hostname(system_ctx_t *ctx, char **hostname);
int system_load_contact(system_ctx_t *ctx, char **contact);

#endif // SYSTEM_PLUGIN_API_SYSTEM_LOAD_H