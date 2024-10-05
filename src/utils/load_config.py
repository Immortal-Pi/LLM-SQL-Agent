import os
from dotenv import load_dotenv
import yaml
from pyprojroot import here
import shutil
from openai import AzureOpenAI
from langchain.chat_models import AzureChatOpenAI
import chromadb


print('environment varaibles are loaded',load_dotenv())

class LoadConfig:
    def __init__(self)->None:
        with open(here('config/app_config.yml')) as cfg:
            app_config=yaml.load(cfg,Loader=yaml.FullLoader)
        self.load_directories(app_config=app_config)


