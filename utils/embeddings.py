from sentence_transformers import SentenceTransformer

model = SentenceTransformer("all-mpnet-base-v2")

def generate_embedding(text: str):
    return model.encode([text])[0].tolist()  # devuelve lista de floats
