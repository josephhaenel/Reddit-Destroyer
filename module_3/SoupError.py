# Custom exception to handle scenarios where BeautifulSoup object retrieval fails.
class SoupObjectError(Exception):
    def __init__(self, message="Soup Object could not be retrieved"):
        super().__init__(message)