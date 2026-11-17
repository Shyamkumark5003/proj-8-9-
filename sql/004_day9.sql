CREATE TABLE doc_chunks (
    id            BIGSERIAL PRIMARY KEY,
    tenant_id     TEXT        NOT NULL,
    source        TEXT        NOT NULL,
    chunk_no      INT         NOT NULL,
    content       TEXT        NOT NULL,
    embedding     vector(768) NOT NULL,
    allowed_roles TEXT[]      NOT NULL,
    updated_at    TIMESTAMPTZ NOT NULL DEFAULT now(),
    UNIQUE (tenant_id, source, chunk_no)
);

GRANT SELECT ON doc_chunks TO app_user;
ALTER TABLE doc_chunks ENABLE ROW LEVEL SECURITY;
ALTER TABLE doc_chunks FORCE ROW LEVEL SECURITY;

CREATE POLICY doc_chunks_read ON doc_chunks FOR SELECT TO app_user
USING (
    tenant_id = current_setting('app.tenant_id', true)
    AND allowed_roles && string_to_array(current_setting('app.roles', true), ',')
);