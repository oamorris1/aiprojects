from crewai import Agent, Task, Crew, Process
from crewai.agents import CrewAgentExecutor
from crewai.project import CrewBase, agent, crew, task

from langchain_openai import AzureChatOpenAI

from tools.queryAnalysisTool import QueryDocumentAnalysis
from tools.summaryTool import ObtainDocSummary
from tools.docsysnthesis import DocumentSynthesisTool

import sys
import threading
import time 
from pathlib import Path

from dotenv import load_dotenv, find_dotenv


from tasks import AnalyzeDocumentTasks


import panel as pn 
pn.extension(design="material")
uploaded_files = []
uploaded_filenames = []
load_dotenv(find_dotenv('.env'))

deployment_name3 = "gpt-35-turbo-16k"
deployment_name4 = "gpt-4"
llm_gpt3 = AzureChatOpenAI(deployment_name=deployment_name3, model_name=deployment_name3, temperature=0, streaming=True)
llm_gpt4 = AzureChatOpenAI(deployment_name=deployment_name4, model_name=deployment_name4, temperature=0, streaming=True)

class DocumentSummarizeAgents():
   


    def document_summary_agent(self):
        return Agent(
            role='Expert Research and Document Analyst',
            goal=f"""Obtain a document from the ObtainDocSummary tool. Then use the ObtainDocSummary tool  to throughly read and anaylze a document.
            Provide a comprehensive summary of the given text. The summary should cover all the key points
            and main ideas presented in the original text, while also condensing the information into a concise and easy-to-understand format.
            Please ensure that the summary includes relevant details and examples that support the main ideas, while avoiding any unnecessary information
            or repetition. The length of the summary should be appropriate for the length and complexity of the original text, 
            providing a clear and accurate overview without omitting any important information Do not pass the summary to the query_analysis_agent .""",
             backstory="""An expert writer, researcher and analyst. You are a renowned writer and software engineer, known for
            your insightful and ability to write and summarize all key points in documents in an understable fashion.
            """,
    tools=[ObtainDocSummary.doc_sum],
    allow_delegation=False,
    verbose=True,
    max_iter=6,
    llm=llm_gpt4

        )

    def query_analysis_agent(self):
        return Agent(
            role="Expert Query Analyzer and Classifier",
            goal=f"""You receive user queries and determine the scope and depth of the required information to answer the query. Carefully analyze the query to extract
            what the user requires.
            Utilize the QueryAnalysisTool to dissect the query, identifying key words, phrases, and underlying questions.
            Classify the query to ascertain whether it can be addressed with a single document or if it requires a combination of documents.
            This classification should guide the subsequent agents in fetching and processing the right documents
            or summaries to formulate a complete and accurate response.""",
            backstory="""As a sophisticated linguistic model trained in semantic analysis and information retrieval, you specialize in understanding and categorizing complex queries.
            Your expertise lies in breaking down intricate questions into their elemental parts, determining the extent of information required,
            and directing these queries to the appropriate resources. Your analytical skills ensure that each query is processed efficiently and accurately, leading to timely and relevant responses.""",
            tools=[QueryDocumentAnalysis.analyze_query_and_summaries],
            allow_delgation=False,
            verbose=True,
            memory=True,
            llm=llm_gpt4,
            max_iter=6,
            
        )
        
    def single_document_analysis_agent(self):
        return Agent(
        role="Expert Integrative Synthesizer",
        goal=f""" Activated only after the query_analysis_agent has completed its assessment and identified the relevant document necessary to address the user's query.
        This agent's primary function is to integrate and synthesize insights from a single document to formulate a comprehensive, nuanced response. 
        It delves deep into the content of the document, extracts vital themes, identifies discrepancies, and interconnects these
        findings to construct a detailed and insightful narrative that fully addresses the complexities of the query.
        The synthesis process is meticulous, aiming to provide a multifaceted answer that draws from a diverse array of sources,
        thereby enriching the final output with well-rounded perspectives.
        """,
        backstory="""As an advanced synthesis model equipped with cutting-edge NLP capabilities, you excel at integrating
        diverse pieces of information into a unified whole. Your skills enable you to discern patterns
        and connections between different data points, making you adept at handling complex queries that require insights from multiple perspectives.
        Your analytical prowess turns disparate documents into coherent narratives, making complex information accessible and understandable.""",
        tools=[DocumentSynthesisTool.synthesize_documents],
        allow_delegation=True,
        verbose=True,
        memory=True,
        llm=llm_gpt4,
        max_iter=6
    )

        

    def document_analysis_agent(self):
      return Agent(
        role="Expert Integrative Synthesizer",
        goal=f""" Activated only after the query_analysis_agent has completed its assessment and identified the relevant documents necessary to address the user's query.
        This agent's primary function is to integrate and synthesize insights from multiple documents to formulate a comprehensive, nuanced response. 
        It delves deep into the content of each selected document, extracts vital themes, identifies discrepancies, and interconnects these
        findings to construct a detailed and insightful narrative that fully addresses the complexities of the query.
        The synthesis process is meticulous, aiming to provide a multifaceted answer that draws from a diverse array of sources,
        thereby enriching the final output with well-rounded perspectives.
        """,
        backstory="""As an advanced synthesis model equipped with cutting-edge NLP capabilities, you excel at integrating
        diverse pieces of information into a unified whole. Your skills enable you to discern patterns
        and connections between different data points, making you adept at handling complex queries that require insights from multiple perspectives.
        Your analytical prowess turns disparate documents into coherent narratives, making complex information accessible and understandable.""",
        tools=[DocumentSynthesisTool.synthesize_documents],
        allow_delegation=True,
        verbose=True,
        memory=True,
        llm=llm_gpt4,
        max_iter=6
    )



docs_path = "path/to/documents"
summaries_path = "path/to/save/summaries.json"
agents = DocumentSummarizeAgents()
tasks = AnalyzeDocumentTasks()

def custom_ask_human_input(self, final_answer: dict) -> str:
      
      global user_input

      prompt = self._i18n.slice("getting_input").format(final_answer=final_answer)

      chat_interface.send(prompt, user="assistant", respond=False)

      while user_input == None:
          time.sleep(1)  

      human_comments = user_input
      user_input = None

      return human_comments


CrewAgentExecutor._ask_human_input = custom_ask_human_input

user_input = None
initiate_chat_task_created = False

def initiate_chat(message):

    global initiate_chat_task_created
    # Indicate that the task has been created
    initiate_chat_task_created = True

    StartCrew(message)

def callback(contents: str, user: str, instance: pn.chat.ChatInterface):
    
    global initiate_chat_task_created
    global user_input

    if not initiate_chat_task_created:
        thread = threading.Thread(target=initiate_chat, args=(contents,))
        thread.start()

    else:
        user_input = contents

query= "What are some common variables used in studies regarding human error-based aviation accidents "

#agents
summarizer_agent = agents.document_summary_agent()
analyzer_agent   = agents.query_analysis_agent()
single_doc_analyzer_agent = agents.single_document_analysis_agent()
docs_analyzer_agent = agents.document_analysis_agent()


def StartCrew(prompt):

    doc_sum_task = tasks.summarize_document(summarizer_agent, docs_path)
    analyze_query_task = tasks.analyze_document_query(analyzer_agent, summaries_path, prompt )
    docs_synthesizer_task = tasks.document_sythesis(docs_analyzer_agent, prompt)
   
    # Create the crew with a sequential process
    summary_crew= Crew(
    agents=[summarizer_agent, analyzer_agent,  docs_analyzer_agent],
    tasks=[doc_sum_task, analyze_query_task,  docs_synthesizer_task],
    process=Process.sequential,
    verbose=True,
    manager_llm=llm_gpt4
)


    result = summary_crew.kickoff()

    chat_interface.send("## Final Result\n"+result, user="assistant", respond=False)



def handle_file_upload(event):
    global uploaded_files, uploaded_filenames
    new_files = file_input.value
    new_filenames = file_input.filename
    
    if new_files:
            if isinstance(new_files, list):
                uploaded_files.extend(new_files)
            else:
                uploaded_files.append(new_files)
            
            if isinstance(new_filenames, list):
                uploaded_filenames.extend(new_filenames)
            else:
                uploaded_filenames.append(new_filenames)
            if (len(uploaded_files) == 1):
                chat_interface.send(f"Added {len(uploaded_files)} file to the upload qeue.", user="System", respond=False)
            else:
                chat_interface.send(f"Added {len(uploaded_files)} file(s) to the upload qeue.", user="System", respond=False)

def process_files(event):
    global uploaded_files, uploaded_filenames
    save_folder_path = "C:path_to_document_folder/analysis_crew/documents"
    
    for file_content, file_name in zip(uploaded_files, uploaded_filenames):
        save_path = Path(save_folder_path, file_name)
        with open(save_path, mode='wb') as w:
            w.write(file_content)
        if save_path.exists():
            chat_interface.send(f"File '{file_name}' uploaded to directory successfully!", user="System", respond=False)
    
    # Clear the lists after processing
    uploaded_files.clear()
    uploaded_filenames.clear()

#file uploader widget
file_input = pn.widgets.FileInput(name="Upload Documents")
file_input.param.watch(handle_file_upload, 'value')

# Button to process uploaded files
process_button = pn.widgets.Button(name="Upload Files", button_type="primary")
process_button.on_click(process_files)

chat_interface = pn.chat.ChatInterface(callback=callback)
chat_interface.send("Please enter your query", user="System", respond=False)
#chat_interface.servable()

# Create the Material template
template = pn.template.MaterialTemplate(title='Document Analysis App')

# Add components to the sidebar
template.sidebar.append(pn.pane.Markdown("# Upload and Process Files"))
template.sidebar.append(file_input)
template.sidebar.append(process_button)

# Add components to the main area
template.main.append(chat_interface)


# Adding file input widget to the layout and serving the application with increased websocket and buffer size for large doument uploads
app = pn.Column(
    file_input,
    chat_interface,
    process_button,
    
)
MAX_SIZE_MB = 150
#layout.servable()
pn.serve(
    template,
    websocket_max_message_size=MAX_SIZE_MB * 1024 * 1024,
    http_server_kwargs={'max_buffer_size': MAX_SIZE_MB * 1024 * 1024}
)
