from enum import Enum

class Query(str, Enum):

    """Enum for SQL querys"""

    COUNT_DOCUMENTS = """
                    SELECT
                        COUNT(*) 
                    FROM page_content a
                    JOIN path b on b.id = a.path_id
                    WHERE a.has_content = 1
                    AND b.updated BETWEEN DATE_ADD(NOW(), INTERVAL -35 DAY) AND NOW();"""

    ALL_DOCUMENTS = """
                    SELECT
                        a.path_id as `path_id`,
                        a.body as `document`
                    FROM page_content a
                    JOIN path b on b.id = a.path_id
                    WHERE a.has_content = 1
                    AND b.updated BETWEEN DATE_ADD(NOW(), INTERVAL -35 DAY) AND NOW()
                    ORDER BY a.id;"""

    PATH_IDS = """SELECT DISTINCT(a.path_id)
                        FROM page_content a
                        JOIN path b on b.id = a.path_id
                        WHERE a.has_content = 1
                        AND b.updated BETWEEN DATE_ADD(NOW(), INTERVAL -35 DAY) AND NOW()
                        ORDER BY a.id"""

    PENDING_KEYWORDS = """SELECT 
                                mkt.id as `keyword_market_id`,
                                kwd.keyword
                            FROM semrush_volume kwr 
                            JOIN market_keyword mkt ON mkt.id = kwr.keyword_market_id 
                            JOIN keyword kwd ON kwd.id = mkt.keyword_id;"""

    EXISTING_KEYWORDS = """
                        SELECT
                        mkt.id as `keyword_market_id`,
                        kwd.keyword
                        FROM market_keyword mkt
                        JOIN keyword kwd ON kwd.id = mkt.keyword_id
                        WHERE mkt.active = 1;"""

    INSERT_RELEVANCE_SCORE = """
                                INSERT INTO keyword_relevance (keyword_relevance_type, keyword_market_id, created, updated, relevance_score)
                                VALUES (%s, %s, NOW(), NOW(), %s)
                                ON DUPLICATE KEY UPDATE
                                    relevance_score = VALUES(relevance_score),
                                    keyword_relevance_type = VALUES(keyword_relevance_type),
                                    updated = VALUES(updated);"""
    
    INSERT_RELEVANCE_PATH = """
                                INSERT INTO keyword_relevance_path (keyword_market_id, path_id, path_relevance_score, created, updated)
                                VALUES (%s, %s, %s, NOW(), NOW())
                                ON DUPLICATE KEY UPDATE
                                    path_relevance_score = VALUES(path_relevance_score),
                                    updated = VALUES(updated);"""
    def __str__(self) -> str:
        return self.value
