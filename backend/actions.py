import hashlib


def unique_face_id(media_url : str , face_index : int , frame_index : int):
    return hashlib.sha256(media_url.encode()).hexdigest() + "_" + str(face_index) + "_" + str(frame_index)