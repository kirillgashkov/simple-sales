#!/usr/bin/env bash

set -e
shopt -s nullglob


copy_glob_from_into() {
    local from="$1"
    local into="$2"

    if [ ! -d "$from" ]; then
        echo "Directory '$from' does not exist"
        return
    fi

    if [ ! -d "$into" ]; then
        echo "Directory '$into' does not exist"
        return
    fi

    local glob_matched=0

    # Needs 'nullglob' to be set.
    for file in "$from"/*; do
        glob_matched=1
        cp -v "$file" "$into"
    done

    if [ "$glob_matched" = 0 ]; then
        echo "No '$from/*' files found"
    fi
}


if [ "$1" = "cron" ]; then
    echo "Copying simple_sales cronjobs..."

    copy_glob_from_into /app/simple_sales/cronjobs/15min /etc/periodic/15min
    copy_glob_from_into /app/simple_sales/cronjobs/daily /etc/periodic/daily
    copy_glob_from_into /app/simple_sales/cronjobs/hourly /etc/periodic/hourly
    copy_glob_from_into /app/simple_sales/cronjobs/monthly /etc/periodic/monthly
    copy_glob_from_into /app/simple_sales/cronjobs/weekly /etc/periodic/weekly

    echo "Starting cron daemon..."

    touch /var/log/cron.log  # Create the log file to be able to run tail

    crond -f && tail -f /var/log/cron.log
else
    exec "$@"
fi
