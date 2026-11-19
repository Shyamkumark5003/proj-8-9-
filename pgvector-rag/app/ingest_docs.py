from pathlib import Path
from app.db import get_admin_conn
from app.llm import embed

ALL = ["viewer", "manager", "admin"]
ROLES = {"security_policy.md": ["manager", "admin"]}  # idhu viewer ku restricted


def _vec(v):
    return "[" + ",".join(str(x) for x in v) + "]"


def ingest(folder="data/docs", tenant="acme"):
    n = 0
    with get_admin_conn() as conn:
        for f in sorted(Path(folder).glob("*.md")):
            paras = [p.strip() for p in f.read_text(encoding="utf-8").split("\n\n") if p.strip()]
            for i, p in enumerate(paras):
                conn.execute(
                    """
                    INSERT INTO doc_chunks (tenant_id, source, chunk_no, content, embedding, allowed_roles)
                    VALUES (%s, %s, %s, %s, %s::vector, %s)
                    ON CONFLICT (tenant_id, source, chunk_no) DO UPDATE
                    SET content = EXCLUDED.content,
                        embedding = EXCLUDED.embedding,
                        allowed_roles = EXCLUDED.allowed_roles,
                        updated_at = now()
                    """,
                    (tenant, f.name, i, p, _vec(embed(p)), ROLES.get(f.name, ALL)),
                )
                n += 1
    return n


if __name__ == "__main__":
    print("ingested", ingest(), "chunks")
    