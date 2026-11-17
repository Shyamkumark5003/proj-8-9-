INSERT INTO chunks (tenant_id, content, embedding, allowed_roles, source) VALUES
('acme', 'Refund policy: 7 days la return pannalaam', '[0.9, 0.1, 0.1]', '{viewer,manager,admin}', 'refund_policy.pdf'),
('acme', 'Salary bands (confidential)',               '[0.1, 0.9, 0.1]', '{admin}',                  'salary.pdf'),
('acme', 'Manager performance review process',        '[0.2, 0.8, 0.2]', '{manager,admin}',          'hr_manager.pdf'),
('beta', 'Beta company refund policy',                '[0.9, 0.1, 0.1]', '{viewer,admin}',           'beta_refund.pdf');