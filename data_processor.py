import joblib

from models.userModel import UserDataModel
from typing import Dict, Any
import pandas as pd
from schemas.schemas_user import User_Ia_Create

svm_model = joblib.load('modelo_treinado.pkl')

class DataProcessor:
    @staticmethod
    def remove_unwanted_fields(user_data: UserDataModel) -> Dict[str, Any]:
        # Convert the UserDataModel instance to a dictionary
        user_data_dict = user_data.dict()

        # Remove unwanted fields
        fields_to_remove = ['nome', 'numero', 'endereco']
        for field in fields_to_remove:
            if field in user_data_dict:
                del user_data_dict[field]

        return user_data_dict

def classify_user(user_data: User_Ia_Create) -> int:
    filtered_data = DataProcessor.remove_unwanted_fields(user_data)
    data_to_predict = pd.DataFrame([filtered_data])
    prediction = svm_model.predict(data_to_predict)
    return int(prediction[0])