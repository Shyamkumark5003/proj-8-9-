import pytest
from app.access import get_user
from app.search import search

SALARY_VEC = [0.1, 0.9, 0.1]  # salary chunk ku perfect match


def test_viewer_never_gets_restricted_chunks():
    rows = search(get_user("viewer_acme"), SALARY_VEC)
    assert len(rows) > 0
    for _id, content, source, allowed_roles, dist in rows:
        assert "viewer" in allowed_roles, f"Leak: {content}"
    assert all("Salary" not in r[1] for r in rows)


def test_admin_sees_salary_first():
    rows = search(get_user("admin_acme"), SALARY_VEC)
    assert "Salary" in rows[0][1]


def test_manager_sees_manager_not_admin_only():
    contents = [r[1] for r in search(get_user("manager_acme"), SALARY_VEC)]
    assert any("Manager performance" in c for c in contents)
    assert not any("Salary" in c for c in contents)


def test_other_tenant_isolated():
    rows = search(get_user("viewer_beta"), SALARY_VEC)
    contents = [r[1] for r in rows]
    assert contents == ["Beta company refund policy"]


def test_no_context_means_no_rows():
    # tenant/roles set pannama direct query -> fail closed
    from app.db import get_app_conn
    with get_app_conn() as conn:
        rows = conn.execute("SELECT id FROM chunks").fetchall()
    assert rows == []


def test_unknown_user_rejected():
    with pytest.raises(PermissionError):
        get_user("hacker")