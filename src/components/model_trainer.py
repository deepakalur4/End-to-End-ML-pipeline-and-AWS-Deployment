from src.logger import logging
from src.exception import custom_exception
import os,sys
from dataclasses import dataclass
import pandas as pd,numpy as np
from src.utils import evlaute_model
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestRegressor,AdaBoostRegressor,GradientBoostingRegressor
from sklearn.svm import SVR
from sklearn.tree import DecisionTreeRegressor
from sklearn.linear_model import Ridge,Lasso
from sklearn.linear_model import ElasticNet
from sklearn.neighbors import KNeighborsRegressor
from sklearn.metrics import r2_score
from src.utils import save_obj


@dataclass
class model_trainer:
    model_pickle_file=os.path.join("artifacts","model.pkl")

class model_trainer_config:
    def __init__(self) -> None:
        self.model_trainer=model_trainer()
    
    def initiate_model_training(self,train_arr,test_arr):
        try:
            logging.info("Starting model training")
            X_train,X_test,y_train,y_test=(train_arr[:,:-1],test_arr[:,:-1],train_arr[:,-1],test_arr[:,-1])
            models={"logistic_reg":LogisticRegression(),
                    "decision_tree":DecisionTreeRegressor(),
                    "svr":SVR(),
                    "laso":Lasso(),
                    "ridge":Ridge(),
                    "elastic_net":ElasticNet(),
                    "neibour":KNeighborsRegressor(),
                    "rabdim_forst":RandomForestRegressor(),
                    "ada":AdaBoostRegressor(),
                    "gradinet":GradientBoostingRegressor()
                }
            best_modl=evlaute_model(x_train=X_train,y_train=y_train,x_test=X_test,y_test=y_test)
            best_model=(max(best_modl.values()))
            model=([i[0] for i in best_modl.items() if i[1]==best_model])
            best_model=models[model[0]]
            mod=best_model.fit(X_train,y_train)
            predicts=best_model.predict(X_test)

            save_obj(obj=best_model,file_path=self.model_trainer.model_pickle_file)

            return (r2_score(y_test,predicts))
           

        except Exception as e:
            raise custom_exception(e,sys)
