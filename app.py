# Import necessary modules
from typing import Any, List, Union

import uvicorn
from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse

from src.utils.db_handler import MongoDBclient
from src.utils.s3_handler import S3Connection

# Initializing the FastAPI app
app = FastAPI(title="Image-Search-Data-Collection-Server")

# creating instances of MongoDB client and S3 connection
mongo = MongoDBclient()
s3 = S3Connection()

choices = {}

# fetch all labels
@app.get("/fetch")
def fetch_labels():
    try:
        global choices

        # fetch all documents from the "labels" collection in the MongoDB database
        result = mongo.database["labels"].find()
        docs = [doc for doc in result]
        choices = dict(docs[0])

        # create a response dictionary
        response = {"Status": "Success", "Response": str(docs[0])}

        # return a JSON response
        return JSONResponse(
            content=response, status_code=200, media_type="application/json"
        )
    except Exception as e:
        raise e


# label post API
@app.post("add_label/{label_name}")
def add_label(label_name: str):

    # retrieve all documents from the "labels" collection in the MongoDB database
    result = mongo.database["labels"].find()
    docs = [doc for doc in result]

    # get the highest numerical key from the first document (excluding _id field)
    last_val = list(map(int, list(docs[0].keys())[1:]))[-1]

    # update the first document by adding new field with new label
    response = mongo.database["labels"].update_one(
        {"_id": docs[0]["_id"]}, {"$set": {str(last_val + 1): label_name}}
    )

    # check if update was successful
    if response.modified_count == 1:
        # if yes, then add label to S3
        response = s3.add_label(label_name)
        return {"Status": "Success", "S3-Response": response}
    else:
        # or else return failure message
        return {"Status": "Fail", "Message": response[1]}


@app.get("/single_upload/")
def single_upload():

    # create a dictionary with info about the response
    info = {"Response": "Available", "Post-Request-Body": ["label", "Files"]}

    # return response
    return JSONResponse(content=info, status_code=200, media_type="application/json")


@app.post("/single_upload/")
async def single_upload(label, file: UploadFile = None):
    """
    Responsible for single image upload to S3.

    Args:
        label (str): label for the image
        file (UploadFile, Optional): the image file to be uploaded

    Returns:
        dict: A dictionary containing filename, label and response from S3 if successful else error message

    """

    # check if label is in the dictionary or not
    label = choices.get(label, False)
    if file.content_type == "image/jpeg" and label != False:
        # upload file to S3
        response = s3.upload_to_s3(file.file, label)
        return {"filename": file.filename, "label": label, "S3-Response": response}
    else:
        return {
            "ContentType": f"content type should be image/jpeg not {file.content_type}",
            "LabelFound": label,
        }


@app.get("/bulk_upload")
def bulk_upload():

    # create a dictionary with info about the response
    info = {"Response": "Available", "Post-Request-Body": ["label", "Files"]}

    # return response
    return JSONResponse(content=info, status_code=200, media_type="application/json")


@app.post("/bulk_upload")
def bulk_upload(label, files: List[UploadFile] = File(...)):
    """
    Upload multiple images to S3 with specified label.

    Args:
        label (str): label for the image
        files (List[UploadFile]): list of image files to upload

    Returns:
        dict: A dictionary containing filename, label and response from S3 if successful else error message

    """
    try:

        # list to track unspported files
        skipped = []
        final_response = None
        label: Union[bool, Any] = choices.get(label, False)

        if label:
            for file in files:
                # check if file is JPEG
                if file.content_type == "image/jpeg":
                    # upload to S3
                    response = s3.upload_to_s3(file.file, label)
                    final_response = response
                else:
                    skipped.append(file.filename)
            return {
                "label": label,
                "skipped": skipped,
                "S3-Response": final_response,
                "LabelFound": label,
            }
        else:
            return {
                "label": label,
                "skipped": skipped,
                "S3-Response": final_response,
                "LabelFound": label,
            }
    except Exception as e:
        return {"ContentType": f"content type should be image/jpeg not {e}"}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080)
