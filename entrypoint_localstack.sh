#!/bin/sh

docker-entrypoint.sh &

sleep 10

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