import random
import os
import requests
from flask import Flask, render_template, abort, request
from QuoteEngine.IngestorInterfaceAll import Ingestor
from MemeGenerator.MemeEngine import MemeEngine

app = Flask(__name__)
meme = MemeEngine('./static')


def setup():
    """Load all resources."""
    quote_files = ['./_data/DogQuotes/DogQuotesTXT.txt',
                   './_data/DogQuotes/DogQuotesDOCX.docx',
                   './_data/DogQuotes/DogQuotesPDF.pdf',
                   './_data/DogQuotes/DogQuotesCSV.csv']

    all_quotes = []
        
# Iterate over each quote file and parse its content
    for file_path in quote_files:
        quotes = Ingestor.parse(file_path)
        all_quotes.extend(quotes)

# Print the parsed quotes (for demonstration purposes)
    for quote in all_quotes:
        print(f"Author: {quote.author}, Text: {quote.body}")

        quotes = None        

    images_path = "./_data/photos/dog/"
    
# Initialize an empty list to store image filenames
    image_files = []

# Iterate over files in the directory
    for filename in os.listdir(images_path):
        if filename.lower().endswith(('.jpg', '.jpeg', '.png', '.gif')):
        # Add image filenames to the list
            image_files.append(filename)

# Print the list of image filenames
    print("Image files found:")
    for image_file in image_files:
        print(image_file)
#        imgs = None
        imgs = []
    return quotes, imgs

quotes, imgs = setup()

@app.route('/')
def meme_rand():
    """Generate a random meme."""
# Select a random image filename
    try:
        random_image = random.choice(imgs)
    except IndexError:
        pass

# Select a random quote
    random_quote = random.choice(quotes)
    
    print(f"Random image: {random_image}")
    print(f"Random quote: {random_quote.author} - {random_quote.text}")
    
    img = None
    quote = None
    
    path = meme.make_meme(img, quote.body, quote.author)
    return render_template('meme.html', path=path)


@app.route('/create', methods=['GET'])
def meme_form():
    """User input for meme information."""
    return render_template('meme_form.html')


@app.route('/create', methods=['POST'])
def meme_post():
    """ Create a user defined meme """

    # Get form parameters
    image_url = request.form.get('image_url')
    body = request.form.get('body')
    author = request.form.get('author')

    # Save the image from the image_url to a temporary local file
    temp_image_path = './temp_image.jpg'
    try:
        response = requests.get(image_url, stream=True)
        if response.status_code == 200:
            with open(temp_image_path, 'wb') as temp_image_file:
                for chunk in response.iter_content(chunk_size=1024):
                    temp_image_file.write(chunk)
        else:
            return "Error: Unable to download image from the provided URL."
    except Exception as e:
        return f"Error: {str(e)}"

    # Generate a meme using the temp image file and form parameters
    path = meme.make_meme(temp_image_path, body, author)

    # Remove the temporary saved image
    os.remove(temp_image_path)
    path = None
    return render_template('meme.html', path=path)


if __name__ == "__main__":
    app.run()
