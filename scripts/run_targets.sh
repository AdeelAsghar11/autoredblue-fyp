#!/usr/bin/env bash
# docker-compose helper for the local vulnerable targets (DVWA, Juice
# Shop, Metasploitable -- see docker-compose.yml and docs/PROJECT.md's
# scope guardrails: these three only, never a live .gov.pk site).
#
# Not implemented yet -- scaffolding only.
set -euo pipefail

echo "TODO: docker compose -f docker-compose.yml up -d, wait for health," \
     "print the URLs from config/allowlist.example.yaml." >&2
exit 1
