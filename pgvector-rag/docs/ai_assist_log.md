# AI-assist log (Day 9)

| # | Task | What I asked the AI | What it gave | What I changed / rejected | How I verified |
|---|------|---------------------|--------------|---------------------------|----------------|
| 1 | ask() | Build ask() with budget, citations, "I don't know" | ask.py | EXAMPLE: timeout was 60s, qwen3.5:2b timed out, set 300 and turned off thinking | ran 3 sample questions; tests/test_ask.py |
| 2 | Golden set + recall | 15 questions and recall@k script | golden.json, recall.py | EXAMPLE: checked each expected chunk by reading the docs myself | python -m eval.recall (15/15) |
| 3 | Show passage | Spec, plan, tasks, tests, function | passage.py, test_passage.py | EXAMPLE: confirmed the tests failed first, then passed | pytest red then green |

## What I do NOT trust blindly
- (write 2 or 3 lines: e.g. recall 1.00 is on easy questions only; MAX_DISTANCE needs tuning on harder data)
