import os

from dotenv import load_dotenv

from db_api.deta_db_class import DetaDB

load_dotenv()

PROJECT_KEY = os.getenv('PROJECT_KEY')
PROJECT_ID = os.getenv('PROJECT_ID')
db = DetaDB(project_key=PROJECT_KEY, project_id=PROJECT_ID)

# db._init()
