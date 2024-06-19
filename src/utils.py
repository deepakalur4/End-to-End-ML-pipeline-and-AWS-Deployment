import os
import pickle

def save_obj(file_path,obj):
    try:
        dir_path = os.path.dirname(file_path)        
        os.makedirs(dir_path, exist_ok=True)
        with open(file_path,"wb") as file_obj:
            pickle.dump(obj,file_obj)
    except Exception as e:
        raise custom_exception(e,sys)
