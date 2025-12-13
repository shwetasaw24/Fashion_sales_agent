import os
import logging

try:
    from pymongo import MongoClient
except ImportError:
    MongoClient = None
    logging.getLogger(__name__).warning("pymongo not installed; MongoDB features disabled")

logger = logging.getLogger(__name__)

MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")
MONGO_DB = os.getenv("MONGO_DB", "fashion_agent_db")


def _init_mongo():
    if MongoClient is None:
        return None, None
    try:
        client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=5000)
        # verify connection
        client.server_info()
        db = client[MONGO_DB]
        logger.info("✅ Connected to MongoDB at %s", MONGO_URI)
        return client, db
    except Exception as e:
        logger.warning("⚠️ MongoDB not available: %s", e)
        return None, None


client, db = _init_mongo()


def get_db():
    return db


def get_collection(name: str):
    if db is None:
        return None
    return db[name]
