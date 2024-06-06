import os
import json
from typing import Dict, List
from langchain_community.document_loaders import PyMuPDFLoader
from langchain_community.document_loaders import PyPDFLoader, TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_openai import AzureOpenAIEmbeddings
#from langchain.tools import tool
from crewai_tools import tool
from langchain.agents import Tool
from langchain.chains.summarize import load_summarize_chain
from langchain.chains import RetrievalQA
from langchain_community.vectorstores import FAISS
from langchain_openai import AzureChatOpenAI
text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=150)
embeddings = AzureOpenAIEmbeddings(deployment="text-embedding-ada-002", model="text-embedding-ada-002", chunk_size=10)
deployment_name3 = "gpt-35-turbo-16k"
deployment_name4 = "gpt-4"
llm_gpt3 = AzureChatOpenAI(deployment_name=deployment_name3, model_name=deployment_name3, temperature=0, streaming=True)
llm_gpt4 = AzureChatOpenAI(deployment_name=deployment_name4, model_name=deployment_name4, temperature=0, streaming=True)
from langchain_openai import AzureChatOpenAI
from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv('.env'))
deployment_name4 = "gpt-4"


query="What are some common variables used in studies regarding human error-based aviation accidents"
documents=[
    {
      "title": "The_role_of_human_factors_in_aviation_ground_operation_related_accidents.pdf",
      "path": "C:/Users/Admin/Desktop/erdcDBFunc/crewAIDocSum/documents/The_role_of_human_factors_in_aviation_ground_operation_related_accidents.pdf"
    }
  ]



def synthesize_documents(query: str, documents: List[Dict]):
     
     """
        Synthesizes single or multiple documents by extracting key information, themes, and narratives. 
        Provides a comprehensive and accessible overview of all relevant findings.
        Parameters:
            query (str): The user query to be answered.
            documents (list): A list of dictionaries containing details about the documents to be analyzed.
        Returns:
            str: A comprehensive synthesis of the information relevant to the query.
    """
     print("Starting document synthesis...")
     print(f"Query: {query}")
     print(f"Documents: {documents}")

     synthesized_information = ""
     for document in documents:

        title = document['title']
        path = document['path']
        print(f"Processing document: {title} at {path}")
        print("path variable type: ", type(path))
        try:
            loader = PyPDFLoader(path)
            needed_document = loader.load_and_split()
            print("made it here")
            # if n
            # eeded_document is None or not isinstance(needed_document, str):
            #     print(f"Document loaded is not a string: {type(needed_document)}")
            #     raise ValueError(f"Failed to load the document content properly from {path}")
            needed_doc_chunks = text_splitter.split_documents(needed_document)
            if not needed_doc_chunks:
                raise ValueError("No valid text chunks to process")
            vector_store = FAISS.from_documents(needed_doc_chunks, embeddings)
            retriever = vector_store.as_retriever()
            print("Made it here 2")
            qa_chain = RetrievalQA.from_chain_type(llm=llm_gpt4,chain_type="stuff", retriever=retriever)
            print("made it here 3")
            print("type query: ", type(query))
            result = qa_chain.invoke({"query": query})
            print("made it here 4")
            synthesized_information += f"Title: {title}\n{result['result']}\n\n"
            print(f"Processed: {title}")

        except Exception as e:
            print(f"An error occurred while processing document {title}: {e}")

     return synthesized_information

synthesized_info = synthesize_documents(query, documents)
print(synthesized_info)