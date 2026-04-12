from src.core.entities.SocialProfile import SocialProfile
from src.core.io.files_loader import load_image_or_video
from src.core.io.leedspoting_api import get_profiles_from_api, get_profiles_count_from_api
from src.core.io.url_loader import download_to_temp_file
from src.core.services.harvesting_service import harvest_faces_from_frames
import numpy as np
from src.core.services.embedding_service import compute_similarity
from src.app.config import FACE_CONFIDENCE_THRESHOLD
from src.core.services.face_detection_service import IFaceDetector
from src.core.services.embedding_service import IEmbeddingModel


def search_api(
    target_first_name: str,
    target_last_name: str,
    target_frames_rgb: np.ndarray,
    detector: IFaceDetector,
    embedding_model: IEmbeddingModel,
    similarity_threshold: float = FACE_CONFIDENCE_THRESHOLD,
) -> list[SocialProfile]:
    if get_profiles_count_from_api(target_first_name, target_last_name) == 0:
        return [] #no profiles found
    
    profiles = get_profiles_from_api(target_first_name, target_last_name)

    #compute all the embeddings for all the profiles
    all_embeddings = []
    embeddings_to_profile = {}

    for profile in profiles:

        media_links = profile.get_all_images_links()
        for media_link in media_links:
            file = download_to_temp_file(media_link, "data/downloads")
            frames = load_image_or_video(file)
            cropped_faces = harvest_faces_from_frames(frames, detector)
            if len(cropped_faces) == 0:
                continue
            for cf in cropped_faces:
                embedding = embedding_model.compute_embedding(embedding_model.preprocess(cf))
                all_embeddings.append(embedding)
                embeddings_to_profile[embedding] = profile


    #compute the target embedding
    target_embeddings = []

    for frame in target_frames_rgb:
        cropped_faces = harvest_faces_from_frames(frame, detector)
        if len(cropped_faces) == 0:
            continue
        for cf in cropped_faces:
            embedding = embedding_model.compute_embedding(embedding_model.preprocess(cf))
            target_embeddings.append(embedding)


    #SEARCH METHOD:
    #we create a list of dictionaries with the profile id and the similarity score
    # * we know that search is slow but we prefer it because it is simple and easy to understand
    #result = {profile: SocialProfile: similarity_score: float}
    results = {}
    for target_embedding in target_embeddings:
        for profile_embedding in all_embeddings:
            similarity_score = compute_similarity(target_embedding , profile_embedding)
            if similarity_score >= similarity_threshold:
                if embeddings_to_profile[profile_embedding] not in results:
                    results[embeddings_to_profile[profile_embedding]] = similarity_score
                else:
                    results[embeddings_to_profile[profile_embedding]] = max(results[embeddings_to_profile[profile_embedding]], similarity_score)
    #--------------------------------------------------------

