BEGIN;

CREATE FUNCTION create_database_user(
    database_username name,
    database_password text,
    employee_type_name text,
    first_name text,
    middle_name text,
    last_name text,
    city_name text,
    city_region text DEFAULT NULL
) RETURNS SETOF database_users AS $$
DECLARE
    employee_type_id uuid;
    city_id uuid;
    employee_id uuid;
BEGIN
    SELECT id INTO STRICT employee_type_id FROM employee_types WHERE name = employee_type_name;

    IF city_region IS NULL THEN
        SELECT id INTO STRICT city_id FROM cities WHERE name = city_name;
    ELSE
        SELECT id INTO STRICT city_id FROM cities WHERE name = city_name AND region = city_region;
    END IF;

    INSERT INTO employees (employee_type_id, first_name, middle_name, last_name, city_id)
    VALUES (employee_type_id, first_name, middle_name, last_name, city_id)
    RETURNING id INTO STRICT employee_id;

    EXECUTE format('CREATE ROLE %I WITH INHERIT LOGIN PASSWORD %L', database_username, database_password);

    IF employee_type_name = 'manager' THEN
        EXECUTE format('GRANT simple_sales_manager TO %I', database_username);
    ELSIF employee_type_name = 'salesperson' THEN
        EXECUTE format('GRANT simple_sales_salesperson TO %I', database_username);
    ELSE
        RAISE EXCEPTION 'Unknown employee type: %', employee_type_name;
    END IF;

    INSERT INTO database_users (role_name, employee_id)
    VALUES (database_username, employee_id);

    RETURN QUERY SELECT * FROM database_users WHERE role_name = database_username;
END;
$$ LANGUAGE plpgsql;

CREATE FUNCTION create_database_user_from_employee(
    database_username name,
    database_password text,
    employee_id uuid
) RETURNS SETOF database_users AS $$
DECLARE
    employee_type_name text;
BEGIN
    EXECUTE format('CREATE ROLE %I WITH INHERIT LOGIN PASSWORD %L', database_username, database_password);

    SELECT employee_types.name INTO STRICT employee_type_name
    FROM employees
    JOIN employee_types ON employee_types.id = employees.employee_type_id
    WHERE employees.id = database_user.employee_id;

    IF employee_type_name = 'manager' THEN
        EXECUTE format('GRANT simple_sales_manager TO %I', database_username);
    ELSIF employee_type_name = 'salesperson' THEN
        EXECUTE format('GRANT simple_sales_salesperson TO %I', database_username);
    ELSE
        RAISE EXCEPTION 'Unknown employee type: %', employee_type_name;
    END IF;

    INSERT INTO database_users (role_name, employee_id)
    VALUES (database_username, employee_id);

    RETURN QUERY SELECT * FROM database_users WHERE role_name = database_username;
END;
$$ LANGUAGE plpgsql;

CREATE FUNCTION drop_database_user(
    database_username name
) RETURNS SETOF database_users AS $$
DECLARE
    database_user database_users;
    employee_type_name text;
BEGIN
    DELETE FROM database_users WHERE role_name = database_username RETURNING * INTO STRICT database_user;

    SELECT employee_types.name INTO STRICT employee_type_name
    FROM employees
    JOIN employee_types ON employee_types.id = employees.employee_type_id
    WHERE employees.id = database_user.employee_id;

    IF employee_type_name = 'manager' THEN
        EXECUTE format('REVOKE simple_sales_manager FROM %I', database_username);
    ELSIF employee_type_name = 'salesperson' THEN
        EXECUTE format('REVOKE simple_sales_salesperson FROM %I', database_username);
    ELSE
        RAISE EXCEPTION 'Unknown employee type: %', employee_type_name;
    END IF;

    EXECUTE format('DROP ROLE %I', database_username);

    DELETE FROM employees WHERE id = database_user.employee_id;

    RETURN NEXT database_user;
END;
$$ LANGUAGE plpgsql;

COMMIT;
