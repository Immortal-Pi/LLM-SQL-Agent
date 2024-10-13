import os
from typing import List,Tuple
from utils.load_config import LoadConfig
from sqlalchemy import create_engine, inspect
import pandas as pd 
APPCFG=LoadConfig()


class ProcessFiles:
    """
    this class uploads file(CSV, XLSX) to SQL database into seperate tables
    """

    def __init__(self,dataframe:pd.DataFrame,chatbot:List,filename:str) -> None:
        """
        file_dir(List) : file paths list 
        chatbot(List)  : list of chatbots conversation history
        """
        APPCFG=LoadConfig()
        self.dataframe=dataframe
        self.chatbot=chatbot
        self.filename=filename
        db_path=APPCFG.uploaded_files_sqldb_directory
        db_path=f'sqlite:///{db_path}'
        self.engine=create_engine(db_path)
        #print(f'number of uploaded files:',len(self.file_dir))


    def _process_uploaded_files(self):
        """
        process the uploaded file and store them into the SQL database.
        Returns:
            Tuple(Str,List):empty string and the updated chatbot conversation list
        """
        # for file_dir in self.file_dir:
        file_name_with_extensions=os.path.basename(self.filename)
        file_name,file_extension=os.path.splitext(file_name_with_extensions)
        #     if file_extension=='.csv':
        #         df=pd.read_csv(file_dir)
        #     elif file_extension=='.xlsx':
        #         df=pd.read_excel(file_dir)
        #     else:
        #         raise ValueError('the selected file type not supported')
        self.dataframe.to_sql(file_name,self.engine,index=False)
        print('===================================================')
        print('All csv/xlsx files are saved into the sql database')
        # self.chatbot.append(
        #     (" ","uploaded files are ready. Please ask questions")
        # )
        return ""
        

    def _validate_db(self):
        """
        validate SQL database- updated correctly with the rught tables
        """
        insp=inspect(self.engine)
        table_names=insp.get_table_names()
        print('===================================================')
        print(f'Available table names in created SQL DB: {table_names}')
        print('===================================================')
        return table_names

    
    def run(self):
        """
        execute the file prpocessing pipelines
        contains : steps for processing uploaded files and validating the database
        """
        output_txt=self._process_uploaded_files()
        table_names=self._validate_db()
        return table_names
    

class UploadFile:
    """
        control variaous file processsing pipleline based on chatbot functionality 

    """
    
    @staticmethod    
    def validate_db(text=' '):
        """
        validate SQL database- updated correctly with the rught tables
        """
        APPCFG=LoadConfig()
        
        db_path=APPCFG.uploaded_files_sqldb_directory
        db_path=f'sqlite:///{db_path}'
        engine=create_engine(db_path)
        insp=inspect(engine)
        table_names=insp.get_table_names()
        print('===================================================')
        print(f'Available table names in created SQL DB: {table_names}')
        print('===================================================')
        return table_names
    
    @staticmethod
    def run_pipeline(dataframe:pd.DataFrame,chatbot:List,chatbot_functionality:str,filename:str):
        """
            Run the appropriate pipeline based on functionality

            Args:
                files_dir (List): List of paths to uploaded files.
                chatbot (List): The current state of the chatbot's dialogue.
                chatbot_functionality (str): A string specifying the chatbot's current functionality.

            Returns:
                Tuple: Tuple: A tuple of an empty string and the updated chatbot list, or None if functionality not matched.
        """
        if chatbot_functionality=='Process files':
            pipeline_instance=ProcessFiles(
                dataframe=dataframe,chatbot=chatbot,filename=filename)
            table_names=pipeline_instance.run()
            return table_names
        else:
            pass
