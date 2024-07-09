from pymongo import MongoClient
from ..core.config import settings



connect = MongoClient(f"mongodb+srv://{settings.DBUSERNAME}:{settings.DBPASSWORD}@cluster0.bs2qfsl.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")

def connect_to_mongodb():
    try:
        if connect:
            connect[settings.DBNAME]
            print(f"Connection with MongoDB {settings.DBNAME} successfully!")
            return connect
        else:
            print(f"Error when try to connect with MongoDB: {e}")
            return None
    except Exception as e:
        print(f"Error when try to connect with MongoDB: {e}")
        return None

db = connect[settings.DBNAME]
users_collection = db['users']

async def connect_db():
    """Connect to MongoDB"""
    global db_client
    db_client = connect_to_mongodb()
    
async def close_db():
    """Close MongoDB"""
    db_client.close()
    
def get_collection_client(table: str):
    return db_client[table]
    
