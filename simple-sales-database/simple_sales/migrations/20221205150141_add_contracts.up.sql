BEGIN;

CREATE TABLE IF NOT EXISTS contracts (
    number text PRIMARY KEY,
    client_id uuid NOT NULL REFERENCES clients (id),
    start_date date NOT NULL,
    end_date date NOT NULL,
    CONSTRAINT end_date_after_start_date CHECK (end_date >= start_date)
);

CREATE TABLE IF NOT EXISTS contracts_products (
    contract_number text REFERENCES contracts (number),
    product_serial_number text REFERENCES products (serial_number),
    PRIMARY KEY (contract_number, product_serial_number)
);

COMMIT;
