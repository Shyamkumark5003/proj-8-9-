from app import ask as A
from app.access import UserContext

USER = UserContext("acme", ("viewer",))


def chunk(i, dist, text="x" * 400):
    return {"id": i, "source": "s.md", "chunk_no": i, "content": text, "distance": dist}


def test_idk_when_nothing_close_and_llm_not_called(monkeypatch):
    monkeypatch.setattr(A, "retrieve", lambda u, q, k=5: [chunk(1, 0.9)])

    def boom(*a, **kw):
        raise AssertionError("LLM must not be called")

    monkeypatch.setattr(A, "chat", boom)
    r = A.ask(USER, "anything")
    assert r.text == A.IDK and r.citations == []


def test_budget_limits_chunks():
    picked = A.build_context([chunk(i, 0.1) for i in range(5)], budget=250)
    assert len(picked) == 2   # each chunk ~100 tokens


def test_answer_has_citation(monkeypatch):
    monkeypatch.setattr(A, "retrieve", lambda u, q, k=5: [chunk(7, 0.1, "7 days refund")])
    monkeypatch.setattr(A, "chat", lambda s, u: "Return within 7 days [1].")
    r = A.ask(USER, "q")
    assert r.citations[0]["id"] == 7


def test_answer_without_citation_is_rejected(monkeypatch):
    monkeypatch.setattr(A, "retrieve", lambda u, q, k=5: [chunk(7, 0.1)])
    monkeypatch.setattr(A, "chat", lambda s, u: "Return within 7 days.")
    assert A.ask(USER, "q").text == A.IDK


def test_llm_says_idk_is_passed_through(monkeypatch):
    monkeypatch.setattr(A, "retrieve", lambda u, q, k=5: [chunk(7, 0.1)])
    monkeypatch.setattr(A, "chat", lambda s, u: "I don't know.")
    assert A.ask(USER, "q").text == A.IDK
