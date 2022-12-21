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

create-roles:
	psql -d "$$SIMPLE_SALES_DATABASE_MAINTENANCE_DB_DSN" -f - < "./simple_sales/create_roles.sql"
.PHONY: create-roles

drop-roles:
	psql -d "$$SIMPLE_SALES_DATABASE_MAINTENANCE_DB_DSN" -f - < "./simple_sales/drop_roles.sql"
.PHONY: drop-roles

create-db:
	psql -d "$$SIMPLE_SALES_DATABASE_MAINTENANCE_DB_DSN" -f - < "./simple_sales/create_database.sql"
.PHONY: create-db

drop-db:
	psql -d "$$SIMPLE_SALES_DATABASE_MAINTENANCE_DB_DSN" -f - < "./simple_sales/drop_database.sql"
.PHONY: drop-db

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

# These commands are for testing purposes only.

connect-as-it-guy:
	psql -d "postgresql://it_guy:123@localhost:5432/simple_sales?sslmode=disable"
.PHONY: connect-as-it-guy

connect-as-michael:
	psql -d "postgresql://michael:123@localhost:5432/simple_sales?sslmode=disable"
.PHONY: connect-as-michael

connect-as-jan:
	psql -d "postgresql://jan:123@localhost:5432/simple_sales?sslmode=disable"
.PHONY: connect-as-jan

connect-as-dwight:
	psql -d "postgresql://dwight:123@localhost:5432/simple_sales?sslmode=disable"
.PHONY: connect-as-dwight

connect-as-jim:
	psql -d "postgresql://jim:123@localhost:5432/simple_sales?sslmode=disable"
.PHONY: connect-as-jim

connect-as-pam:
	psql -d "postgresql://pam:123@localhost:5432/simple_sales?sslmode=disable"
.PHONY: connect-as-pam

connect-as-admin: connect-as-it-guy
.PHONY: connect-as-salesperson

connect-as-manager: connect-as-michael
.PHONY: connect-as-salesperson

connect-as-salesperson: connect-as-dwight
.PHONY: connect-as-salesperson
