from io import IO
from src.core.io.dataset_reader import read_posts_from_csv
def learn_service(csv_file: IO[str]) -> None:
    posts = read_posts_from_csv(csv_file)
    #need to ingest_post for each post
    pass

