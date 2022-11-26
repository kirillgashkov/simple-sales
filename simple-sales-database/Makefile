new-migration:
	migrate create -dir "./simple_sales/migrations" -ext sql NAME
.PHONY: new-migration

migrate:
	migrate -database "$$SIMPLE_SALES_DATABASE_MAIN_DB_DSN" -path "./simple_sales/migrations" up
.PHONY: migrate

rollback:
	migrate -database "$$SIMPLE_SALES_DATABASE_MAIN_DB_DSN" -path "./simple_sales/migrations" down 1
.PHONY: rollback

force:
	migrate -database "$$SIMPLE_SALES_DATABASE_MAIN_DB_DSN" -path "./simple_sales/migrations" force -- $(V)
.PHONY:

create-db:
	psql -d "$$SIMPLE_SALES_DATABASE_MAINTENANCE_DB_DSN" -f - < "./simple_sales/create_database.sql"
.PHONY: create-db

drop-db:
	psql -d "$$SIMPLE_SALES_DATABASE_MAINTENANCE_DB_DSN" -f - < "./simple_sales/drop_database.sql"
.PHONY: drop-db

connect-to-db:
	psql -d "$$SIMPLE_SALES_DATABASE_MAIN_DB_DSN"
.PHONY: connect-to-db
