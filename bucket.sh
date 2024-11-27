#!/bin/sh
set -e
mc alias set myminio http://46.101.90.67:9000 minioadmin minioadmin
mc mb myminio/payday