from typing import List, Dict, Tuple
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from scipy.sparse import csr_matrix
from corpus import Corpus

class TfidfKeywordScorer:

    """ Given a corpus of text documents and query, this class
    will calculate the tf-idf for each term in each document.
    The input query will be scored against each document in the
    corpus.
    """

    def __init__(self, corpus:Corpus, queries:Dict[str, str]):
        self.corpus = corpus
        self.queries = queries.values()
        self.scored_queries = []
        self.ranking_paths = []

        self._vectorizer = TfidfVectorizer()
        document_term_matrix = self._vectorizer.fit_transform((item.document for item in corpus))

        for keyword_market_id, keyword in queries.items():
            print(f"Scoring `{keyword}` against {len(corpus)} documents")
            top_ranking_paths = self._query_corpus(keyword, document_term_matrix)
            total_query_score = sum((score for _, score in top_ranking_paths))
            self.scored_queries.append(
                (keyword_market_id, total_query_score)
            )
            for item in top_ranking_paths:
                self.ranking_paths.append(
                    (keyword_market_id, *item)
                )

    def __repr__(self) -> str:
        return f"TermFrequencyInverseDocumentFrequency({self.corpus}, {self.queries})"

    def _query_corpus(self, query:str, document_term_matrix:csr_matrix, top_n:int=10,) -> List[Tuple[int, float]]:

        """Calculate the cosine similarity between the query and each document in the corpus.
        Return the top_n documents with the highest similarity scores."""

        # Transform the query into a vector
        query_vector = self._vectorizer.transform([query])
        # Calculate the cosine similarity between the query and each document
        similarities = cosine_similarity(query_vector, document_term_matrix).flatten()
        # Sort the similarities in descending order
        sorted_similarities = sorted(enumerate(similarities), key=lambda x: x[1], reverse=True)
        # Slice the top n results
        top_similarities = sorted_similarities[:top_n]
        # Create a list to store the top ranking paths, and their relevance scores
        top_ranking_paths = []
        for i, similarity in top_similarities:
            # Find the path_id for each similarity
            for j, path_id in enumerate(self.corpus.path_ids):
                # if indexes of path_id and similarity are the same, append path_id to top_ranking_paths
                if i == j:
                    top_ranking_paths.append((path_id, similarity))
        return top_ranking_paths
