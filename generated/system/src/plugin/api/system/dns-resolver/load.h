#ifndef SYSTEM_PLUGIN_API_SYSTEM_DNS_RESOLVER_LOAD_H
#define SYSTEM_PLUGIN_API_SYSTEM_DNS_RESOLVER_LOAD_H

#include "plugin/context.h"

int system_dns_resolver_load_server(system_ctx_t *ctx, UT_array **server);
int system_dns_resolver_load_search(system_ctx_t *ctx, UT_array **search);

#endif // SYSTEM_PLUGIN_API_SYSTEM_DNS_RESOLVER_LOAD_H