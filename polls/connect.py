import dropbox
from django.conf import settings

def upload_image_to_dropbox(file_path, file_name):
    dbx = dropbox.Dropbox('')
    with open(file_path, 'rb') as f:
        dbx.files_upload(f.read(), f'/{file_name}', mode=dropbox.files.WriteMode.overwrite)
    link = dbx.sharing_create_shared_link(f'/{file_name}')
    return link.url.replace('?dl=0', '?raw=1')
