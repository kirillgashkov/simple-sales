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

GRANT simple_sales_admin TO it_guy;

CREATE ROLE michael WITH
    INHERIT
    LOGIN
    PASSWORD '123';

GRANT simple_sales_manager TO michael;

CREATE ROLE jan WITH
    INHERIT
    LOGIN
    PASSWORD '123';

GRANT simple_sales_manager TO jan;

CREATE ROLE dwight WITH
    INHERIT
    LOGIN
    PASSWORD '123';

GRANT simple_sales_salesperson TO dwight;

CREATE ROLE jim WITH
    INHERIT
    LOGIN
    PASSWORD '123';

GRANT simple_sales_salesperson TO jim;

CREATE ROLE pam WITH
    INHERIT
    LOGIN
    PASSWORD '123';

GRANT simple_sales_salesperson TO pam;
