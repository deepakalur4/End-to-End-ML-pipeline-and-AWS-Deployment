from src.logger import logging
from src.exception import custom_exception
import os,sys
from dataclasses import dataclass
import pandas as pd
from sklearn.model_selection import train_test_split
from src.components.data_transformation import *

@dataclass
class data_ingestion:
    raw_data_path=os.path.join("artifacts","raw_data.csv")
    train_data_path=os.path.join("artifacts","train_data.csv")
    test_data_path=os.path.join("artifacts","test_data.csv")

class data_ingestion_config:
    def __init__(self):
        self.data_ingestion=data_ingestion()
    
    def initiate_data_ingestion(self):
        try:
            logging.info("Data ingestion_started")
            df=pd.read_csv(r"src\notebooks\data\stud.csv")
            train_data,test_data=train_test_split(df,test_size=0.2,random_state=42)
            os.makedirs(os.path.dirname(self.data_ingestion.raw_data_path),exist_ok=True)
            os.makedirs(os.path.dirname(self.data_ingestion.train_data_path),exist_ok=True)
            os.makedirs(os.path.dirname(self.data_ingestion.test_data_path),exist_ok=True)

            df.to_csv(self.data_ingestion.raw_data_path,header=True,index=False)
            train_data.to_csv(self.data_ingestion.train_data_path,header=True,index=False)
            test_data.to_csv(self.data_ingestion.test_data_path,header=True,index=False)
            
            return (self.data_ingestion.train_data_path,self.data_ingestion.test_data_path)
        except Exception as e:
            raise custom_exception(e,sys)


if __name__=='__main__':
    data_ingestion_obj=data_ingestion_config()
    train_path,test_path=data_ingestion_obj.initiate_data_ingestion()
    data_transformation_obj=data_transformation_config()
    train_arr,test_arr,_=data_transformation_obj.initiate_data_transoformation(train_path,test_path)
