#################################################
# Author:   Dan Dinh                            #
# Date:     2024-11-28                          #
# Exercise: 2 with Together AI                  #
# Question: 4 with document translation         #
#################################################

import os
from groq import Groq
from dotenv import load_dotenv
import fitz


# Load environment variables from .env file
load_dotenv()

# Get API key from environment variables
api_key = os.getenv('API_KEY')

# Function to extract text from a PDF
def extract_text_from_pdf(pdf_path):
    """
    Extract text from a PDF file and return it as a list of strings.
    """
    try:
        # Open the PDF file
        pdf_document = fitz.open(pdf_path)
        print(f"Number of pages: {pdf_document.page_count}")
        
        # Define a list to store the extracted text
        pdf_content = []
        
        # Extract text from each page
        for page_num in range(pdf_document.page_count):
            page = pdf_document[page_num]  # Get page
            text = page.get_text()  # Extract text
            pdf_content.append(text)
            print(f"Page {page_num + 1}:")
            print(text)
            if page_num > 5:
                break

        # for page in pdf_document:
        #     text = page.get_text()
        #     pdf_content.append(text)
        #     print(text)

        # Close the document
        pdf_document.close()
        
        return pdf_content
    except Exception as e:
        print(f"An error occurred: {e}")


def get_response(messages):
    """
    Get the response from the chat completion API.
    """
    # Create Groq client
    client = Groq(
        api_key=api_key,
    )

    # Create chat completion
    chat_completion = client.chat.completions.create(        
        messages=messages,
        model="llama3-8b-8192",
        max_tokens=8192,
        stream=True,
    )

    return_message = ""
    # Print response from chat completion
    for chunk in chat_completion:
        response = chunk.choices[0].delta.content or ""
        print(response, end="")
        return_message += response

    print("\n")
    return return_message

# Get user input for the file path
pdf_path = input("Enter the file path: ")

# Extract text from the PDF
pdf_content = extract_text_from_pdf(pdf_path)

# Define the prompt for the chat completion
initial_prompt = f"\
        You are a professional translator specializing in Vietnamese and domain knowledge of the provided document. Translate the provided text into Vietnamese while ensuring the following:\
1. Use only valid and accurate Vietnamese characters, avoiding any incorrect or non-Vietnamese symbols or characters.\
2. Ensure the translation accurately conveys the original meaning and context, focusing on clarity and professionalism.\
3. Correctly translate technical terms and context-specific language into Vietnamese to ensure they are understood by readers in the field.\
4. Avoid adding unrelated notes or comments; provide only the fully translated Vietnamese text.\
5. Pay close attention to grammar, syntax, and terminology to ensure the translation is coherent and error-free."

messages = []

# Initialize the messages array with the initial prompt
messages.extend([
    {"role": "user", "content": initial_prompt},
    {"role": "assistant", "content": "I am waiting for the document content."}
])

for text in pdf_content:
    # Add user question to messages array
    messages.append({"role": "user", "content": text})
    
    # Get response from the chat completion API
    return_message = get_response(messages)

    # Add response to messages array
    messages.append({"role": "assistant", "content": return_message})
