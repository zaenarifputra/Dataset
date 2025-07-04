# Content-Based Filtering
# Modul untuk merekomendasikan item berdasarkan deskripsi
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from app.preprocessing import cleanse

def recommend(query, dataset, keys=None):
    if keys is None:
        keys = ["deskripsi"]
    
    documents = []
    for item in dataset:
        combined = " ".join([str(item.get(k, "")) for k in keys])
        documents.append(cleanse(combined))

    query_clean = cleanse(query)

    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform(documents + [query_clean])
    scores = cosine_similarity(tfidf_matrix[-1], tfidf_matrix[:-1])[0]

    results = sorted(zip(scores, dataset), key=lambda x: x[0], reverse=True)
    return [item for score, item in results if score > 0.1]

