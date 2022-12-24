new-migration:
	migrate create -dir "./simple_sales/migrations" -ext sql NAME
.PHONY: new-migration

_migrate:
	migrate -database "$$SIMPLE_SALES_DATABASE_MAIN_DB_DSN" -path "./simple_sales/migrations" up
.PHONY: _migrate

_rollback:
	migrate -database "$$SIMPLE_SALES_DATABASE_MAIN_DB_DSN" -path "./simple_sales/migrations" down 1
.PHONY: _rollback

_down-all:
	migrate -database "$$SIMPLE_SALES_DATABASE_MAIN_DB_DSN" -path "./simple_sales/migrations" down -all
.PHONY: _down-all

_force:
	migrate -database "$$SIMPLE_SALES_DATABASE_MAIN_DB_DSN" -path "./simple_sales/migrations" force -- $(V)
.PHONY: _force

version:
	migrate -database "$$SIMPLE_SALES_DATABASE_MAIN_DB_DSN" -path "./simple_sales/migrations" version
.PHONY: version

# Note: this dump doesn't include the migration version,
# although it probably should.
dump-db-schema:
	pg_dump -d "$$SIMPLE_SALES_DATABASE_MAIN_DB_DSN" --schema-only --no-privileges --no-owner > "./simple_sales/schema.sql"
.PHONY: dump-db-schema

migrate: _migrate dump-db-schema
.PHONY: migrate

rollback: _rollback dump-db-schema
.PHONY: rollback

down-all: _down-all dump-db-schema
.PHONY: down-all

force: _force dump-db-schema
.PHONY: force

connect-as-postgres-to-maintenance-db:
	psql -d "$$SIMPLE_SALES_DATABASE_MAINTENANCE_DB_DSN"
.PHONY: connect-as-postgres-to-maintenance-db

connect-as-postgres:
	psql -d "$$SIMPLE_SALES_DATABASE_MAIN_DB_DSN"
.PHONY: connect-as-postgres

#
# Scripts
#

create-db:
	psql -d "$$SIMPLE_SALES_DATABASE_MAINTENANCE_DB_DSN" -f - < "./simple_sales/scripts/1_create_database.up.sql"
.PHONY: create-db

drop-db:
	psql -d "$$SIMPLE_SALES_DATABASE_MAINTENANCE_DB_DSN" -f - < "./simple_sales/scripts/1_drop_database.down.sql"
.PHONY: drop-db

create-roles:
	psql -d "$$SIMPLE_SALES_DATABASE_MAINTENANCE_DB_DSN" -f - < "./simple_sales/scripts/2_create_roles.up.sql"
.PHONY: create-roles

drop-roles:
	psql -d "$$SIMPLE_SALES_DATABASE_MAINTENANCE_DB_DSN" -f - < "./simple_sales/scripts/2_drop_roles.down.sql"
.PHONY: drop-roles

# These are temporary, probably will be merged with create/drop roles later.
#
# Warning: when merging don't forget that we need to connect to the main
# database. We could utilize '\connect' in the create/drop roles scripts.

# Notice that we have to connect to the main database here.
grant-privileges:
	psql -d "$$SIMPLE_SALES_DATABASE_MAIN_DB_DSN" -f - < "./simple_sales/scripts/3_grant_privileges.up.sql"
.PHONY: create-privileges

# Notice that we have to connect to the main database here.
revoke-privileges:
	psql -d "$$SIMPLE_SALES_DATABASE_MAIN_DB_DSN" -f - < "./simple_sales/scripts/3_revoke_privileges.down.sql"
.PHONY: drop-privileges

# Notice that we have to connect to the main database here.
enable-row-security:
	psql -d "$$SIMPLE_SALES_DATABASE_MAIN_DB_DSN" -f - < "./simple_sales/scripts/4_enable_row_security.up.sql"
.PHONY: enable-row-security

# Notice that we have to connect to the main database here.
disable-row-security:
	psql -d "$$SIMPLE_SALES_DATABASE_MAIN_DB_DSN" -f - < "./simple_sales/scripts/4_disable_row_security.down.sql"
.PHONY: disable-row-security

# Notice that we have to connect to the main database here.
create-policies:
	psql -d "$$SIMPLE_SALES_DATABASE_MAIN_DB_DSN" -f - < "./simple_sales/scripts/5_create_policies.up.sql"
.PHONY: create-policies

# Notice that we have to connect to the main database here.
drop-policies:
	psql -d "$$SIMPLE_SALES_DATABASE_MAIN_DB_DSN" -f - < "./simple_sales/scripts/5_drop_policies.down.sql"
.PHONY: drop-policies

#
# Fake data
#

generate-fake-data:
	( cd simple_sales && python faker.py )
.PHONY: insert-data

# Notice that we have to connect to the main database here.
load-fake-data:
	psql -d "$$SIMPLE_SALES_DATABASE_MAIN_DB_DSN" -f - < "./simple_sales/fake_data.sql"
.PHONY: delete-data
