def set_context(conn, user):
    conn.execute("SELECT set_config('app.tenant_id', %s, true)", (user.tenant_id,))
    conn.execute("SELECT set_config('app.roles', %s, true)", (",".join(user.roles),))
