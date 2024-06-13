from crewai import Task



class AnalyzeDocumentTasks():
    def summarize_document(self, agent, docs_path):
       return Task(
           description=f"""Conduct a thorough analysis of a document using the Document_Summary tool.  The documents for summarization are here: {docs_path}
           Throughly read and anaylze a document. Provide a comprehensive summary of the given text. The summary should cover all the key points
           and main ideas presented in the original text, while also condensing the information into a concise and easy-to-understand format.
           The goal is to please ensure that the summary includes relevant details and examples that support the main ideas, while avoiding any unnecessary 
           information or repetition. The length of the summary should be appropriate for the length and complexity of the original text,
           providing a clear and accurate overview without omitting any important information. After the summaries are complete make sure
           that you check with a human to ensure the summaries are satifactory before the summaries are given to the next agent.""",
           agent=agent,
           async_execution=False,
           expected_output="""
           
          Provide a list of dictionaries. Each dictionary should contain:
          - 'title': The title of the document.
          - 'summary' : A through and detailed summary that captures all of the points in the original document
          - 'path': The file path to the document.
             The list format will facilitate the subsequent processing tasks without needing further parsing. DO NOT create your output as a JSON Object
             The output must be structured as a Python Dictionary.
           """,
           human_input = True
          


       )
    
    def analyze_document_query(self, agent, summaries_path, query):
     return Task(
        description=f"""
        Wait until the document_summary_agent has completed their task. Then, using the Query_and_Document_Summary_Analysis tool analyze
        the given user query: {query}
        to ascertain the specific information required from the document summaries found here: {summaries_path}.
        - Use the provided summaries_path to access and review document summaries.
        - The input format for the action should be a Python dictionary
        - The input should be a Python dictionary, but it MUST NOT be enclosed in triple backticks or have a JSON label.
        - The output will be a list of dictionaries detailing relevant documents, including titles and paths.
        - Extract key words, phrases, and underlying questions from the user's query using advanced NLP techniques.
        - Match these extracted elements with the information in the document summaries from the summaries loacted in the summaries_path to determine which document(s) could potentially answer the query. 
        - The process should be meticulous to ensure that all possible documents that could answer the query are considered,
        """,
        agent=agent,
        async_execution=False,  # Synchronous execution to maintain order and dependencies
        expected_output="""
        - Provide a list of dictionaries. Each dictionary should contain:
          - 'title': The title of the document.
          - 'path': The file path to the document.
          - You MUST structure your output in the form of a list of dictionaries.
          - The input SHOULD NOT be enclosed in triple backticks
          - The input SHOULD NOT have a JSON label.
          - The input SHOULD NOT have a python label
        The list format will facilitate the subsequent processing tasks without needing further parsing.   
        """
    )
    

  

    def document_sythesis(self, agent, query):
        return Task(
            description=f"""
            Wait until the query_analysis_agent has completed their task. Take the information recived from the query_analysis_agent
            to perform your task.  If it is a single document  use the single document to answer the query: {query}.  If it is multiple documents use all
            of the documents to answer the query.  Do not attempt to verify if the documents are sufficient or if the provided document is comprehensive for the task,
            take the document and path you are given and proceed with the task of using the proivided document or documents to 
            answer the query: '{query}'. 
            This task involves:
            - You must give your output to the document_analysis_agent as a LIST of DICTIONARIES.
            - DO NOT PASS the input as JSON 
            - The input should not be enclosed in triple backticks
            - The input should not have a JSON label.
            - The input should not have a python label
            - Receiving the necessary document paths and titles from the query_analysis_agent to answer the query
            - Analyzing each document  to extract key information, themes, and data points that are directly relevant to the query.
            - Comparing and contrasting the findings across different documents to identify commonalities, discrepancies, and unique insights.
            - Integrating these insights into a coherent narrative that addresses the query's requirements, highlighting how each piece of information contributes to understanding the broader topic.
            - Utilizing advanced NLP techniques to ensure that the synthesis is not only comprehensive but also presents the information in an easily digestible format for the end-user.
            """,
            agent=agent,
            
            
            async_execution=False,
            expected_output=f"""
            Produce a detailed synthesis report that addresses the query comprehensively. The report should:
            - Clearly articulate how each document contributes to the answer.
            - Provide a unified analysis that combines insights from all relevant documents.
            - Highlight key themes, conflicts, or consensus found in the literature regarding the query.
            - Include a summary section that distills the most critical findings into actionable insights or conclusions.
            - Be formatted to allow easy navigation between sections corresponding to each document's contribution to the narrative,
              ensuring that users can trace the origins of each piece of information.
            - DO NOT give your final answer in JSON or dictionary format.  It MUST be in the form of a well written formated human readable report.
            - The report must include: Clearly labeled  bold sections. 
            - The sections should include: an introduction section that restates the query. The names in bold of all documents used in the report. The
                key concepts or findings in bold followed by their explanations. A synthesis of the various documents' information and contribution and a final 
                conclusion summary section  that
                eloquently ties all the relevant data together into a conclusion.  
            """
    )



