from pymongo import MongoClient
from .embedding import get_embedding
import os
from datetime import datetime
import uuid
CLUSTER_HOST = "cluster0.bdvqb9v.mongodb.net/?appName=Cluster0"

db_username = os.getenv('db_username')
db_password = os.getenv('db_password')

CONNECTION_STRING = f"mongodb+srv://{db_username}:{db_password}@{CLUSTER_HOST}"

# Connect to your MongoDB deployment
client = MongoClient(CONNECTION_STRING)
collection = client["rag_db"]["rag"]

# Add new table
db = client["rag_db"]
trx_collection = db["transactions"]

# Define a function to run vector search queries
def get_query_results(query):
  """Gets results from a vector search query."""

  query_embedding = get_embedding(query)
  print("QUERY EMBEDDING:", query_embedding)
  pipeline = [
      {
            "$vectorSearch": {
              "index": "vector_index",
              "queryVector": query_embedding,
              "path": "embedding",
              "exact": True,
              "limit": 5
            }
      }, {
            "$project": {
              "_id": 0,
              "text": 1
         }
      }
  ]

  results = collection.aggregate(pipeline)

  products = []
  for product in results:
    products.append(product['text'])
  return products

def get_item_by_product_id(product_id):
    results = collection.find({"product_id": product_id},
                              {"_id": 0, "name": 1, "price": 1, "product_id": 1})
    
    products = []
    for product in results:
        products.append(product['text'])
    return products

def get_item_by_product_by_brand(brand):
    results = collection.find({"brand": brand})
    
    products = []
    for product in results:
        products.append(product['text'])
    return products

def get_item_by_material(material: str):
    results = collection.find(
        {"material": {"$regex": material, "$options": "i"}}
    )

    products = []
    for product in results:
        products.append(product.get("text"))
    return products

def create_transaction(user_id: str, product: dict):
    trx = {
        "transaction_id": str(uuid.uuid4()),
        "user_id": user_id,
        "product_id": product["product_id"],
        "product_name": product["name"],
        "price": product["price"],
        "currency": "USD",
        "created_at": datetime.utcnow()
    }
    trx_collection.insert_one(trx)
    return trx

def get_user_transactions(user_id: str):
    results = trx_collection.find(
        {"user_id": user_id},
        {"_id": 0}
    ).sort("created_at", -1)

    return list(results)