from pymongo import MongoClient
import numpy as np
import os

# ======================
# CONFIG
# ======================

from dotenv import load_dotenv
load_dotenv()


CLUSTER_HOST = "cluster0.bdvqb9v.mongodb.net/?appName=Cluster0"

db_username = os.getenv('db_username')
db_password = os.getenv('db_password')

CONNECTION_STRING = f"mongodb+srv://{db_username}:{db_password}@{CLUSTER_HOST}"

DB_NAME = "rag_db"
COLLECTION_NAME = "rag"
VECTOR_INDEX_NAME = "_id_"   # samakan dgn index Atlas kamu
VECTOR_FIELD = "embedding"

# ======================
# CONNECT
# ======================
print("🔌 Connecting to MongoDB...")
client = MongoClient(CONNECTION_STRING)
collection = client[DB_NAME][COLLECTION_NAME]
print("✅ Connected")

# ======================
# GET 1 REAL VECTOR
# ======================
doc = collection.find_one(
    {VECTOR_FIELD: {"$exists": True}},
    {VECTOR_FIELD: 1}
)

if not doc:
    raise RuntimeError("❌ No document with embedding found")

query_vector = doc[VECTOR_FIELD]

# ======================
# BASIC CHECK
# ======================
dim = len(query_vector)
norm = np.linalg.norm(query_vector)

print(f"📐 Vector dim  : {dim}")
print(f"📏 Vector norm : {norm}")

if dim != 384:
    raise RuntimeError("❌ Vector dim NOT 384")

if norm == 0:
    raise RuntimeError("❌ Zero vector detected")

print("✅ Vector looks healthy")

# ======================
# VECTOR SEARCH TEST
# ======================
pipeline = [
    {
        "$vectorSearch": {
            "index": VECTOR_INDEX_NAME,
            "queryVector": query_vector,
            "path": VECTOR_FIELD,
            "numCandidates": 100,
            "limit": 3
        }
    }
]

print("🔍 Running vector search...")
results = list(collection.aggregate(pipeline))

print(f"✅ Vector search success, got {len(results)} result(s)")
for r in results:
    print(" - _id:", r["_id"])
