#!/bin/bash

CONTAINER_NAME="ctf-db"
MYSQL_USER="root"
MYSQL_PASSWORD="rootpassword"
BACKUP_DIR="/tmp"
DB_NAME="mydb"
DATE=$(date +%F_%H-%M-%S)
BACKUP_FILE="${BACKUP_DIR}/mysql_backup_${DATE}.sql"

mkdir -p "${BACKUP_DIR}"

docker exec "${CONTAINER_NAME}" sh -c "mysqldump -u${MYSQL_USER} -p${MYSQL_PASSWORD} mydb > ${BACKUP_FILE}"

docker cp ${CONTAINER_NAME}:${BACKUP_FILE} /home/apa/backup/sql_files/mysql_backup_$(date +%F_%H-%M-%S).sql

