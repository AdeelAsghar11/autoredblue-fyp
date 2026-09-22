"""Thin wrappers around each external security CLI tool.

These wrap tools, they don't reimplement them; the interesting work is
the agentic/AI layer that calls them (see docs/PROJECT.md "Team &
context"). No LLM involvement in this package; plain subprocess/API
plumbing only.
"""
