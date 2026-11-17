-- 1. Low-privilege app user (RLS ku bound aagum)
CREATE ROLE app_user LOGIN PASSWORD 'app_pass' NOSUPERUSER NOBYPASSRLS;

GRANT USAGE ON SCHEMA public TO app_user;
GRANT SELECT ON chunks TO app_user;

-- 2. RLS on pannu
ALTER TABLE chunks ENABLE ROW LEVEL SECURITY;
ALTER TABLE chunks FORCE ROW LEVEL SECURITY;

-- 3. Policy: tenant match AND role match
CREATE POLICY chunks_read ON chunks
FOR SELECT
TO app_user
USING (
    tenant_id = current_setting('app.tenant_id', true)
    AND allowed_roles && string_to_array(current_setting('app.roles', true), ',')
);