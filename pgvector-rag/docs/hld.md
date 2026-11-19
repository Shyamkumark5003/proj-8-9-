# High-level design: Policy Q&A assistant

## Problem (client's words)
"Our staff keep asking HR and support the same policy questions. Answers differ by
person, and some documents must not be seen by everyone."

## Data we use, and why
- 5 policy documents (refunds, leave, expenses, onboarding, security), split by paragraph.
  Why: policies are short, one paragraph holds one rule, so one chunk answers one question.
- Per chunk metadata: tenant, allowed roles, source, chunk number, updated time.
  Why: access control and citations both need it.

## Who uses it
- Staff (viewer): general policies.
- Managers and admins: also restricted policies (security).
- Support team: checks the cited passage.

## Main parts
1. Ingest: split, embed, upsert into Postgres (pgvector).
2. Access: Postgres Row Level Security; app connects as a low-privilege user.
3. Retrieve: similarity search; RLS filters before ranking.
4. ask(): context within a token budget, answer with citations, "I don't know" gate.
5. Evaluate: 15-question golden set, recall@k.
6. Show source passage: read the cited chunk under the same access rules.

## Out of scope
Login/SSO, UI, document upload, multiple languages, answer-quality grading,
large-scale index tuning (HNSW).

## Decisions and reasons
| Decision | Reason |
|---|---|
| Postgres + pgvector, no separate vector DB | One system for data and permissions; RLS is already there |
| RLS in the database, not only in app code | A bug in app code cannot leak restricted chunks |
| Paragraph chunking | Documents are short; one rule per paragraph |
| Distance threshold and "I don't know" | Better to say nothing than to guess |
| Reject answers with no valid citation | Every claim must be checkable |
| Context budget of 600 tokens | Controls cost, keeps the model focused |
| Local model via OpenAI-compatible API | No data leaves the machine; easy to swap |
| show_passage returns None for not-allowed and not-found | Does not reveal that a restricted chunk exists |

## Known limits
recall@k = 1.00 is on 15 easy questions over 15 chunks. Needs harder questions and a bigger corpus.
