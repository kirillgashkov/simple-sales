CREATE ROLE simple_sales_admin
WITH
    NOINHERIT
    CREATEDB
    CREATEROLE;

CREATE ROLE simple_sales_manager
WITH
    NOINHERIT;

CREATE ROLE simple_sales_salesperson
WITH
    NOINHERIT;


CREATE ROLE it_guy WITH
    INHERIT
    LOGIN
    PASSWORD '123'
    -- CREATE DB and CREATE ROLE are not inherited by default
    CREATEDB
    CREATEROLE;

GRANT it_guy TO simple_sales_admin;

CREATE ROLE michael WITH
    INHERIT
    LOGIN
    PASSWORD '123';

GRANT michael TO simple_sales_manager;

CREATE ROLE jan WITH
    INHERIT
    LOGIN
    PASSWORD '123';

GRANT jan TO simple_sales_manager;

CREATE ROLE dwight WITH
    INHERIT
    LOGIN
    PASSWORD '123';

GRANT dwight TO simple_sales_salesperson;

CREATE ROLE jim WITH
    INHERIT
    LOGIN
    PASSWORD '123';

GRANT jim TO simple_sales_salesperson;

CREATE ROLE pam WITH
    INHERIT
    LOGIN
    PASSWORD '123';

GRANT pam TO simple_sales_salesperson;
