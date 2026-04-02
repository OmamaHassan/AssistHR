def get_retriever(k=4, score_threshold=0.3):
    from embedding import similarity_search

    class PGVectorRetriever:
        def __init__(self, k=4):
            self.k = k

        def invoke(self, query: str):
            return similarity_search(query, k=self.k)

    return PGVectorRetriever(k=k)