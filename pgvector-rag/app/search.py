from app.db import get_app_conn
from app.access import UserContext


def search(user: UserContext, query_vec: list, limit: int = 5):
    vec = "[" + ",".join(str(x) for x in query_vec) + "]"
    with get_app_conn() as conn:
        # true = indha transaction ku mattum
        conn.execute("SELECT set_config('app.tenant_id', %s, true)", (user.tenant_id,))
        conn.execute("SELECT set_config('app.roles', %s, true)", (",".join(user.roles),))
        rows = conn.execute(
            """
            SELECT id, content, source, allowed_roles,
                   embedding <=> %s::vector AS distance
            FROM chunks
            ORDER BY distance
            LIMIT %s
            """,
            (vec, limit),
        ).fetchall()
    return rows