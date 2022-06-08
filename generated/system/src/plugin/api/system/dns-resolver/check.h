#ifndef SYSTEM_PLUGIN_API_SYSTEM_DNS_RESOLVER_CHECK_H
#define SYSTEM_PLUGIN_API_SYSTEM_DNS_RESOLVER_CHECK_H

#include "plugin/context.h"

int system_dns_resolver_check_server(system_ctx_t *ctx, const UT_array *server);
int system_dns_resolver_check_search(system_ctx_t *ctx, const UT_array *search);

#endif // SYSTEM_PLUGIN_API_SYSTEM_DNS_RESOLVER_CHECK_H