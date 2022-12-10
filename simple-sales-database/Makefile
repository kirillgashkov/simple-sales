new-migration:
	migrate create -dir "./simple_sales/migrations" -ext sql NAME
.PHONY: new-migration

migrate:
	migrate -database "$$SIMPLE_SALES_DATABASE_MAIN_DB_DSN" -path "./simple_sales/migrations" up
.PHONY: migrate

rollback:
	migrate -database "$$SIMPLE_SALES_DATABASE_MAIN_DB_DSN" -path "./simple_sales/migrations" down 1
.PHONY: rollback

down-all:
	migrate -database "$$SIMPLE_SALES_DATABASE_MAIN_DB_DSN" -path "./simple_sales/migrations" down -all
.PHONY: down-all

force:
	migrate -database "$$SIMPLE_SALES_DATABASE_MAIN_DB_DSN" -path "./simple_sales/migrations" force -- $(V)
.PHONY: force

version:
	migrate -database "$$SIMPLE_SALES_DATABASE_MAIN_DB_DSN" -path "./simple_sales/migrations" version
.PHONY: version

create-db:
	psql -d "$$SIMPLE_SALES_DATABASE_MAINTENANCE_DB_DSN" -f - < "./simple_sales/create_database.sql"
.PHONY: create-db

drop-db:
	psql -d "$$SIMPLE_SALES_DATABASE_MAINTENANCE_DB_DSN" -f - < "./simple_sales/drop_database.sql"
.PHONY: drop-db

connect-to-db:
	psql -d "$$SIMPLE_SALES_DATABASE_MAIN_DB_DSN"
.PHONY: connect-to-db

# Note: this dump doesn't include the migration version,
# although it probably should.
dump-db-schema:
	pg_dump -d "$$SIMPLE_SALES_DATABASE_MAIN_DB_DSN" --schema-only --no-privileges --no-owner > "./simple_sales/schema.sql"
.PHONY: dump-db-schema
