BEGIN;

CREATE TABLE IF NOT EXISTS product_models (
    id uuid PRIMARY KEY DEFAULT uuid_generate_v4(),
    name text NOT NULL
);

CREATE TABLE IF NOT EXISTS products (
    serial_number text PRIMARY KEY,
    product_model_id uuid NOT NULL REFERENCES product_models (id)
);

COMMIT;
