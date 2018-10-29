#!/bin/bash
set -e
echo "we are saying things"
psql -v ON_ERROR_STOP=1 --username $POSTGRES_USER --dbname $POSTGRES_DB <<-EOSQL
        CREATE TABLE  weblogs (
               day    date,
               status varchar(3)
               );
EOSQL
