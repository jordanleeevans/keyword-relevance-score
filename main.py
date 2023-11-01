import argparse, MySQLdb, dsnparse
from tf_idf import TfidfKeywordScorer
from modules.keywords import Keywords, RelevanceType
from modules.corpus import Corpus

parser = argparse.ArgumentParser(description='Gets mandatory connection string') 
parser.add_argument('--connection', dest="connection", required=True, 
                    help='Connection string to database.')
parser.add_argument('--existing', dest="existing", action='store_true', default=False, 
                    help='Flag to indicate if existing keywords should be used.')
args = parser.parse_args()

# Get credentials from connection string
connection = dsnparse.parse(args.connection)
host = connection.host
user = connection.username
password = connection.password
db = connection.paths[0]
port = connection.port
# Instantiate connection to database
connection = MySQLdb.connect(host=host, user=user, passwd=password, db=db, port=port)

def main(existing_keywords):

    """Main function that runs the tf-idf algorithm on
    pending keywords inside keyword_relevance against
    all scraped pages within page_content."""

    # Get all documents from database
    corpus = Corpus(connection)
    # Get all keywords pending review inside database
    keywords = Keywords(connection, RelevanceType.GENERIC, existing_keywords)
    # Get tf-idf scores for each keyword
    query_results = TfidfKeywordScorer(corpus, keywords.get_keywords())
    # Insert tf-idf scores into database
    keywords.insert_kwr_relevance_score(query_results.scored_queries)
    keywords.insert_kwr_relevance_path(query_results.ranking_paths)

if __name__ == "__main__":
    main(args.existing)

