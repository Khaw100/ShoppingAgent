from pymongo import MongoClient
from .embedding import get_embedding
import os
from urllib.parse import quote_plus
import certifi

from dotenv import load_dotenv
load_dotenv()


CLUSTER_HOST = "cluster0.bdvqb9v.mongodb.net/?appName=Cluster0"

db_username = os.getenv('db_username')
db_password = os.getenv('db_password')

CONNECTION_STRING = f"mongodb+srv://{db_username}:{db_password}@{CLUSTER_HOST}"

# Connect to your MongoDB deployment
client = MongoClient(CONNECTION_STRING,
                    tls=True,
                    tlsCAFile=certifi.where(),
                    serverSelectionTimeoutMS=5000)
collection = client["rag_db"]["rag"]

# Define a function to run vector search queries
def get_query_results(query):
  """Gets results from a vector search query."""

  query_embedding = get_embedding(query)
  print("QUERY EMBEDDING:", len(query_embedding))
  pipeline = [
      {
            "$vectorSearch": {
              "index": "vector_index",
              "queryVector": query_embedding,
              "path": "embedding",
              "exact": True,
              "numCandidates": 100, 
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
    results = collection.find({"product_id": product_id})
    
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