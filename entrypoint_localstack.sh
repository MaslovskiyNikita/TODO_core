#!/bin/sh

docker-entrypoint.sh &

until curl -s http://localhost:4566/_localstack/health | grep -q '"ses": "available"'; do
  echo "Waiting for LocalStack SES..."
  sleep 2
done

awslocal ses verify-email-identity --email-address "$EMAIL_HOST_USER"

echo "Creating SES templates..."
for template in ${TEMPLATES_DIR}/*.json; do
  if [ -f "$template" ]; then
    echo "Processing template: ${template}"
    awslocal ses create-template --template "file://${template}"
  else
    echo "No templates found in ${TEMPLATES_DIR}"
    break
  fi
done


wait