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

    def __init__(self,file_dir:List,chatbot:List) -> None:
        """
        file_dir(List) : file paths list 
        chatbot(List)  : list of chatbots conversation history
        """
        APPCFG=LoadConfig()
        self.file_dir=file_dir
        self.chatbot=chatbot
        db_path=APPCFG.uploaded_files_sqldb_directory
        db_path=f'sqlite:///{db_path}'
        self.engine=create_engine(db_path)
        print(f'number of uploaded files:',len(self.file_dir))


    def _process_uploaded_files(self)-> Tuple:
        """
        process the uploaded file and store them into the SQL database.
        Returns:
            Tuple(Str,List):empty string and the updated chatbot conversation list
        """
        for file_dir in self.file_dir:
            file_name_with_extensions=os.path.basename(file_dir)
            file_name,file_extension=os.path.splitext(file_name_with_extensions)
            if file_extension=='.csv':
                df=pd.read_csv(file_dir)
            elif file_extension=='.xlsx':
                df=pd.read_excel(file_dir)
            else:
                raise ValueError('the selected file type not supported')
            df.to_sql(file_name,self.engine,index=False)
            print('===================================================')
            print('All csv/xlsx files are saved into the sql database')
            self.chatbot.append(
                (" ","uploaded files are ready. Please ask questions")
            )
            return "",self.chatbot
        

    def _validate_db(self):
        """
        validate SQL database- updated correctly with the rught tables
        """
        insp=inspect(self.engine)
        table_names=insp.get_table_names()
        print('===================================================')
        print(f'Available table names in created SQL DB: {table_names}')
        print('===================================================')

    
    def run(self):
        """
        execute the file prpocessing pipelines
        contains : steps for processing uploaded files and validating the database
        """
        input_txt,chatbot=self._process_uploaded_files()
        self._validate_db()
        return input_txt,chatbot
    

class UploadFile:
    """
        control variaous file processsing pipleline based on chatbot functionality 

    """
    @staticmethod
    def run_pipeline(files_dir:List,chatbot:List,chatbot_functionality:str):
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
                file_dir=files_dir,chatbot=chatbot)
            input_txt,chatbot=pipeline_instance.run()
            return input_txt,chatbot
        
        else:
            pass
