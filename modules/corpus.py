from collections import namedtuple
from MySQLdb.connections import Connection
from queries import Query

class Corpus:
    
    """ This class returns a generator of
    namedtuples with the following fields: path_id, document.
    The path_id is the unique identifier for the document and
    the document is the webpage content pulled from page_content.
    """

    def __init__(self, connection:Connection):
        self.connection = connection
        self.path_ids = self._get_path_ids()
        print("Pulled {} documents from page_content".format(len(self)))

    def __iter__(self):
        return self.generator()

    def __next__(self):
        if self.generator:
            return self.generator.next()
        raise StopIteration

    def __len__(self):
        with self.connection.cursor() as cursor:
            cursor.execute(Query.COUNT_DOCUMENTS)
            return cursor.fetchone()[0]

    def __str__(self):
        return "Corpus with {} documents".format(len(self))

    def __repr__(self):
        return "Corpus(connection={})".format(self.connection)

    def generator(self):
        """Returns a generator of records from the database.
        This utilises generator exhaustion to return all 
        records iteratively."""
        with self.connection.cursor() as cursor:
            cursor.execute(Query.ALL_DOCUMENTS)
            records = cursor.fetchone()
            while records:
                corpus = namedtuple('Corpus', ['path_id', 'document'])
                yield corpus(*records)
                records = cursor.fetchone()

    def _get_path_ids(self):
        """Returns a list of path_ids"""
        with self.connection.cursor() as cursor:
            cursor.execute(Query.PATH_IDS)
            return [record[0] for record in cursor.fetchall()]
