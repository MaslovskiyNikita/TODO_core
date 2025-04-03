import boto3


class SesManager:

    @staticmethod
    def get_ses_client():
        return boto3.client(
            "ses",
            region_name="us-east-1",
            endpoint_url="http://localstack:4566",
            aws_access_key_id="test",
            aws_secret_access_key="test",
        )
