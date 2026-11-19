# Plan
1. Re-use get_app_conn + set_context, so RLS decides visibility (no new Python if-checks).
2. New module app/passage.py with one function show_passage.
3. Return None for both "not allowed" and "not found" (no leak).
