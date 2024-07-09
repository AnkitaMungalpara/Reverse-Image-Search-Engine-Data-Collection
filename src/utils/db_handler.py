import os

import pymongo


class MongoDBclient:
    client = None

    def __init__(self, database_name=os.environ["DATABASE_NAME"]):
        # initialize MongoDB client
        if MongoDBclient.client is None:
            # establish connection to MongoDB
            MongoDBclient.client = pymongo.MongoClient(
                f"mongodb+srv://{os.environ['ATLAS_CLUSTER_USERNAME']}:{os.environ['ATLAS_CLUSTER_PASSWORD']}@cluster0.kyn1evb.mongodb.net/?retryWrites=true&w=majority"
            )
        self.client = MongoDBclient.client

        # access the specified database within MongoDB cluster
        self.database = self.client[database_name]

        self.database_name = database_name
