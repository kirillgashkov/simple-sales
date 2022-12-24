BEGIN;

--
-- Role: "simple_sales_employee" (includes "simple_sales_manager" and "simple_sales_salesperson")
--


CREATE POLICY employee_select_tasks_policy
ON tasks
FOR SELECT
TO simple_sales_employee
USING (assigned_to = (SELECT get_current_employee_id()));

CREATE POLICY employee_update_tasks_policy
ON tasks
FOR UPDATE
TO simple_sales_employee
USING (
    assigned_to = (SELECT get_current_employee_id())
    AND completed_at IS NOT NULL
);


--
-- Role: "simple_sales_manager"
--


CREATE POLICY manager_select_tasks_policy
ON tasks
FOR SELECT
TO simple_sales_manager
USING (
    created_by = (SELECT get_current_employee_id())
    OR assigned_to IN (
        SELECT employees.id
        FROM employees
        JOIN employee_types ON employees.employee_type_id = employee_types.id
        WHERE employee_types.name = 'salesperson'
    )
);

CREATE POLICY manager_update_tasks_policy
ON tasks
FOR UPDATE
TO simple_sales_manager
USING (
    created_by = (SELECT get_current_employee_id())
    AND completed_at IS NOT NULL
)
WITH CHECK (
    created_by = (SELECT get_current_employee_id())
);

CREATE POLICY manager_insert_tasks_policy
ON tasks
FOR INSERT
TO simple_sales_manager
WITH CHECK (
    created_by = (SELECT get_current_employee_id())
);

CREATE POLICY manager_delete_tasks_policy
ON tasks
FOR DELETE
TO simple_sales_manager
USING (
    created_by = (SELECT get_current_employee_id())
    AND completed_at IS NOT NULL
);


--
-- Role: "simple_sales_salesperson"
--


--
-- Role: "simple_sales_admin"
--


CREATE POLICY admin_tasks_policy
ON tasks
FOR SELECT
TO simple_sales_admin;

COMMIT;
