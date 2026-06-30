from dotenv import load_dotenv
import os

load_dotenv()

URL = os.getenv("URL")
PRODUCT_IDS = os.getenv("PRODUCT_IDS").split(",")
DEPTH_PERCENTAGE = float(os.getenv("DEPTH_PERCENTAGE"))
GRAPH_UPDATE_INTERVAL = float(os.getenv("GRAPH_UPDATE_INTERVAL"))
LOCAL_HOST = os.getenv("LOCAL_HOST")
LOCAL_PORT = int(os.getenv("LOCAL_PORT"))