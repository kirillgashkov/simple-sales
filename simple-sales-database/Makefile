create-db:
	psql -d "$$SIMPLE_SALES_DATABASE_MAINTENANCE_DB_DSN" -f - < "./simple_sales/create_database.sql"
.PHONY: create-db

drop-db:
	psql -d "$$SIMPLE_SALES_DATABASE_MAINTENANCE_DB_DSN" -f - < "./simple_sales/drop_database.sql"
.PHONY: create-db

migrations-up:
	migrate -database "$$SIMPLE_SALES_DATABASE_MAIN_DB_DSN" -path "./simple_sales/migrations" up
.PHONY: migrations-up

migrations-down:
	migrate -database "$$SIMPLE_SALES_DATABASE_MAIN_DB_DSN" -path "./simple_sales/migrations" down -all
.PHONY: migrations-down

migrations-rollback:
	migrate -database "$$SIMPLE_SALES_DATABASE_MAIN_DB_DSN" -path "./simple_sales/migrations" down 1
.PHONY: migrations-rollback
