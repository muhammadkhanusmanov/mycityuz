import pyimgur
from django.conf import settings

CLIENT_ID = settings.IMGUR_CLIENT_ID

def upload_image_to_imgur(image):
    im = pyimgur.Imgur(CLIENT_ID)
    uploaded_image = im.upload_image(image.temporary_file_path(), title="MyPics")
    return uploaded_image.link