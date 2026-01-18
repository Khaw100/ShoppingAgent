import openai
from tqdm import tqdm
import os


from sentence_transformers import SentenceTransformer

model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")



def get_embedding(text: str):
  if not text:
      return [0.0] * 384  # MiniLM embedding size

  embedding = model.encode(
      text,
      normalize_embeddings=True  # strongly recommended for cosine similarity
  )
  return embedding.tolist()
