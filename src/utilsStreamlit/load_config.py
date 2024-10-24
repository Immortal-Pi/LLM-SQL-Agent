import os
from dotenv import load_dotenv
import yaml
from pyprojroot import here
import shutil
from openai import AzureOpenAI
from openai import OpenAI
from langchain_community.chat_models import ChatOpenAI, AzureChatOpenAI
import chromadb



print('environment varaibles are loaded',load_dotenv())

class LoadConfig:
    def __init__(self)->None:
        with open(here('config/app_config.yml')) as cfg:
            app_config=yaml.load(cfg,Loader=yaml.FullLoader)
        self.load_directories(app_config=app_config)
        self.load_llm_configs(app_config=app_config)
        self.load_openai_models()
        #self.load_chroma_client()
        self.load_rag_config(app_config=app_config)

    def load_directories(self,app_config):
        self.stored_csv_xlsx_directory=here(
            app_config['directories']['stored_csv_xlsx_directory'])
        self.sqldb_directory = str(here(
            app_config['directories']['sqldb_directory']))
        self.stored_csv_xlsx_directory = here(
            app_config['directories']['stored_csv_xlsx_directory'])
        self.uploaded_files_sqldb_directory = str(here(
            app_config["directories"]["uploaded_files_sqldb_directory"]))
        self.stored_csv_xlsx_sqldb_directory = str(here(
            app_config["directories"]["stored_csv_xlsx_sqldb_directory"]))
        self.persist_directory = app_config["directories"]["persist_directory"]

    def load_llm_configs(self,app_config):
        self.model_name=os.getenv('AZURE_OPENAI_DEPLOYMENT_MODEL')
        self.agent_llm_system_role=app_config['llm_config']['agent_llm_system_role']
        self.rag_llm_system_role=app_config['llm_config']['rag_llm_system_role']
        self.temperature=app_config['llm_config']['temperature']
        self.embedding_model_name=os.getenv('AZURE_OPENAI_EMBEDDING_MODEL_NAME')

    def load_openai_models(self):
        # openai_api_key=os.environ['OPENAI_API_KEY']
        # self.openai_client=OpenAI()
        # self.langchain_llm=ChatOpenAI()
        azure_openai_api_key = os.environ["AZURE_OPENAI_API_KEY"]
        azure_openai_endpoint = os.getenv('AZURE_OPENAI_EMBEDDINGS_ENDPOINT')
        # This will be used for the GPT and embedding models
        self.azure_openai_client = AzureOpenAI(
            api_key=azure_openai_api_key,
            api_version=os.getenv("AZURE_OpenAI_API_VERSION"),
            azure_endpoint=azure_openai_endpoint)
        
        self.azure_openai_client_chat=AzureOpenAI(
            api_key=os.getenv('AZURE_OPENAI_API_KEY'),
                    api_version=os.getenv("AZURE_OpenAI_API_VERSION"),
                    azure_endpoint=os.getenv('AZURE_OpenAI_ENDPOINT')
        )
        self.langchain_llm = AzureChatOpenAI(
            openai_api_version=os.getenv("AZURE_OpenAI_API_VERSION"),
            azure_deployment=self.model_name,
            model_name=self.model_name,
            temperature=self.temperature)

    def load_chroma_client(self):
        self.chroma_client=chromadb.PersistentClient(
            path=str(here(self.persist_directory))
        )

    def load_rag_config(self,app_config):
        self.collection_name=app_config['rag_config']['collection_name']
        self.top_k=app_config['rag_config']['top_k']

    def remove_directory(self,directory_path,str):
        """

        :param directory_path:
        :param str:
        :return:
        """
        if os.path.exists(directory_path):
            try:
                shutil.rmtree(directory_path)
                print(f'the directory {directory_path} has been successfully removed ')
            except OSError as e:
                print(f'Error: {e}')
        else:
            print(f'the directory {directory_path} does not exist')