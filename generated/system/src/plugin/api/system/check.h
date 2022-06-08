#ifndef SYSTEM_PLUGIN_API_SYSTEM_CHECK_H
#define SYSTEM_PLUGIN_API_SYSTEM_CHECK_H

#include "plugin/context.h"

int system_check_location(system_ctx_t *ctx, const char *location);
int system_check_hostname(system_ctx_t *ctx, const char *hostname);
int system_check_contact(system_ctx_t *ctx, const char *contact);

#endif // SYSTEM_PLUGIN_API_SYSTEM_CHECK_H