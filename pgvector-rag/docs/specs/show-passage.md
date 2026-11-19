# Spec: Show the source passage

## Problem
A cited answer says "[1] refund_policy.md". The user wants to read the exact passage to verify it.

## Behaviour
- show_passage(user, chunk_id) returns {id, source, chunk_no, content, updated_at}.
- Chunk not visible to this user (other tenant, role not allowed) returns None.
- Chunk does not exist returns None. Same result, so the existence of restricted chunks is not leaked.

## Not in scope
Highlighting inside the passage, showing neighbouring chunks, UI.

## Acceptance
1. Allowed user gets the passage.
2. Low-privilege user gets None for a restricted chunk.
3. Other tenant gets None.
4. Unknown id gets None.
