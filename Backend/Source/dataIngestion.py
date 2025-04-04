import os
from pathlib import Path
import shutil
import sys
import json 
import uuid
import joblib
import warnings
from typing import List
from langchain_groq import ChatGroq
from dotenv import load_dotenv
from llama_parse import LlamaParse
from langchain.schema import Document
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings.fastembed import FastEmbedEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import UnstructuredMarkdownLoader
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_core.documents import Document
from langchain_community.document_loaders import PyPDFLoader
# from langchain_chroma import Chroma
from uuid import uuid4




load_dotenv()
warnings.filterwarnings("ignore")
GROQ_API_KEY=os.getenv("GROQ_API_KEY")
LLAMA_CLOUD_API_KEY=os.getenv("LLAMA_CLOUD_API_KEY")
GEMINI_API_KEY=os.getenv("GEMINI_API_KEY")
PROJECT_HOME_PATH = Path(__file__).resolve().parent


# Initialize Embeddings
embed_model = FastEmbedEmbeddings(model_name='BAAI/bge-base-en')
# embed_model = GoogleGenerativeAIEmbeddings(model="models/text-embedding-004",google_api_key=GEMINI_API_KEY)


llm = ChatGroq(model_name="mixtral-8x7b-32768",api_key=GROQ_API_KEY,temperature=0)



#create instance of llamaparse
parser = LlamaParse(
    api_key=LLAMA_CLOUD_API_KEY,  # can also be set in your env as LLAMA_CLOUD_API_KEY
    result_type="markdown",  # "markdown" and "text" are available
    verbose=True
)


def parsed_pdf_data(pdf_path):
    print("Inside parsed pdf data :")
    print("pdf path is :",pdf_path)
    # Define the instruction for LlamaParser
    instruction = """
        The provided document may contain various types of content, including text, tables, diagrams, mathematical equations, and HTML/Markdown.
        Follow these instructions carefully to ensure all data is captured accurately:

        1.Text Extraction:
        - Extract all plain text content such as paragraphs, lists, and descriptions.
        - Preserve text formatting like bold, italics, and underlines.
        - Maintain the logical flow of sentences and paragraphs without skipping essential information.

        2.Table Handling:
        - Identify tabular data and extract it in a structured format (CSV or JSON).
        - Ensure correct alignment of rows and columns.
        - Capture table headers and associate them with corresponding data.
        - For complex tables (with multi-level headers or merged cells), ensure proper mapping of the data and explain the table structure.

        3.Diagrams and Images:
        - Extract diagrams, charts, and images and store them separately (e.g., PNG, JPEG).
        - Extract any captions or annotations along with the diagrams.
        - Attempt to capture any embedded text or labels in the diagram.

        4.Mathematical Equations:
        - Identify and extract any mathematical formulas or symbols.
        - Ensure the extraction of superscripts, subscripts, and special characters.
        - Convert the equations to LaTeX or MathML format, if possible.

        5.HTML/Markdown Content:
        - For sections containing HTML, extract the HTML elements (tags, links, images) while preserving the structure.
        - For Markdown sections, retain headings, lists, code blocks, and links in markdown format.
        - Ensure any code snippets remain in their original format.

        6.Document Structure:
        - Preserve the document's hierarchical structure, including headings, subheadings, and sections, to maintain the readability of the parsed content.

        Try to provide an accurate representation of the document, and if questions arise, be as precise as possible when answering based on the parsed content.
        """

    try:
        # Use LlamaParse to extract the data
        # parsed_data = LlamaParse(result_type="markdown", api_key=LLAMA_CLOUD_API_KEY,
        #                         parsing_instruction=instruction).load_data(pdf_path)

        loader = PyPDFLoader(pdf_path)
        parsed_data=loader.load()


        # print("parsed data is :",parsed_data)
        for doc in parsed_data:
            print(doc.page_content)
            print()
    except Exception as e:
        parsed_data=""
   
    return parsed_data


# Create vector database
def create_vector_database(pdf_url,collection_name):
    print("inside create vectordb function :::")
    print("pdf url is :",pdf_url)
    print("pdf name is :",collection_name)

    print("Inside create vectordatabase normal function :::")
    try:
        vector_store = Chroma(
            collection_name=collection_name,
            embedding_function=embed_model,
            persist_directory="./Database",
        )

        documents=parsed_pdf_data(pdf_url)

        print("documents are :",documents)
        doc_list=[]
        for idr,doc in enumerate(documents):
            doc=Document(page_content=doc.page_content,id=idr)
            doc_list.append(doc)
        
        uuids = [str(uuid4()) for _ in range(len(doc_list))]

        vector_store.add_documents(documents=doc_list,ids=uuids)

        print('Vector DB created successfully !')
    
    except Exception as e :
        print("Error creating vector database ::: ",e)

    
if __name__=='__main__':
    data=parsed_pdf_data("D:\personal\Personal_Projects\student_rag_app\Backend\Data\shubham_murtadak_generative_ai_engineer_resume.pdf")
    
    print(data)
    # pdf_path="DocEase-Chat-with-PDF\\backend\\uploaded_files\\THIS IS A DUMMY PDF.pdf"
    # create_vector_database("https://firebasestorage.googleapis.com/v0/b/chat-pdf-6a1d8.firebasestorage.app/o/ZZMJ2JfefRTmhc2eAFYjkUo1VI12%2F2025-02-03%2Fshubham_murtadak_ai_ml_engineer_resume%20(5).pdf?alt=media&token=59da84c1-6bac-40bb-aea0-5d053c646d58")