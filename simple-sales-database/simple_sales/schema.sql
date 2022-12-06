--
-- PostgreSQL database dump
--

-- Dumped from database version 15.1
-- Dumped by pg_dump version 15.0 (Homebrew)

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

--
-- Name: uuid-ossp; Type: EXTENSION; Schema: -; Owner: -
--

CREATE EXTENSION IF NOT EXISTS "uuid-ossp" WITH SCHEMA public;


--
-- Name: EXTENSION "uuid-ossp"; Type: COMMENT; Schema: -; Owner: -
--

COMMENT ON EXTENSION "uuid-ossp" IS 'generate universally unique identifiers (UUIDs)';


SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: addresses; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.addresses (
    id uuid DEFAULT public.uuid_generate_v4() NOT NULL,
    postal_code text NOT NULL,
    city_id uuid NOT NULL,
    street text NOT NULL,
    house text NOT NULL,
    apartment text,
    note text
);


--
-- Name: cities; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.cities (
    id uuid DEFAULT public.uuid_generate_v4() NOT NULL,
    city_name text NOT NULL,
    region_name text
);


--
-- Name: clients; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.clients (
    id uuid DEFAULT public.uuid_generate_v4() NOT NULL,
    organization_name text NOT NULL,
    city_id uuid
);


--
-- Name: contacts; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.contacts (
    id uuid DEFAULT public.uuid_generate_v4() NOT NULL,
    client_id uuid NOT NULL,
    first_name text,
    middle_name text,
    last_name text,
    phone text,
    email text,
    address_id uuid,
    note text,
    CONSTRAINT at_least_one_name_or_note CHECK ((num_nonnulls(first_name, middle_name, last_name, note) > 0))
);


--
-- Name: contracts; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.contracts (
    number text NOT NULL,
    client_id uuid NOT NULL,
    delivery_address_id uuid,
    delivery_from timestamp with time zone,
    delivery_to timestamp with time zone,
    warranty_from timestamp with time zone,
    warranty_to timestamp with time zone,
    description text,
    CONSTRAINT contracts_delivery_from_delivery_to_check CHECK ((delivery_from <= delivery_to)),
    CONSTRAINT contracts_warranty_from_warranty_to_check CHECK ((warranty_from <= warranty_to))
);


--
-- Name: contracts_products; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.contracts_products (
    contract_number text NOT NULL,
    product_serial_number text NOT NULL
);


--
-- Name: employee_types; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.employee_types (
    id uuid DEFAULT public.uuid_generate_v4() NOT NULL,
    name text NOT NULL
);


--
-- Name: employees; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.employees (
    id uuid DEFAULT public.uuid_generate_v4() NOT NULL,
    employee_type_id uuid NOT NULL,
    first_name text NOT NULL,
    middle_name text,
    last_name text NOT NULL,
    city_id uuid NOT NULL
);


--
-- Name: product_models; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.product_models (
    id uuid DEFAULT public.uuid_generate_v4() NOT NULL,
    name text NOT NULL
);


--
-- Name: products; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.products (
    serial_number text NOT NULL,
    product_model_id uuid NOT NULL
);


--
-- Name: schema_migrations; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.schema_migrations (
    version bigint NOT NULL,
    dirty boolean NOT NULL
);


--
-- Name: sessions; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.sessions (
    id uuid DEFAULT public.uuid_generate_v4() NOT NULL,
    user_id uuid NOT NULL,
    created_at timestamp with time zone DEFAULT now() NOT NULL,
    expires_at timestamp with time zone NOT NULL,
    CONSTRAINT expires_at_after_created_at CHECK ((expires_at > created_at))
);


--
-- Name: task_priorities; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.task_priorities (
    id uuid DEFAULT public.uuid_generate_v4() NOT NULL,
    level smallint NOT NULL,
    name text NOT NULL
);


--
-- Name: task_types; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.task_types (
    id uuid DEFAULT public.uuid_generate_v4() NOT NULL,
    name text NOT NULL
);


--
-- Name: tasks; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.tasks (
    id uuid DEFAULT public.uuid_generate_v4() NOT NULL,
    task_type_id uuid NOT NULL,
    task_priority_id uuid NOT NULL,
    note text,
    contact_id uuid NOT NULL,
    contract_number text,
    product_serial_number text,
    created_at timestamp with time zone DEFAULT now() NOT NULL,
    due_at timestamp with time zone,
    completed_at timestamp with time zone,
    created_by uuid NOT NULL,
    assigned_to uuid
);


--
-- Name: users; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.users (
    id uuid DEFAULT public.uuid_generate_v4() NOT NULL,
    username text NOT NULL,
    password_hash text NOT NULL,
    employee_id uuid NOT NULL
);


--
-- Name: addresses addresses_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.addresses
    ADD CONSTRAINT addresses_pkey PRIMARY KEY (id);


--
-- Name: cities cities_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.cities
    ADD CONSTRAINT cities_pkey PRIMARY KEY (id);


--
-- Name: clients clients_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.clients
    ADD CONSTRAINT clients_pkey PRIMARY KEY (id);


--
-- Name: contacts contacts_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.contacts
    ADD CONSTRAINT contacts_pkey PRIMARY KEY (id);


--
-- Name: contracts contracts_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.contracts
    ADD CONSTRAINT contracts_pkey PRIMARY KEY (number);


--
-- Name: contracts_products contracts_products_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.contracts_products
    ADD CONSTRAINT contracts_products_pkey PRIMARY KEY (contract_number, product_serial_number);


--
-- Name: employee_types employee_types_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.employee_types
    ADD CONSTRAINT employee_types_pkey PRIMARY KEY (id);


--
-- Name: employees employees_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.employees
    ADD CONSTRAINT employees_pkey PRIMARY KEY (id);


--
-- Name: product_models product_models_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.product_models
    ADD CONSTRAINT product_models_pkey PRIMARY KEY (id);


--
-- Name: products products_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.products
    ADD CONSTRAINT products_pkey PRIMARY KEY (serial_number);


--
-- Name: schema_migrations schema_migrations_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.schema_migrations
    ADD CONSTRAINT schema_migrations_pkey PRIMARY KEY (version);


--
-- Name: sessions sessions_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.sessions
    ADD CONSTRAINT sessions_pkey PRIMARY KEY (id);


--
-- Name: task_priorities task_priorities_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.task_priorities
    ADD CONSTRAINT task_priorities_pkey PRIMARY KEY (id);


--
-- Name: task_types task_types_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.task_types
    ADD CONSTRAINT task_types_pkey PRIMARY KEY (id);


--
-- Name: tasks tasks_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.tasks
    ADD CONSTRAINT tasks_pkey PRIMARY KEY (id);


--
-- Name: users users_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_pkey PRIMARY KEY (id);


--
-- Name: contracts_products_product_serial_number_contract_number_idx; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX contracts_products_product_serial_number_contract_number_idx ON public.contracts_products USING btree (product_serial_number, contract_number);


--
-- Name: users_username_lower_idx; Type: INDEX; Schema: public; Owner: -
--

CREATE UNIQUE INDEX users_username_lower_idx ON public.users USING btree (lower(username));


--
-- Name: addresses addresses_city_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.addresses
    ADD CONSTRAINT addresses_city_id_fkey FOREIGN KEY (city_id) REFERENCES public.cities(id);


--
-- Name: clients clients_city_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.clients
    ADD CONSTRAINT clients_city_id_fkey FOREIGN KEY (city_id) REFERENCES public.cities(id);


--
-- Name: contacts contacts_address_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.contacts
    ADD CONSTRAINT contacts_address_id_fkey FOREIGN KEY (address_id) REFERENCES public.addresses(id);


--
-- Name: contacts contacts_client_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.contacts
    ADD CONSTRAINT contacts_client_id_fkey FOREIGN KEY (client_id) REFERENCES public.clients(id);


--
-- Name: contracts contracts_client_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.contracts
    ADD CONSTRAINT contracts_client_id_fkey FOREIGN KEY (client_id) REFERENCES public.clients(id);


--
-- Name: contracts contracts_delivery_address_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.contracts
    ADD CONSTRAINT contracts_delivery_address_id_fkey FOREIGN KEY (delivery_address_id) REFERENCES public.addresses(id);


--
-- Name: contracts_products contracts_products_contract_number_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.contracts_products
    ADD CONSTRAINT contracts_products_contract_number_fkey FOREIGN KEY (contract_number) REFERENCES public.contracts(number);


--
-- Name: contracts_products contracts_products_product_serial_number_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.contracts_products
    ADD CONSTRAINT contracts_products_product_serial_number_fkey FOREIGN KEY (product_serial_number) REFERENCES public.products(serial_number);


--
-- Name: employees employees_city_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.employees
    ADD CONSTRAINT employees_city_id_fkey FOREIGN KEY (city_id) REFERENCES public.cities(id);


--
-- Name: employees employees_employee_type_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.employees
    ADD CONSTRAINT employees_employee_type_id_fkey FOREIGN KEY (employee_type_id) REFERENCES public.employee_types(id);


--
-- Name: products products_product_model_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.products
    ADD CONSTRAINT products_product_model_id_fkey FOREIGN KEY (product_model_id) REFERENCES public.product_models(id);


--
-- Name: sessions sessions_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.sessions
    ADD CONSTRAINT sessions_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id);


--
-- Name: tasks tasks_assigned_to_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.tasks
    ADD CONSTRAINT tasks_assigned_to_fkey FOREIGN KEY (assigned_to) REFERENCES public.employees(id);


--
-- Name: tasks tasks_contact_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.tasks
    ADD CONSTRAINT tasks_contact_id_fkey FOREIGN KEY (contact_id) REFERENCES public.contacts(id);


--
-- Name: tasks tasks_contract_number_product_serial_number_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.tasks
    ADD CONSTRAINT tasks_contract_number_product_serial_number_fkey FOREIGN KEY (contract_number, product_serial_number) REFERENCES public.contracts_products(contract_number, product_serial_number) MATCH FULL;


--
-- Name: tasks tasks_created_by_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.tasks
    ADD CONSTRAINT tasks_created_by_fkey FOREIGN KEY (created_by) REFERENCES public.employees(id);


--
-- Name: tasks tasks_task_priority_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.tasks
    ADD CONSTRAINT tasks_task_priority_id_fkey FOREIGN KEY (task_priority_id) REFERENCES public.task_priorities(id);


--
-- Name: tasks tasks_task_type_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.tasks
    ADD CONSTRAINT tasks_task_type_id_fkey FOREIGN KEY (task_type_id) REFERENCES public.task_types(id);


--
-- Name: users users_employee_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_employee_id_fkey FOREIGN KEY (employee_id) REFERENCES public.employees(id);


--
-- PostgreSQL database dump complete
--
