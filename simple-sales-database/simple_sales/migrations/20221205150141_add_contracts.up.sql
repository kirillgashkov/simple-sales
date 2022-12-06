BEGIN;

CREATE TABLE IF NOT EXISTS contracts (
    number text PRIMARY KEY,
    client_id uuid NOT NULL REFERENCES clients (id),

    delivery_address_id uuid REFERENCES addresses (id),
    delivery_from timestamp with time zone,
    delivery_to timestamp with time zone,

    warranty_from timestamp with time zone,
    warranty_to timestamp with time zone,

    description text,

    CONSTRAINT contracts_delivery_from_delivery_to_check CHECK (delivery_from <= delivery_to),
    CONSTRAINT contracts_warranty_from_warranty_to_check CHECK (warranty_from <= warranty_to)
);


CREATE TABLE IF NOT EXISTS contracts_products (
    contract_number text REFERENCES contracts (number),
    product_serial_number text REFERENCES products (serial_number),
    PRIMARY KEY (contract_number, product_serial_number)
);

CREATE INDEX IF NOT EXISTS contracts_products_product_serial_number_contract_number_idx ON contracts_products (product_serial_number, contract_number);

COMMIT;
