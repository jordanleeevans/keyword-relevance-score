# README

This tool aims to decide a keywords relevance to a particular text based on a wider corpus. In the context of a website, this tool will quantify how relevant a keyword is to a particular page based on the content of the entire website. This tool is useful for SEO purposes, as it can help you decide which keywords to target for a particular page. This tool is also useful for content writers, as it can help you decide which keywords to include in your content.

The `Queries` enum has been redacted of any sensitive information. This means that the tool will not work out of the box. You will need to add your own queries to the `Queries` enum. The queries are used to retrieve the content of the website, keywords and other information that is required to calculate the relevance of a keyword to a particular page.

# Dependencies
- Python 3.6+
- MySQLdb
- argparse
- dsnparse