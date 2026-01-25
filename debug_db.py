from pymongo import MongoClient
import os
from dotenv import load_dotenv
load_dotenv()
CLUSTER_HOST = "cluster0.bdvqb9v.mongodb.net/?appName=Cluster0"

db_username = os.getenv("db_username")
db_password = os.getenv("db_password")

uri = f"mongodb+srv://{db_username}:{db_password}@{CLUSTER_HOST}"

print("Connecting to MongoDB...")
print(uri)
client = MongoClient(uri, serverSelectionTimeoutMS=5000)
db = client["rag_db"]
try:
    client.admin.command("ping")
    print("✅ MongoDB CONNECTED")
    print("Collections:", db.list_collection_names())

except Exception as e:
    print("❌ MongoDB CONNECTION FAILED:", e)
