#!/usr/bin/env bash
# Pulls the Ollama model sized to whichever machine this runs on
# (dev: personal PC, 6GB VRAM, 3B-7B; lab: A4000, 16GB VRAM, 7B-14B --
# see docs/ARCHITECTURE.md "Hardware: two machines, two roles" and
# config/settings.example.yaml's vram_tier).
#
# Not implemented yet -- scaffolding only.
set -euo pipefail

echo "TODO: read vram_tier from config/settings.yaml and run" \
     "'ollama pull <model>' for the right tier." >&2
exit 1
