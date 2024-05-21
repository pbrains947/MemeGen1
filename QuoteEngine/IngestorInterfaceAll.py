from .QuoteModel import QuoteModel
from typing import List
import subprocess
import random
import os
from docx import Document
import pandas as pd
from abc import ABC, abstractmethod


class IngestorInterface(ABC):
    """
    Abstract base class for actual Ingestr classes for diffent types of files.

    Each child class will actually ingest the files and return desired data.
    """

    allowed_extensions = []

    @classmethod
    def can_ingest(cls, path) -> bool:
        """
        Check if the given file can be ingested by this strategy.
        """
        ext = path.split('.')[-1]
        return ext in cls.allowed_extensions
        pass

    @classmethod
    @abstractmethod
    def parse(cls, path: str) -> List[QuoteModel]:
        """
        Parse the given file and return a list of QuoteModel objects.
        """
        pass


class CSVIngestor(IngestorInterface):
    """Helper module to read CSV file."""
    @classmethod
    def can_ingest(cls, path: str) -> bool:
        return path.lower().endswith('.csv')
    
    @classmethod
    def parse(cls, path: str) -> List[QuoteModel]:
        """
        Parses a CSV file and returns a list of QuoteModel objects.
        Parameters:
        - path (str): The file path of the CSV file to parse.

        Returns:
        - List[QuoteModel]: A list of QuoteModel objects representing the quotes extracted from the CSV file.

        Raises:
        - ValueError: If there is an error parsing the CSV file.
        """	
        try:
            df = pd.read_csv(path, header=0)

            quotes = []
            
            for _, row in df.iterrows():
                quotes.append(QuoteModel(row['body'], row['author']))
            return quotes
        except Exception as e:
            raise ValueError(f"Error parsing CSV file: {e}")    


class DocxIngestor(IngestorInterface):
    """Helper module to read DOCX file."""
    @classmethod
    def can_ingest(cls, path: str) -> bool:
        return path.lower().endswith('.docx')

    @classmethod
    def parse(cls, path: str) -> List[QuoteModel]:
        """
        Parses a DOCX file and returns a list of QuoteModel objects.

        Parameters:
        - path (str): The file path of the DOCX file to parse.

        Returns:
        - List[QuoteModel]: A list of QuoteModel objects representing the quotes extracted from the DOCX file.

        Raises:
        - ValueError: If there is an error parsing the DOCX file.
        """	
        try:
            doc = Document(path)

            quotes = []

            for para in doc.paragraphs:
                if para.text.strip():
                    # Assuming that each non-empty paragraph is a quote
                    quote_text = para.text.strip()
                    # Split the quote into body and author (assuming format: "Quote - Author")
                    if "-" in quote_text:
                        body, author = map(str.strip, quote_text.split("-", 1))
                        quotes.append(QuoteModel(body=body, author=author))
            return quotes
        except Exception as e:
            raise ValueError(f"Error parsing DOCX file: {e}")
        

class PDFIngestor(IngestorInterface):
    """Helper module to read PDF file."""
    @classmethod
    def can_ingest(cls, path: str) -> bool:
        return path.lower().endswith('.pdf')

    @classmethod
    def parse(cls, path: str) -> List[QuoteModel]:
        """
        Parses a PDF file and returns a list of QuoteModel objects.

        Parameters:
        - path (str): The file path of the PDF file to parse.

        Returns:
        - List[QuoteModel]: A list of QuoteModel objects representing the quotes extracted from the PDF file.

        Raises:
        - ValueError: If there is an error parsing the PDF file.
        """	
        try:
            # Convert PDF to text using pdftotext CLI utility
            temp_text_file = "temp_quotes.txt"        
            subprocess.call(['pdftotext', '-layout', path, temp_text_file]) 

            # Read the converted text file
            lines = open(temp_text_file, "r", encoding="utf-8")

            quotes = []

            for line in lines:
                line = line.strip('\n\r').strip()  # Split the line into segments based on the delimiter                          

            # Split the quote into body and author based on the format: "Quote - Author"
                if len(line) > 0:
                    parsed = line.split('-')
                    quotes.append(QuoteModel(parsed[0].strip().strip('"'), parsed[1].strip()))

            lines.close()
            # Clean up temporary text file
            os.remove(temp_text_file)
            return quotes
        except Exception as e:
            raise ValueError(f"Error parsing PDF file: {e}")


class TXTIngestor(IngestorInterface):
    """Helper module to read TXT file."""
    @classmethod
    def can_ingest(cls, path: str) -> bool:
        return path.lower().endswith('.txt')

    @classmethod
    def parse(cls, path: str) -> List[QuoteModel]:
        """
        Parses the given file and returns a list of QuoteModel objects.

        Args:
        path (str): The path to the file to be parsed.

        Returns:
        List[QuoteModel]: A list of QuoteModel objects parsed from the file.
        """	
        quotes = []
        with open(path, 'r') as file:
            for line in file:
                body = line.split("-")[0].strip().strip('"')
                author = line.split("-")[1].strip()
                new_quote = QuoteModel(body, author)
                quotes.append(new_quote)
        return quotes
    

class Ingestor(IngestorInterface):
    """
    Class to handle parsing different file types and returning a list of QuoteModel objects.

    Inherits from IngestorInterface.

    Methods:
        parse(cls, path: str) -> List[QuoteModel]: Parses the given file and returns a list of QuoteModel objects.

    Raises:
        ValueError: If no suitable ingestor is found for the file.
    """
    @classmethod
    def parse(cls, path: str) -> List[QuoteModel]:
        ingestors = [CSVIngestor, DocxIngestor, PDFIngestor, TXTIngestor]
        for ingestor in ingestors:
            if ingestor.can_ingest(path):
                return ingestor.parse(path)
        raise ValueError(f"No suitable ingestor found for file: {path}")