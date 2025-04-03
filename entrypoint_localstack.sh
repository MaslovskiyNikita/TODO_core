#!/bin/sh

awslocal --endpoint-url=http://localstack:4566 ses verify-email-identity --email-address your@email.com