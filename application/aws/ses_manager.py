import json

import boto3


class SesManager:
    def __init__(self):
        self.client = boto3.client(
            "ses",
            region_name="us-east-1",
            endpoint_url="http://localstack:4566",
            aws_access_key_id="test",
            aws_secret_access_key="test",
        )

    def send_templated_email(self, source, destination, template_name, template_data):
        self.client.send_templated_email(
            Source=source,
            Destination={"ToAddresses": [destination]},
            Template=template_name,
            TemplateData=json.dumps(template_data),
        )


ses_manager = SesManager()  # type: ignore [no-untyped-call]
