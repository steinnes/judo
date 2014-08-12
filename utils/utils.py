import time
import hashlib


class InvalidFileUpload(Exception):
    pass


def save_file(upload):
    print "upload=", upload
    FILE_SAVE_PATH = '/tmp/judo'
    allowed_filetypes = {
        'image/jpeg': ('jpg', 'jpeg'),
        'image/png': ('png'),
        'application/pdf': ('pdf')
    }
    if upload.content_type not in allowed_filetypes:
        raise InvalidFileUpload("Invalid file type")
    file_suffix = upload.filename.split(".")[-1].lower()
    if file_suffix not in allowed_filetypes[upload.content_type]:
        raise InvalidFileUpload("Invalid file suffix: {}, supported for this type: {}".format(
            file_suffix, allowed_filetypes[upload.content_type]))

    file_path = "{}/{}".format(FILE_SAVE_PATH, hashlib.sha1(upload.filename + str(time.time())).hexdigest())
    f = open(file_path, "w")
    f.write(upload.file.read())
    return file_path

def scan_attachments(form):
    """
    returns a list of objects in form if they are named attachment_*
    ... this isn't fragile, nooooo
    """
    return [getattr(form, field) for field in form.__dict__['dict'].keys() if field.startswith('attachment_')]