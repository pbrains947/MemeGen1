class QuoteModel:
    def __init__(self, body: str, author: str):
        """
        Initializes a QuoteModel object with the given body and author.

        Args:
            body (str): The quote text.
            author (str): The author of the quote.
        """
        self.body = body
        self.author = author

    def __str__(self):
        """
        Returns a formatted string representation of the quote.
        """
        return f'"{self.body}" - {self.author}'