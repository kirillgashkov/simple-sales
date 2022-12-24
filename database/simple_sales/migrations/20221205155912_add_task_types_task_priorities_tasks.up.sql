BEGIN;

CREATE TABLE IF NOT EXISTS task_types (
    id uuid PRIMARY KEY DEFAULT uuid_generate_v4(),
    name text NOT NULL
);


CREATE TABLE IF NOT EXISTS task_priorities (
    id uuid PRIMARY KEY DEFAULT uuid_generate_v4(),
    level smallint NOT NULL,
    name text NOT NULL
);

INSERT INTO task_priorities (id, level, name)
VALUES
    ('6260bf47-9df8-4d42-99f8-eb7feb5a3dd2', 1, 'low'),
    ('897a4f3c-526b-4bd0-9f75-bb79efea9377', 2, 'medium'),
    ('bb82f92d-cb67-4df8-a613-cab6ee7dd392', 3, 'high')
ON CONFLICT DO NOTHING;


CREATE TABLE IF NOT EXISTS tasks (
    id uuid PRIMARY KEY DEFAULT uuid_generate_v4(),
    task_type_id uuid NOT NULL REFERENCES task_types (id),
    task_priority_id uuid NOT NULL REFERENCES task_priorities (id),
    note text,
    
    contact_id uuid NOT NULL REFERENCES contacts (id),
    
    contract_number text,
    product_serial_number text,
    FOREIGN KEY (contract_number, product_serial_number) REFERENCES contracts_products (contract_number, product_serial_number) MATCH FULL,

    created_at timestamp with time zone NOT NULL DEFAULT NOW(),
    due_at timestamp with time zone,
    completed_at timestamp with time zone,

    created_by uuid NOT NULL REFERENCES employees (id),
    assigned_to uuid REFERENCES employees (id)
);

COMMIT;
