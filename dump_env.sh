#!/bin/sh
set -e

# Store env variables in a file. This is needed because cronjobs don't inherit env variables from
# the process that executes the crontab
export -p > /app/container.env
chmod 600 /app/container.env

exec cron -f