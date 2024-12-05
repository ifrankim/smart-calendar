from models.photo import Photo


def capture_and_process():
    photo_path = Photo.capture()
    return Photo.send_to_backend(photo_path)
