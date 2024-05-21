from PIL import Image, ImageFont, ImageDraw
import random
import os
import argparse
import time

class MemeEngine:
    """
    Class to handle generating and saving memes.
    """
    def __init__(self, output_dir):
        """
        Initialize the MemeEngine object.

        Args:
            output_dir (str): The directory where the generated memes will be saved.
        """	
        self.output_dir = output_dir

    def generate_unique_filename(self):
        """
        Generate a unique filename for the meme.

        Returns:
            str: The unique filename for the meme.
        """	
        timestamp = int(time.time())  # Get current timestamp
        random_number = random.randint(1, 1000)  # Generate a random number
        unique_filename = f"meme_{timestamp}_{random_number}.jpg"
        return os.path.join(self.output_dir, unique_filename)
    
    def make_meme(self, img_path, text, author, width=500) -> str:  
        """
        Generate a meme by adding text to an image.

        Args:
            img_path (str): Path to the input image.
            text (str): Quote text to add to the image.
            author (str): Author of the quote.
            width (int, optional): Width of the output image. Defaults to 500.

        Returns:
            str: Path to the manipulated image.
        """    
        try:
            # Open the input image
            img = Image.open(img_path)        

            # Resize image
            img = img.resize((width, int(width * img.height / img.width)))

            # Create drawing context
            draw = ImageDraw.Draw(img)
                
            # Load font
            #font_size = 20                
            font_size = int(img.height / 20)
            font_path = "./_data/fonts/arial.ttf"
            font = ImageFont.truetype(font_path, font_size)       

            # Generate random location for text
            x = random.randint(0, int(img.width / 4))
            y = random.randint(0, int(img.height - font_size * 2))         
           
            # Add text and author to the image
            draw.text((x, y), f"{text} - {author}", fill="white", font=font)  

            # Save the image
            output_path = self.generate_unique_filename()
            img.save(output_path)
         
            return output_path
        except FileNotFoundError:
            return "Error: Invalid File Path."
        except PermissionError:
            return "Error: Permission denied to access the input image file."
        except Exception as e:
            return f"Error: {str(e)}"