import os
import Face_Harvester
import Digital_Identity
import Face_Detection
os.environ["TF_CPP_MIN_LOG_LEVEL"] = '2'
os.environ["TF_ENABLE_ONEDNN_OPTS"] = '0'
import dataset_reader
import logging
import warnings
import IVF
import config
import metadata as metadata_module
from metadata import Post_Metadata

warnings.filterwarnings('ignore', category=DeprecationWarning)
logging.getLogger('tensorflow').setLevel(logging.ERROR)
face_vector_store = IVF.FaceVectorStore("sandbox/face_vector_store.index")
while True:

    url = input("Enter the URL of the image to search for: ")
    if url == "exit":
        break
    else:

        frames = Face_Harvester.Harveste_URL(url)
        frame_count = 0
        face_count = 0
        for frame in frames:
            frame_count += 1
            for face in frame:
                face_count += 1
                embedding = Digital_Identity.get_face_embedding(face)
                results = face_vector_store.search_face(embedding)
                for result in results:
                    if result["score"] > 0.5:   
                        print(f"Found {result['face_id']} with score {result['score']}")

        print(f"Found {face_count} faces in {frame_count} frames")