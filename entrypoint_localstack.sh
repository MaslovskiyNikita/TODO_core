#!/bin/sh

docker-entrypoint.sh &

awslocal ses verify-email-identity --email-address "$EMAIL_HOST_USER"

wait