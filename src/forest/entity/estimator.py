import sys
from pandas import DataFrame
from sklearn.pipeline import Pipeline
from forest.exception import CustomException
from forest.logger import logging


class ForestModel:
    def __init__(self, preprocessing_object: Pipeline, trained_model_object: object):
        self.preprocessing_object = preprocessing_object
        self.trained_model_object = trained_model_object

    def predict(self, dataframe: DataFrame) -> DataFrame:
        logging.info("Entering predict method of ForestModel class")
        try:
            logging.info("Using the trained model to make predictions")
            transformed_feature = self.preprocessing_object.transform(
                dataframe)
            logging.info("Exited predict method of ForestModel class")
            return self.trained_model_object.predict(transformed_feature)
        except Exception as e:
            logging.error(f"Error in predict: {str(e)}")
            raise CustomException(e, sys)

    def __repr__(self) -> str:
        return f"{type(self.trained_model_object).__name__}()"

    def __str__(self) -> str:
        return f"{type(self.trained_model_object).__name__}()"
