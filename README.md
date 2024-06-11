# Analysis crew
Document Analysis Application

#Overview
The Document Analysis Application is a powerful tool designed for document summarization and deep qualitative comparison analysis. It leverages the capabilities of LangChain and the agent framework CrewAI to provide comprehensive and accurate document insights. The application uses agents to perform specific tasks, such as summarizing documents, analyzing user queries, and synthesizing information from multiple documents.

# Features
- Document Summarization: Summarize documents to capture all key points and main ideas in an easy-to-understand format.
- Query Analysis: Analyze user queries to determine the required information and classify the query.
- Document Synthesis: Integrate and synthesize insights from one or multiple documents to provide a comprehensive response.
- File Upload and Processing: Upload multiple files and process them upon user request.

#Installation
To install and run the Document Analysis Application, follow these steps:

# Clone the repository:


git clone <repository-url>
cd <repository-directory>
Create and activate a virtual environment:



python3.11 -m venv venv
source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
Install dependencies:


pip install -r requirements.txt
Set up environment variables:

Create a .env file in the root directory and add your Azure OpenAI API keys and other necessary environment variables.


# Start the Application:


python crew_panel.py

# Upload Documents:

- Use the sidebar to upload documents.
- Click on the "Upload Files" button to process the uploaded documents.
- Query the System: Enter your query in the chat interface to analyze the documents and get a comprehensive response.
- 
# Configuration
- Environment Variables:
    -Ensure that your .env file contains the correct API keys and configuration settings.
Requirements
- Python 3.11
# Required Packages:
- Panel
- LangChain
- CrewAI
- Other dependencies listed in requirements.txt

# Work in Progress
This application is a work in progress. Further tools and agents are under development, including:

- Azure AI Pipeline for Blob Storage: Integrating blob storage for scalable and efficient data handling.

- Integrated Vectorization: Backed by indexes in Azure AI Search for enhanced document retrieval.

- Additional Analysis Tools: Including classification, systematic literature review, and meta-analysis.
