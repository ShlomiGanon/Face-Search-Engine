from io import IO
from src.core.io.dataset_reader import read_posts_from_csv

#LEARN : (csv_file) -> add a faces to the database and ivf 
#SEARCH : (media_file) -> search for a face in the database and return the most similar faces
#* SEARCH_API : (first_name, last_name , media_file) -> search for a face in the database and return the most similar faces

#we need to redesign the all backend 

#link the frontend to the backend (to use the api)

def learn_service(csv_file: IO[str]) -> None:
    posts = read_posts_from_csv(csv_file)
    #need to ingest_post for each post
    pass

