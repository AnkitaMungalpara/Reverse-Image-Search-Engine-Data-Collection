# import necessary packages
import os
import shutil
import sys
from zipfile import ZipFile

from src.exception import CustomException


class DataStore:
    def __init__(self):

        # initialize the root directory where data is stored
        self.root = os.path.join(os.getcwd(), "data")

        self.zip = os.path.join(self.root, "archive.zip")
        self.images = os.path.join(self.root, "archive")
        self.list_unwanted = ["BACKGROUND_Google"]

    def prepare_data(self):
        """
        Extracts data from a zip file to a specified directory.

        Returns:
            dict: A dictionary specifying if extraction is successful or not

        """

        try:
            print("Extracting data...")
            with ZipFile(self.zip, "r") as file:
                file.extractall(path=self.root)

            file.close()
            print(" DONE!")
        except Exception as e:
            message = CustomException(e, sys)
            return {"Created": False, "Reason": message.error_message}

    def remove_unwanted_classes(self):
        """
        Remove unwanted classes from specified (images) directory

        Returns:
            dict

        """

        try:
            print("Removing unwanted classes...")
            for label in self.list_unwanted:
                path = os.path.join(self.images, label)
                shutil.rmtree(path, ignore_errors=True)
            print(" DONE!")
        except Exception as e:
            message = CustomException(e, sys)
            return {"Created": False, "Reason": message.error_message}

    def sync_data(self):
        """
        Syncs local images directory to AWS S3 bucket

        Returns:
            dict

        """
        try:
            print("=============== Starting data sync ===============")

            os.system(
                f"aws s3 sync '{self.images}' s3://data-collection-image-search/images/ "
            )

            print("===================== DONE! =====================")
        except Exception as e:
            message = CustomException(e, sys)
            return {"Created": False, "Reason": message.error_message}

    def run_step(self):
        """
        Executes a series of steps to prepare data, remove unwanted classes and synchonize data

        Returns:
            bool or dict: True if execution is successful else dictionary with error message

        """
        try:
            self.prepare_data()
            self.remove_unwanted_classes()
            self.sync_data()
            return True
        except Exception as e:
            message = CustomException(e, sys)
            return {"Created": False, "Reason": message.error_message}


if __name__ == "__main__":
    store = DataStore()
    store.run_step()
