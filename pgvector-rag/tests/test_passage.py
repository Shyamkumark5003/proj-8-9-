import pytest
from app.access import UserContext
from app.db import get_admin_conn
from app.passage import show_passage

DUMMY = "[" + ",".join(["0.1"] * 768) + "]"
VIEWER = UserContext("t_test", ("viewer",))
OTHER = UserContext("t_other", ("viewer",))


@pytest.fixture(scope="module")
def ids():
    with get_admin_conn() as conn:
        conn.execute("DELETE FROM doc_chunks WHERE tenant_id IN ('t_test','t_other')")

        def ins(tenant, src, roles, text):
            return conn.execute(
                """INSERT INTO doc_chunks (tenant_id, source, chunk_no, content, embedding, allowed_roles)
                   VALUES (%s, %s, 0, %s, %s::vector, %s) RETURNING id""",
                (tenant, src, text, DUMMY, roles),
            ).fetchone()[0]

        found = {
            "open": ins("t_test", "open.md", ["viewer", "admin"], "Open passage"),
            "secret": ins("t_test", "secret.md", ["admin"], "Secret passage"),
        }
    yield found
    with get_admin_conn() as conn:
        conn.execute("DELETE FROM doc_chunks WHERE tenant_id IN ('t_test','t_other')")


def test_allowed_user_gets_passage(ids):
    p = show_passage(VIEWER, ids["open"])
    assert p["content"] == "Open passage"
    assert p["source"] == "open.md" and p["chunk_no"] == 0


def test_low_privilege_gets_none_for_restricted(ids):
    assert show_passage(VIEWER, ids["secret"]) is None


def test_other_tenant_gets_none(ids):
    assert show_passage(OTHER, ids["open"]) is None


def test_unknown_id_gets_none(ids):
    assert show_passage(VIEWER, 999999999) is None
