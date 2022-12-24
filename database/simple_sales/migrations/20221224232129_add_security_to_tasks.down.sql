BEGIN;

DROP POLICY IF EXISTS admin_tasks_policy ON tasks;

DROP POLICY IF EXISTS manager_delete_tasks_policy ON tasks;
DROP POLICY IF EXISTS manager_insert_tasks_policy ON tasks;
DROP POLICY IF EXISTS manager_update_tasks_policy ON tasks;
DROP POLICY IF EXISTS manager_select_tasks_policy ON tasks;

DROP POLICY IF EXISTS employee_update_tasks_policy ON tasks;
DROP POLICY IF EXISTS employee_select_tasks_policy ON tasks;


ALTER TABLE tasks
DISABLE ROW LEVEL SECURITY,
NO FORCE ROW LEVEL SECURITY;

COMMIT;
