import joblib

from models.userModel import UserDataModel
from typing import List, Dict, Any
import pandas as pd
from schemas.schemas_user import User_Ia_Create


svm_model = joblib.load('modelo_treinado.pkl')

class DataProcessor:
    @staticmethod
    def remove_unwanted_fields(user_data: UserDataModel) -> Dict[str, Any]:
        user_data_dict = user_data.dict()

        fields_to_remove = ['nome', 'numero', 'endereco']
        for field in fields_to_remove:
            if field in user_data_dict:
                del user_data_dict[field]

        return user_data_dict

    @staticmethod
    def prepare_data_for_classification(df: pd.DataFrame) -> pd.DataFrame:
            fields_to_remove = ['nome', 'numero', 'endereco']
            df_cleaned = df.drop(columns=fields_to_remove, errors='ignore')
            return df_cleaned

def classify_user(user_data: User_Ia_Create) -> int:
    filtered_data = DataProcessor.remove_unwanted_fields(user_data)
    data_to_predict = pd.DataFrame([filtered_data])
    prediction = svm_model.predict(data_to_predict)
    return int(prediction[0])

def classify_user_from_csv(df: pd.DataFrame) -> List[int]:
    processed_data = DataProcessor.prepare_data_for_classification(df)

    predictions = svm_model.predict(processed_data)

    return [int(pred) for pred in predictions]
