# import required modules
import os
import sys

from src.exception import CustomException
from src.utils.db_handler import MongoDBclient


class MetaDataStore:
    def __init__(self) -> None:

        # root directory for data
        self.root = os.path.join(os.getcwd(), "data")
        # directory for images
        self.images = os.path.join(self.root, "archive")
        self.labels = os.listdir(self.images)
        # MongoDB client instance
        self.mongo = MongoDBclient()

    def register_labels(self):
        try:
            # prepare records to insert into MongoDB 'labels' collection
            records = {}
            for num, label in enumerate(self.labels):
                records[f"{num}"] = label

            # insert records
            self.mongo.database["labels"].insert_one(records)

        except Exception as e:
            message = CustomException(e, sys)
            return {"Created": False, "Reason": message.error_message}

    def run_step(self):
        try:
            # execute label registration process
            self.register_labels()
        except Exception as e:
            message = CustomException(e, sys)
            return {"Created": False, "Reason": message.error_message}


if __name__ == "__main__":
    meta = MetaDataStore()
    meta.run_step()
