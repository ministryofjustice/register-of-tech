#!/bin/bash

echo "****** CREATING ROT DATABASE ******"
psql -U postgres <<- EOSQL
   CREATE DATABASE rot ENCODING 'UTF8';
EOSQL
echo ""
echo "****** DASHBOARD ROT CREATED ******"
