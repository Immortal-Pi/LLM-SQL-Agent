import gradio as gr
from utilsStreamlit.upload_files import UploadFile
from utilsStreamlit.chatbot import ChatBot
from utilsStreamlit.ui_settings import UISettings
import streamlit as st
from dotenv import load_dotenv
from PyPDF2 import PdfReader
from langchain.text_splitter import CharacterTextSplitter
from langchain_community.embeddings import OpenAIEmbeddings, HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from transformers import AutoModel, AutoTokenizer
from langchain.memory import ConversationBufferMemory
from langchain.chains.conversational_retrieval.base import ConversationalRetrievalChain
from langchain.chat_models import ChatOpenAI
#from htmlTemplates import css, bot_template, user_template
from langchain_chroma import Chroma
from chromadb import Client
# from langchain.llms import HuggingFaceHub
import json
import requests
from streamlit_lottie import st_lottie
import os
import chromadb
from pyprojroot import here
#from prepare_vectordb_from_text_chunks import create_chromaDB
import warnings
import pandas as pd

def load_lottiefile(filepath:str):
    with open(filepath,'r',encoding='utf-8') as f:
        return json.load(f)

def load_lottieurl(url:str):
    r=requests.get(url)
    if r.status_code!=200:
        return None
    return r.json()

def handle_userinput(input_text):
    response,query=ChatBot.respond('test',input_text,'Q&A with Uploaded CSV/XLSX SQL-DB','Chat')
    return response,query

if __name__=='__main__':
    lottie_db=load_lottieurl('https://lottie.host/c23cc5fe-51b5-499e-8a49-19ba8834359a/ySScDGWkb5.json')  
    st.title('SQL Agent for Tabular Data')
    
    st_lottie(
        lottie_db,
        speed=1,
        reverse=True,
        loop=True,
        quality='medium',
        # renderer='svg',
        height=300,
        width=300,
        key=None,
        
    )
    # menu = ['Upload data from CSV file', 'existing SQL database']
    # options = st.sidebar.radio("Select an Option :dart:",menu)  
    user_question=st.text_input("Ask me anything:")
    if user_question:
        response,queries=handle_userinput(user_question)
        st.write(f'ANSWER: {response}')
        
        st.write(f'Query USED: {queries}')
    with st.sidebar:
        
        st.subheader('Your Documents')
        csv_docs = st.file_uploader("Upload CSV here and click on process", accept_multiple_files=False)
        
        if st.button('Process'):
            with st.spinner('Agent getting ready'):
                doc_dataframe=pd.read_csv(csv_docs)
                table_names=UploadFile.run_pipeline(doc_dataframe,'file','Process files',csv_docs.name)
                st.write(f'existing tables in database {table_names}')
                
                
        st.text(' ')
        st.subheader('From Existing SQL tables')            
        if st.button('Process Tables'):
            table_names=UploadFile.validate_db()
            st.write(f'existing tables in database {table_names}')
        
        
