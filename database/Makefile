# Note: this dump doesn't include the migration version,
# although it probably should.
dump-db-schema:
	pg_dump -d "$$SIMPLE_SALES_DATABASE_MAIN_DB_DSN" --schema-only --no-owner > "./simple_sales/schema.sql"
.PHONY: dump-db-schema

new-migration:
	migrate create -dir "./simple_sales/migrations" -ext sql NAME
.PHONY: new-migration

migrate: dump-db-schema
	migrate -database "$$SIMPLE_SALES_DATABASE_MAIN_DB_DSN" -path "./simple_sales/migrations" up
.PHONY: migrate

rollback: dump-db-schema
	migrate -database "$$SIMPLE_SALES_DATABASE_MAIN_DB_DSN" -path "./simple_sales/migrations" down 1
.PHONY: rollback

remigrate: rollback migrate
.PHONY: remigrate

version:
	migrate -database "$$SIMPLE_SALES_DATABASE_MAIN_DB_DSN" -path "./simple_sales/migrations" version
.PHONY: version

force:
	migrate -database "$$SIMPLE_SALES_DATABASE_MAIN_DB_DSN" -path "./simple_sales/migrations" force -- $(V)
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
