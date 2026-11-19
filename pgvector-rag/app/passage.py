from app.db import get_app_conn
from app.rls import set_context


def show_passage(user, chunk_id):
    with get_app_conn() as conn:
        set_context(conn, user)
        row = conn.execute(
            "SELECT id, source, chunk_no, content, updated_at FROM doc_chunks WHERE id = %s",
            (chunk_id,),
        ).fetchone()
    if row is None:
        return None
    return {
        "id": row[0],
        "source": row[1],
        "chunk_no": row[2],
        "content": row[3],
        "updated_at": row[4],
    }
