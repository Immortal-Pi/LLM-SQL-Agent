import os 
from typing import List, Tuple
from utils.load_config import LoadConfig
from langchain_community.utilities import SQLDatabase
from langchain.chains import create_sql_query_chain 
from langchain_community.tools.sql_database.tool import QuerySQLDataBaseTool
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from operator import itemgetter
from sqlalchemy import create_engine
from langchain_community.agent_toolkits import create_sql_agent
import langchain
langchain.debug=True


APPCFG=LoadConfig()

class ChatBot:
    """
    capable of responding to the messages using different models of operation.
    interact with SQL databases 
    LLM for Q&A
    embeddings for retrieval-augmented generation (RAG) with chromaDB
    """