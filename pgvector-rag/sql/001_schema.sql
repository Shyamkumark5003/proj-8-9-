CREATE EXTENSION IF NOT EXISTS vector;

CREATE TABLE chunks (
    id          BIGSERIAL PRIMARY KEY,
    tenant_id   TEXT        NOT NULL,
    content     TEXT        NOT NULL,
    embedding   vector(3)   NOT NULL,
    allowed_roles TEXT[]    NOT NULL,
    source      TEXT        NOT NULL,
    updated_at  TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE INDEX idx_chunks_tenant ON chunks (tenant_id);
CREATE INDEX idx_chunks_roles  ON chunks USING GIN (allowed_roles);