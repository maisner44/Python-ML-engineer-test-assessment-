import os
import faiss
import numpy as np
import pandas as pd
import openai
from dotenv import load_dotenv

load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")
if not openai.api_key:
    raise ValueError("No OpenAI API key found. Please set it in your .env file.")

def get_embedding(text: str, model: str = "text-embedding-ada-002") -> np.ndarray:
    try:
        response = openai.Embedding.create(input=[text], model=model)
        embedding = response["data"][0]["embedding"]
        return np.array(embedding, dtype="float32")
    except Exception as e:
        print("Error during embedding generation:", e)
        return np.zeros(1536, dtype="float32")  # assuming embedding dim is 1536

class FAISSVectorDB:
    def __init__(self, embedding_dim: int = 1536):
        self.embedding_dim = embedding_dim
        self.index = faiss.IndexFlatL2(embedding_dim)
        self.metadata = []  # List to hold corresponding cocktail/user memory data

    def add_items(self, texts, metadatas):
        embeddings = [get_embedding(text) for text in texts]
        embeddings = np.vstack(embeddings)
        self.index.add(embeddings)
        self.metadata.extend(metadatas)

    # Compute embedding for the query, search the index, and return the top-k metadata results.
    def search(self, query: str, k: int = 5):
        query_embedding = get_embedding(query).reshape(1, -1)
        distances, indices = self.index.search(query_embedding, k)
        results = []
        for i in indices[0]:
            if i < len(self.metadata):
                results.append(self.metadata[i])
        return results

    def add_single_item(self, text: str, metadata):
        embedding = get_embedding(text).reshape(1, -1)
        self.index.add(embedding)
        self.metadata.append(metadata)

# Load the cocktail dataset from CSV, preprocess it, and index cocktail details.
def build_cocktail_index(csv_path: str) -> FAISSVectorDB:
    df = pd.read_csv(csv_path)
    texts = []
    metadatas = []
    for _, row in df.iterrows():
        text = f"{row['name']}: {row['ingredients']}"
        texts.append(text)
        metadatas.append({"name": row["name"], "ingredients": row["ingredients"]})

    vector_db = FAISSVectorDB(embedding_dim=1536)
    vector_db.add_items(texts, metadatas)
    print(f"Indexed {len(texts)} cocktails.")
    return vector_db

cocktail_vector_db = build_cocktail_index("data/final_cocktails.csv")

#Retrieve relevant cocktail details from the FAISS and format them as context.
def get_context_for_query(query: str, k: int = 5) -> str:
    results = cocktail_vector_db.search(query, k=k)
    context_lines = []
    for res in results:
        if "name" in res and "ingredients" in res:
            line = f"{res['name']}: {res['ingredients']}"
        elif "type" in res and res["type"] == "user_memory" and "text" in res:
            line = f"User memory: {res['text']}"
        else:
            line = str(res)
        context_lines.append(line)
    context = "\n".join(context_lines)
    return context

def store_user_memory(text: str):
    metadata = {"type": "user_memory", "text": text}
    cocktail_vector_db.add_single_item(text, metadata)
    print("User memory stored.")
