#!/bin/bash

echo "$(date) Running 'delete_old_tasks.sh' cronjob..."

(
set -e

psql -d "$SIMPLE_SALES_DATABASE_MAIN_DB_DSN" <<EOF
    SET ROLE simple_sales_admin;
    DELETE FROM tasks WHERE completed_at < now() - INTERVAL '12 months';
EOF
)

echo "$(date) Finished running 'delete_old_tasks.sh' cronjob."
