"""Graph/orchestration engineering package.

Owner: Adeel.

Owns the LangGraph StateGraph wiring, the shared state object, and the two
checkpointers (in-memory for the approval gate, SQLite for the Verification
Agent's cross-session resume). See docs/ARCHITECTURE.md "Graph &
orchestration engineering".
"""
