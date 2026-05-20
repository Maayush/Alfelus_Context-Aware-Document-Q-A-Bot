import numpy as np

stored_data = []


def clear_vector_store():

    global stored_data

    stored_data = []


def store_embeddings(embeddings, chunks, filename):

    global stored_data

    for embedding, chunk in zip(embeddings, chunks):

        stored_data.append({
            "embedding": embedding,
            "chunk": chunk,
            "filename": filename
        })

    print("TOTAL DOCUMENT CHUNKS:", len(stored_data))


def cosine_similarity(a, b):

    a = np.array(a)
    b = np.array(b)

    return np.dot(a, b) / (
        np.linalg.norm(a) * np.linalg.norm(b)
    )


def search_similar(query_embedding, top_k=8, threshold=0.25):

    global stored_data

    if len(stored_data) == 0:
        return []

    similarities = []

    for item in stored_data:

        similarity = cosine_similarity(
            query_embedding,
            item["embedding"]
        )

        confidence = round(
            float(similarity) * 100,
            2
        )

        similarities.append({
            "chunk": item["chunk"],
            "score": float(similarity),
            "confidence": confidence,
            "filename": item["filename"]
        })

    similarities = sorted(
        similarities,
        key=lambda x: x["score"],
        reverse=True
    )

    filtered_results = []

    for item in similarities:

        if item["score"] >= threshold:
            filtered_results.append(item)

    return filtered_results[:top_k]