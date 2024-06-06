from crewai import Agent, Task, Crew, Process
from crewai.project import CrewBase, agent, crew, task
from langchain_openai import AzureChatOpenAI
import sys

from dotenv import load_dotenv, find_dotenv
from agents import DocumentSummarizeAgents
from tasks import AnalyzeDocumentTasks
load_dotenv(find_dotenv('.env'))

deployment_name3 = "gpt-35-turbo-16k"
deployment_name4 = "gpt-4"
llm_gpt3 = AzureChatOpenAI(deployment_name=deployment_name3, model_name=deployment_name3, temperature=0, streaming=True)
llm_gpt4 = AzureChatOpenAI(deployment_name=deployment_name4, model_name=deployment_name4, temperature=0, streaming=True)
#summaries_path =  r'C:\Users\Admin\Desktop\erdcDBFunc\analysis_crew\summaries.json'
#docs_path = path = r'C:\Users\Admin\Desktop\erdcDBFunc\analysis_crew\documents'

docs_path = "C:/Users/Admin/Desktop/erdcDBFunc/analysis_crew/documents"
summaries_path = "C:/Users/Admin/Desktop/erdcDBFunc/analysis_crew/summaries.json"
agents = DocumentSummarizeAgents()
tasks = AnalyzeDocumentTasks()
query= "What are some common variables used in studies regarding human error-based aviation accidents "
#agents
summarizer_agent = agents.document_summary_agent()
analyzer_agent   = agents.query_analysis_agent()
single_doc_analyzer_agent = agents.single_document_analysis_agent()
docs_analyzer_agent = agents.document_analysis_agent()

#tasks
doc_sum_task = tasks.summarize_document(summarizer_agent, docs_path)
analyze_query_task = tasks.analyze_document_query(analyzer_agent, summaries_path, query )
#single_doc_synthesizer_task = tasks.synthesize_single_document(single_doc_analyzer_agent, query)
docs_synthesizer_task = tasks.document_sythesis(docs_analyzer_agent, query)
#multi_doc_synthesizer_task.context = (analyze_query_task)

#crew
summary_crew= Crew(
    agents=[summarizer_agent, analyzer_agent,  docs_analyzer_agent],
    tasks=[doc_sum_task, analyze_query_task,  docs_synthesizer_task],
    process=Process.sequential,
    verbose=True,
    manager_llm=llm_gpt4
)


results = summary_crew.kickoff()

#synthesis_crew = Crew()
#meta_analysis_crew
#classification_crew
print(results)