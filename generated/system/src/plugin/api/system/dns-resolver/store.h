#ifndef SYSTEM_PLUGIN_API_SYSTEM_DNS_RESOLVER_STORE_H
#define SYSTEM_PLUGIN_API_SYSTEM_DNS_RESOLVER_STORE_H

#include "plugin/context.h"

int system_dns_resolver_store_server(system_ctx_t *ctx, const UT_array *server);
int system_dns_resolver_store_search(system_ctx_t *ctx, const UT_array *search);

#endif // SYSTEM_PLUGIN_API_SYSTEM_DNS_RESOLVER_STORE_H