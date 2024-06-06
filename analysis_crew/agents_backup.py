from langchain_openai import AzureChatOpenAI
from langchain_core.callbacks import BaseCallbackHandler
from typing import TYPE_CHECKING, Any, Dict, Optional
import threading
from crewai import Agent, Task, Crew, Process
from dotenv import load_dotenv, find_dotenv


from tools.queryAnalysisTool import QueryDocumentAnalysis
from tools.summaryTool import ObtainDocSummary
from tools.docsysnthesis import DocumentSynthesisTool

import panel as pn 
pn.extension(design="material")

load_dotenv(find_dotenv('.env'))

deployment_name4 = "gpt-4"
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