import os
import pandas as pd
from src.utils.load_config import LoadConfig


class PrepareVectorDBFromTabularData:
    """
    prepare vector database from a csv file and XLSX file.
    loads the data into chromaDB collection.
    reading the CSV file and generating embeddings

    Attributes:
        APPCFG: Configuration object containing settings and client instances for the database and embeddings
        file_directory: Path to the csv file that contains data to be uploaded
    """

    def __init__(self,file_directory:str)->None:
        """
        file_directory: directory path of the file to be processed
        :param file_directory:
        """
        self.APPCFG=LoadConfig()
        self.file_directory=file_directory

    def run_pipeline(self):
        """
        preparing the database from the CSV.
        :return:
        """
        self.db,self.file_name=self.load_dataframe(file_directory=self.file_directory)


    def load_dataframe(self,file_directory:str):
        """
        load data from csv or excel file

        :param file_directory:
        :return:
        """
        file_name_with_extensions=os.path.basename(file_directory)
        print(file_name_with_extensions)
        file_name,file_extension=os.path.splitext(
            file_name_with_extensions
        )
        if file_extension=='.csv':
            df=df = pd.read_csv(file_directory)
            return df, file_name
        elif file_extension == ".xlsx":
            df = pd.read_excel(file_directory)
            return df, file_name
        else:
            raise ValueError("The selected file type is not supported")

    def _prepare_data_for_injection(self,df:pd.DataFrame,file_name:str):
        """
        generate embeddings
        :param df:
        :param file_name:
        :return:
        """