#!/bin/sh
set -e
mc alias set myminio http://minio:9000 minioadmin minioadmin
mc mb myminio/payday