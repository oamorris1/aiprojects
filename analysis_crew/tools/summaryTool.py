import os
import json
from langchain_community.document_loaders import PyMuPDFLoader
from langchain_community.document_loaders import PyPDFLoader, TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.tools import tool
from langchain.chains.summarize import load_summarize_chain
from langchain_openai import AzureChatOpenAI
import json
import os
import tiktoken
from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv('.env'))
text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=50, length_function=len)
deployment_name4 = "gpt-4"

llm_gpt4 = AzureChatOpenAI(deployment_name=deployment_name4, model_name=deployment_name4, temperature=0, streaming=True)
#path = r'C:\Users\Admin\Desktop\erdcDBFunc\crewAIDocSum\documents'
path_summary =  r'C:\Users\Admin\Desktop\erdcDBFunc\analysis_crew\summaries'
#new_path = r'C:\Users\Admin\Desktop\erdcDBFunc\crewAIDocSum\new_documents'

def embedding_cost(chunks):
    enc = tiktoken.encoding_for_model("text-embedding-ada-002")
    total_tokens = sum([len(enc.encode(page.page_content)) for page in chunks])
    # print(f'Total tokens: {total_tokens}')
    # print(f'Cost in US Dollars: {total_tokens / 1000 * 0.0004:.6f}')
    return total_tokens
 



class ObtainDocSummary():
   @tool("Document_Summary")
   def doc_sum(docs_path):
        """ Use this tool to access document folder and summarize a document"""
        text="" 
        summaries =[]
        for file_Name in os.listdir(docs_path):
          full_file_path = os.path.join(docs_path, file_Name)
                
          loader = PyPDFLoader(full_file_path)
          document = loader.load_and_split()
          for page in document:

            text += page.page_content
    
          text = text.replace('\t', ' ')
          chunks = text_splitter.create_documents([text])

          #chunks = text_splitter.split_documents(document)
          num_tokens = embedding_cost(chunks)
        #   if num_tokens < 50000:
        #       chain = load_summarize_chain(llm_gpt4, chain_type="stuff")
        #   else:
        #       chain = load_summarize_chain(llm_gpt4, chain_type="map_reduce")
          chain = load_summarize_chain(llm_gpt4, chain_type="stuff")
          summary_dict = chain.invoke(document)
          summary = summary_dict.get("output_text")
               
          new_file_name = file_Name.strip(".pdf")
          summaries.append({"title": file_Name, "summary":summary, "path":full_file_path})
          with open('summaries.json', 'w') as file:
               json.dump(summaries, file)  # Saving the list as JSON
          with open(f'{path_summary}\{new_file_name}_Summary.txt', "w") as file:
               file.writelines(summary)
        
        return summaries