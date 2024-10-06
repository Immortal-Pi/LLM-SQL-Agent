from utils.prepare_vectordb_from_csv_xlsx import PrepareVectorDBFromTabularData

if __name__=='__main__':
    from pyprojroot import here
    titanic_dir=here('data/for_upload/titanic_small.csv')
    data_prep_instance=PrepareVectorDBFromTabularData(file_directory=titanic_dir)
    data_prep_instance.run_pipeline()
