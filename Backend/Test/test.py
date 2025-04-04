# import pytesseract
# from pdf2image import convert_from_path
# import os

# def extract_text_from_pdf(pdf_path, language_code):
#     """Extracts text from a PDF and saves it as a text file in the 'Output' folder."""

#     # Create Output folder if not exists
#     os.makedirs("Output", exist_ok=True)

#     # Get PDF name (without extension)
#     pdf_name = os.path.splitext(os.path.basename(pdf_path))[0]

#     # page of PDF to an image
#     images = convert_from_path(pdf_path)

#     # Perform OCR
#     text = "\n".join([pytesseract.image_to_string(img, lang=language_code) for img in images])
#     # print(text)

#     # Save text file
#     output_file = f"Output/{pdf_name}_{language_code}.txt"
#     with open(output_file, "w", encoding="utf-8") as file:
#         file.write(text)

#     print(f"File saved: {output_file}")



# if __name__=='__main__':
#     pdf_path="D:\\personal\\Personal_Projects\\student_rag_app\\Backend\\Data\\python_handwritten-9-29.pdf"
#     language_code="eng"
#     extract_text_from_pdf(pdf_path, language_code)



import easyocr
from pdf2image import convert_from_path
import numpy as np
import cv2
import os


from dotenv import load_dotenv
from llama_parse import LlamaParse

load_dotenv()
GROQ_API_KEY=os.getenv("GROQ_API_KEY")
LLAMA_CLOUD_API_KEY=os.getenv("LLAMA_CLOUD_API_KEY")


def extract_text_from_pdf(pdf_path):
    """Extracts handwritten text from a PDF using EasyOCR and saves it to a text file."""

    # Create Output folder if not exists
    os.makedirs("Output", exist_ok=True)
    
    # Initialize EasyOCR Reader
    reader = easyocr.Reader(['en'])
    
    # Get PDF name (without extension)
    pdf_name = os.path.splitext(os.path.basename(pdf_path))[0]

    # Convert PDF pages to images
    images = convert_from_path(pdf_path)

    # Perform OCR using EasyOCR
    text = []
    for img in images:
        # Convert PIL image to NumPy array
        img_np = np.array(img)
        
        # Convert RGB to BGR (for OpenCV compatibility)
        img_cv = cv2.cvtColor(img_np, cv2.COLOR_RGB2BGR)
        
        # Perform OCR
        extracted_text = reader.readtext(img_cv, detail=0)
        text.extend(extracted_text)
    
    # Save the extracted text
    output_file = f"Output/{pdf_name}_handwritten.txt"
    with open(output_file, "w", encoding="utf-8") as file:
        file.write("\n".join(text))
    
    print(f"File saved: {output_file}")



#create instance of llamaparse
parser = LlamaParse(
    api_key=LLAMA_CLOUD_API_KEY,  # can also be set in your env as LLAMA_CLOUD_API_KEY
    result_type="markdown",  # "markdown" and "text" are available
    verbose=True
)


def parsed_pdf_data(pdf_path):

    instruction = """
    Extract all content from the provided handwritten notes, including:

    - Capture all text accurately, including paragraphs, lists, and annotations.
    - Preserve the order and structure of the content.
    - Retain formatting details like headings, subheadings, and emphasis.

    Provide a complete and organized representation of the handwritten notes in text format.
    """

    try:
        # Use LlamaParse to extract the data
        parsed_data = LlamaParse(result_type="markdown", api_key=LLAMA_CLOUD_API_KEY,
                                parsing_instruction=instruction).load_data(pdf_path)

    except Exception as e:
        parsed_data=""
   
    return parsed_data

if __name__ == '__main__':
    pdf_path = "D:/personal/Personal_Projects/student_rag_app/Backend/Data/42557_BDA_1.pdf"
    # extract_text_from_pdf(pdf_path)
    parsed_data=parsed_pdf_data(pdf_path)

    print("parsed data is :",parsed_data)

