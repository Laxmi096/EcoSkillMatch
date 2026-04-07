from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def recommend(user_skills, items):
    documents = [user_skills] + [item["skills"] for item in items]

    vectorizer = TfidfVectorizer(stop_words="english")
    tfidf_matrix = vectorizer.fit_transform(documents)

    similarity_scores = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:]).flatten()

    results = []
    for idx, item in enumerate(items):
        new_item = item.copy()
        new_item["match_percent"] = int(similarity_scores[idx] * 100)
        results.append(new_item)

    return sorted(results, key=lambda x: x["match_percent"], reverse=True)
