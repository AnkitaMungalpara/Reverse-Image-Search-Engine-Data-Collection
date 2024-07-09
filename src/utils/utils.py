import uuid

# generate unique names for all images
def image_unique_names():
    return f"img-{str(uuid.uuid1)}"
