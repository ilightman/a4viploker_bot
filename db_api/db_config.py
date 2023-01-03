import os

from dotenv import load_dotenv

from db_api.deta_db_class import DetaDB

# Key Name
# 2zrfb
# Key Description
# Project Key: 2zrfb
# Project Key
# a0ok0t1o_ud5Yx2qaAkQaGFxmp2mwVwsik6KmxdtL
load_dotenv()

PROJECT_KEY = os.getenv('PROJECT_KEY')
PROJECT_ID = os.getenv('PROJECT_ID')
db = DetaDB(project_key=PROJECT_KEY, project_id=PROJECT_ID)

# db._init()
