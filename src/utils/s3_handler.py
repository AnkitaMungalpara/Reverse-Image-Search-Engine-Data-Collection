# import necessary packages
import os
import sys
from typing import Dict

import boto3
import boto3.session

from src.exception import CustomException
from src.utils.utils import image_unique_names


class S3Connection:
    "Data class for performing reverse image search engine"

    def __init__(self) -> None:
        # initialize S3 session
        session = boto3.Session(
            aws_acces_key=os.environ["AWS_ACCESS_KEY_ID"],
            aws_secret_access_key=os.environ["AWS_SECRET_ACCESS_KEY"],
        )

        # connect to S3 and initialize session
        self.s3 = session.resource("s3")
        self.bucket = self.s3.Bucket(os.environ["AWS_BUCKET_NAME"])

    def add_label(self, label: str) -> Dict:
        try:
            key = f"images/{label}/"
            # create empty object in S3
            response = self.bucket.put_object(Body="", Key=key)
            return {"Created": True, "Path": response.key}
        except Exception as e:
            message = CustomException(e, sys)
            return {"Created": False, "Reason": message.error_message}

    def upload_to_s3(self, image_path, label):
        try:
            # upload file to S3
            self.bucket.upload_fileobj(
                image_path,
                f"images/{label}/{image_unique_names()}.jpeg",
                ExtraArgs={"ACL": "public-read"},
            )
            return {"Created": True}
        except Exception as e:
            message = CustomException(e, sys)
            return {"Created": False, "Reason": message.error_message}
