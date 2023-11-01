from typing import List
from MySQLdb.connections import Connection
from data.queries import Query
from enum import IntEnum

class RelevanceType(IntEnum):
    """Enum class that defines the relevance type"""
    GENERIC = 0
    BRAND = 1
    COMPETITOR = 2

class Keywords:

    """Holds a list of keywords that are pending review, alongside
    their keyword_market_id, and the relevance type (generic, brand, competitor).
    This class is also responsible for inserting scored keywords into 
    keyword_relevance, and relevance_score_path."""

    def __init__(self, connection:Connection, relevance_type:RelevanceType, existing_keywords:bool=False):
        self.connection = connection
        self.relevance_type =  relevance_type
        self.existing_keywords = existing_keywords

        print("Processing keyword type:", relevance_type.name)
        print("Pulled {} keywords from keyword_relevance".format(len(self)))

    def __len__(self) -> int:
        self.get_keywords()
        return len(self.keywords)

    def __repr__(self) -> str:
        return f"Keywords({self.connection}, {self.keywords})"

    def get_keywords(self):

        """Queries all keywords inside semrush_volume (post the SEMRUSH pull)
        and returns a list of them. We want to do it after this stage because we can 
        use the relevancy scoring in the filtering pre inserting into keyword."""

        query = Query.EXISTING_KEYWORDS if self.existing_keywords else Query.PENDING_KEYWORDS

        with self.connection.cursor() as cursor:
            cursor.execute(query)
            data = cursor.fetchall()

        # Create hashmap for both keyword_market_id and keyword
        self.keyword_map = {row[0]:row[1] for row in data}
        self.keywords = [row[1] for row in data]
        return self.keyword_map # Have to return a hashmap as keywords are not unique, but keyword_market_ids are

    def insert_kwr_relevance_score(self, keyword_relevance_score:List[tuple]):
        """Inserts a list of tuples (relevance_type, keyword_market_id, total_relevance_score) into relevance_score"""
        values = [(self.relevance_type, keyword_market_id, score) for keyword_market_id, score in keyword_relevance_score]
        with self.connection.cursor() as cursor:
            cursor.executemany(Query.INSERT_RELEVANCE_SCORE, values)
            self.connection.commit()

    def insert_kwr_relevance_path(self, keyword_path:List[tuple]):
        """Inserts a list of tuples (keyword_market_id, path, path_relevance_score) into relevance_score_path"""
        with self.connection.cursor() as cursor:
            cursor.executemany(Query.INSERT_RELEVANCE_PATH, keyword_path)
            self.connection.commit()
