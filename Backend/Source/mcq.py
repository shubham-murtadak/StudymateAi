import os 
import json 
from pathlib import Path 
from dotenv import load_dotenv
from langchain import PromptTemplate 
from langchain_groq import ChatGroq
from langchain_community.embeddings.fastembed import FastEmbedEmbeddings
from langchain_community.vectorstores import Chroma



# Load environment variables from .env file
load_dotenv()

# Load environment variables
PROJECT_HOME_PATH = os.getenv('PROJECT_HOME_PATH')
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
GROQ_API_KEY=os.getenv("GROQ_API_KEY")
LLAMA_CLOUD_API_KEY=os.getenv("LLAMA_CLOUD_API_KEY")
GEMINI_API_KEY=os.getenv("GEMINI_API_KEY")
PROJECT_HOME_PATH = Path(__file__).resolve().parent


vdb_path = os.path.join(PROJECT_HOME_PATH, 'Database', 'chroma_db')


llm = ChatGroq(model_name="llama-3.1-8b-instant",api_key=GROQ_API_KEY,temperature=0.8,)

# Initialize Embeddings
embed_model = FastEmbedEmbeddings(model_name='BAAI/bge-base-en')

#function to get chat response
def generate_mcq(collection_name):
    
    print(f"Using vector database at: {vdb_path}")
    
    
    vs_stored = Chroma(
        collection_name=collection_name,
        embedding_function=embed_model,
        persist_directory="./Database",
    )
    
    print("Vector store is:", vs_stored)

    question="Extract all documents"

    retriever = vs_stored.as_retriever(search_type="similarity", search_kwargs={"k": 6})

    text = retriever.invoke(input=question)

    
    template="""
        You are an AI specializing in **educational content creation**. Your task is to generate **multiple-choice questions (MCQs)** based on the provided key concepts.

        ### **Instructions:**
        - Generate **5 well-structured MCQs** based on the given key points.
        - Each question should be **clear, concise, and concept-focused**.
        - Provide **4 answer options**, ensuring that only **one option is correct**.
        - **Shuffle** the answer choices to make them challenging.
        - Strictly provide output in below metioned output format .
        - Strictly DO not provide anyhing expect mcqs ,not any starting cotent ,explaination etc.

        ### **Output Format:**
        {{
        "mcqs": [
            {{
            "question": "What is the primary function of X?",
            "options": ["Option A", "Option B", "Option C", "Option D"],
            "correct_option": "Option B"
            }},
           ......
        ]
        }}

         ### **Key Concepts Extracted from the Video:**
        "{text}"
        
        """

    prompt=PromptTemplate(
        template=template,
        input_variables=["text"]
    )
    #create chain of responses
    chain = (
        prompt
        | llm
    )

    mcqs=chain.invoke({"text":text})
    mcqs=mcqs.content

    result=mcqs[mcqs.find('{'):mcqs.rfind('}') + 1]
    result=json.loads(result)
    print("result of mcq is :",result)
    
    return result



if __name__=='__main__':
    collection_name="AI_Eng_Taskpdf"
    mcqs=generate_mcq(collection_name)

    print("Mcq geenrated are :",mcqs)
