import os
import pandas as pd
from utils.load_config import LoadConfig


class PrepareVectorDBFromTabularData:
    """
    prepare vector database from a csv file and XLSX file.
    loads the data into chromaDB collection.
    reading the CSV file and generating embeddings

    Attributes:
        APPCFG: Configuration object containing settings and client instances for the database and embeddings
        file_directory: Path to the csv file that contains data to be uploaded
    """

    def __init__(self,dataframe:pd.DataFrame,filename:str)->None:
        """
        file_directory: directory path of the file to be processed
        :param file_directory:
        """
        self.APPCFG=LoadConfig()
        self.dataframe=dataframe
        self.filename=filename

    def _inject_data_into_chromadb(self):
        """
        inject the prepared data into chromaDB
        error: if collection name already exists
        this method prints confirmation message upon successful data injection
        """
        collection=self.APPCFG.chroma_client.get_or_create_collection(name=self.APPCFG.collection_name)
        collection.add(
            documents=self.docs,
            metadatas=self.metadatas,
            embeddings=self.embeddings,
            ids=self.ids
        )
        print('=============================')
        print('Data is stored in ChromaDB')
    def run_pipeline(self):
        """
        preparing the database from the CSV.
        :return:
        """
        #self.df,self.dataframe=self.load_dataframe(dataframe=self.dataframe)
        self.docs,self.metadatas,self.ids, self.embeddings=self._prepare_data_for_injection(df=self.dataframe,file_name=self.APPCFG.collection_name)
        self._inject_data_into_chromadb()
        self.validate_db()
    

    def _prepare_data_for_injection(self,df:pd.DataFrame,file_name:str):
        """
        generate embeddings
        :param df:
        :param file_name:
        :return:
        """
        docs=[]
        metadatas=[]
        ids=[]
        embeddings=[]
        for index,row in df.iterrows():
            output_str=''
            for col in df.columns:
                output_str+=f'{col}:{row[col]},\n'
            response=self.APPCFG.azure_openai_client.embeddings.create(
                input=output_str,
                model=self.APPCFG.embedding_model_name
            )
            embeddings.append(response.data[0].embedding)
            docs.append(output_str)
            metadatas.append({'source':file_name})
            ids.append(f'id{index}')
        return docs, metadatas,ids,embeddings
    

    def validate_db(self):
        vectordb=self.APPCFG.chroma_client.get_collection(name=self.filename)
        print("==============================")
        print("Number of vectors in vectordb:", vectordb.count())
        print("==============================")
