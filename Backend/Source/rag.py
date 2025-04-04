import os
from pathlib import Path
import sys
import time
import shutil
import uuid
import ast
import uuid
import warnings
from uuid import uuid4
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain.prompts import PromptTemplate
from langchain_community.vectorstores import Chroma
from langchain.memory import ConversationBufferMemory
from langchain.retrievers.multi_query import MultiQueryRetriever
from langchain_community.embeddings.fastembed import FastEmbedEmbeddings
from langchain.chains import RetrievalQA, ConversationalRetrievalChain
from langchain_core.prompts import ChatPromptTemplate,MessagesPlaceholder
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.chat_history import InMemoryChatMessageHistory
from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI
# from langchain_chroma import Chroma

load_dotenv()
warnings.filterwarnings("ignore")


# Load environment variables from .env file
load_dotenv()

# Load environment variables
PROJECT_HOME_PATH = os.getenv('PROJECT_HOME_PATH')
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
GROQ_API_KEY=os.getenv("GROQ_API_KEY")
LLAMA_CLOUD_API_KEY=os.getenv("LLAMA_CLOUD_API_KEY")
GEMINI_API_KEY=os.getenv("GEMINI_API_KEY")
PROJECT_HOME_PATH = Path(__file__).resolve().parent


# Initialize Embeddings
embed_model = FastEmbedEmbeddings(model_name='BAAI/bge-base-en')
# embed_model = GoogleGenerativeAIEmbeddings(model="models/text-embedding-004",google_api_key=GEMINI_API_KEY)


llm = ChatGroq(model_name="llama-3.1-8b-instant",api_key=GROQ_API_KEY,temperature=0.8,)

# llm = ChatGoogleGenerativeAI(model='gemini-1.5-pro', google_api_key=GEMINI_API_KEY)

def retrive_data(question,collection_name):
    try:
        print("Inside retriever!")
        print("Question is:", question)
        print("Collection name is:", collection_name)

        vdb_path = os.path.join(PROJECT_HOME_PATH, 'Database', 'chroma_db')
        print(f"Using vector database at: {vdb_path}")
        
        
        vs_stored = Chroma(
            collection_name=collection_name,
            embedding_function=embed_model,
            persist_directory="./Database",
        )
        
        print("Vector store is:", vs_stored)

        retriever = vs_stored.as_retriever(search_type="similarity", search_kwargs={"k": 6})

        all_docs = retriever.invoke(input=question)
        
        no_of_docs=len(all_docs)

        print("All docs are:", all_docs)

        # Check if any documents were retrieved
        if not all_docs:
            print("No documents found!")
            return [], []

        # Extract text from the documents
        text_lst = [doc.page_content for doc in all_docs]

        return text_lst,no_of_docs
    
    except Exception as e:
        print("Error occurred:", e)
        return None, None

store={}
#function to manage sessionwise hisotry using inmemorychatmessagehistory
def get_session_history(session_id: str) -> BaseChatMessageHistory:
    if session_id not in store:
        # store[session_id] = deque(maxlen=2)
        store[session_id] = InMemoryChatMessageHistory()

    return store[session_id]


def chatbot(question,collection_name):
    try:
        # data = request.get_json()
        # query = data.get('query')

        # print(f"Query: {question}")

        docs,no_of_docs=retrive_data(question,collection_name)

        print()
        print(f"number of docs retrieve are :{no_of_docs}")

   
        # Define the ChatPromptTemplate
        prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                (
                    """
                   You are a highly intelligent AI assistant named **DocEase**, specializing in answering user queries based on PDF content. Your goal is to provide **structured, well-formatted responses** for clarity and readability.

                    ### **Response Formatting Guidelines:**
                    - Use **headings (`###`)** for major sections.
                    - Use **bold (`**text**`)** to highlight key information.
                    - Use **bullet points (`-`)** for lists and structured details.
                    - Use **line breaks** between sections for better readability.
                    - Ensure responses are **concise, engaging, and well-organized**.

                    ### **Instructions:**
                    - Answer the user's query **only based on the provided PDF content**.
                    - If the exact answer is not available, **respond with the best logical inference**.
                    - Avoid unnecessary text; focus on **clarity and structured presentation**.

                    **Context:**  
                    {context}  

                    **Question:**  
                    {input}  

                    **Answer:**  


                            """
                ),
            ),
            MessagesPlaceholder(variable_name="chat_history"),
            (
                "human",
                "{input}"
            ),
        ]
    )

        #create chain of responses
        chain = (
            prompt
            | llm
        )

        #add history in chain 
        chain_with_message_history = RunnableWithMessageHistory(
            chain,
            get_session_history,
            input_messages_key="input",
            history_messages_key="chat_history",
        )

        # invoke the chain
        response = chain_with_message_history.invoke(
            {"input": question,'context':docs},
            config={"configurable": {"session_id": collection_name}},
        )

        # return response.content

    
        response =response.content

        print(response)

        return response
        # return jsonify(response)
        
    except Exception as e:
        print(e)




if __name__ == '__main__':
    # app.run()
    # chatbot("what is mean by transformers ?")
    txt,img=retrive_data("provide me summary of pdf","multimodal_details")
    print("extracted text is :",txt)
    print("extraced images are :",img)