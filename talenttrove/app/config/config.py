from pathlib import Path

# from base import load_env
# from dotenv import load_dotenv

ROOT_DIR = Path(__file__).parent.parent
# print(ROOT_DIR)
# load_dotenv(ROOT_DIR.joinpath(".env"))
settings = {
    "DB_PATH": str(ROOT_DIR.joinpath("db/talenttrove.db")),
    "Track_PATH": str(ROOT_DIR.joinpath("../data/dummy_data/applications.csv")),
    "Track_Date_PATH": str(ROOT_DIR.joinpath("../data/track.csv")),
    "VECTORDB_PATH": str(ROOT_DIR.joinpath("../data/jd_vectorDB")),
}
