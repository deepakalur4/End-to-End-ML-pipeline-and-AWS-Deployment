from src.logger import logging
from src.exception import custom_exception
import os,sys
from dataclasses import dataclass
import pandas as pd,numpy as np
from sklearn.model_selection import train_test_split
from src.components import data_ingestion
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler,OneHotEncoder
from src.utils import save_obj
from sklearn.compose import ColumnTransformer

@dataclass
class data_transformation:
    preprocessor_pickle_file_path=os.path.join("artifacts","preprocessor.pkl")

class data_transformation_config:
    def __init__(self) -> None:
        self.data_transformation=data_transformation()
    
    def get_preprocessor_pickle_file(Self):
        try:
            num_col=['reading_score', 'writing_score']
            cat_col=['gender','race_ethnicity','parental_level_of_education','lunch','test_preparation_course']

            num_pipeline=Pipeline([
                ("Simple_imputer",SimpleImputer(strategy="median")),
                ("Scaling",StandardScaler())
            ])

            cat_pipeline=Pipeline([
                ("Simple_imputer",SimpleImputer(strategy="most_frequent")),
                ("One_hot_encoder",OneHotEncoder()),
                ("Scaling",StandardScaler(with_mean=False))
            ])

            preprocessor_pipeline=ColumnTransformer([
                ("num_col",num_pipeline,num_col),
                ("cat_col",cat_pipeline,cat_col)
            ])

            return preprocessor_pipeline
        
        except Exception as e:
            raise custom_exception(e,sys)
    
    def initiate_data_transoformation(Self,train_path,test_path):
        try:
            logging.info("Starting data transformation")
            preocessor_obj=Self.get_preprocessor_pickle_file()
            train_data=pd.read_csv(train_path)
            test_data=pd.read_csv(test_path)
            target_col="math_score"

            train_input_columns=train_data.drop(columns=[target_col],axis=1)
            train_output_columns=train_data[target_col]

            test_input_columns=test_data.drop(columns=[target_col],axis=1)
            test_output_columns=test_data[target_col]


            train_input_array=preocessor_obj.fit_transform(train_input_columns)
            test_input_array=preocessor_obj.transform(test_input_columns)
             

            train_arr=np.c_[train_input_array,train_output_columns]
            test_arr=np.c_[test_input_array,test_output_columns]

            save_obj(file_path=Self.data_transformation.preprocessor_pickle_file_path,obj=preocessor_obj)

            return (train_arr,test_arr,Self.data_transformation.preprocessor_pickle_file_path)


        except Exception as e:
            raise custom_exception(e,sys)