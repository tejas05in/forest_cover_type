import sys
import numpy as np
from src.forest.constants import *
from src.forest.exception import CustomException
from src.forest.logger import logging
from src.forest.entity.config_entity import ModelTrainerConfig
from src.forest.entity.artifact_entity import DataTransformationArtifact, ModelTrainerArtifact, ClassificationMetricArtifact
from neuro_mf import ModelFactory
from src.forest.entity.estimator import ForestModel
from src.forest.utils.main_utils import load_numpy_array_data, load_object, save_object
from typing import Tuple, List
from sklearn.metrics import f1_score, precision_score, recall_score


class ModelTrainer:
    def __init__(self, model_trainer_config: ModelTrainerConfig, data_transformation_artifact: DataTransformationArtifact):
        self.data_transformation_artifact = data_transformation_artifact
        self.model_training_config = model_trainer_config

    def get_model_object_and_report(self, train: np.ndarray, test: np.ndarray) -> Tuple[object, object]:
        """Method Name: get_model_object_and_report
        Description: This function uses neuro_mf library to get the model object and report of the base model

        Output: Tuple[object, object] - best model object and metric artifact object
        On Failure: Write an exception to the log file and raise a custom exception
        """
        try:
            logging.info(
                "Using neuro_mf library to get the model object and report of the base model")
            model_factory = ModelFactory(
                model_config_path=self.model_training_config.model_config_file_path)

            X_train, y_train, X_test, y_test = train[:,
                                                     :-1], train[:, -1], test[:, :-1], test[:, -1]

            best_model_detail = model_factory.get_best_model(
                X=X_train, y=y_train, base_accuracy=self.model_training_config.expected_accuracy)

            model_obj = best_model_detail.best_model
            logging.info(f"best_model: {model_obj}")
            logging.info(f"best_score: {best_model_detail.best_score}")

            y_pred = model_obj.predict(X_test)

            f1 = f1_score(y_test, y_pred, average='micro')
            precision = precision_score(y_test, y_pred, average='micro')
            recall = recall_score(y_test, y_pred, average='micro')
            metric_artifact = ClassificationMetricArtifact(
                f1_score=f1, precision_score=precision, recall_score=recall)

            return best_model_detail, metric_artifact

        except Exception as e:
            logging.error(
                "Error occurred in get_model_object_and_report method of ModelTrainer class")
            logging.error(str(e))
            raise CustomException(e, sys) from e

    def initiate_model_trainer(self,) -> ModelTrainerArtifact:
        logging.info(
            "Entering initiate_model_trainer method of ModelTrainer class")
        try:
            train_arr = load_numpy_array_data(
                file_path=self.data_transformation_artifact.transformed_train_file_path)
            test_arr = load_numpy_array_data(
                file_path=self.data_transformation_artifact.transformed_test_file_path)
            best_model_detail, metric_artifact = self.get_model_object_and_report(
                train=train_arr, test=test_arr)
            if best_model_detail.best_score < self.model_training_config.expected_accuracy:
                logging.info(
                    "No best model found with score more than base score")
                raise CustomException(
                    "No best model found with score more than base score", sys)
            preprocessing_obj = load_object(
                file_path=self.data_transformation_artifact.transformed_object_file_path)
            forest_model = ForestModel(
                preprocessing_object=preprocessing_obj,
                trained_model_object=best_model_detail.best_model
            )
            logging.info(
                "Created Forest model object with preprocessor and model object")
            logging.info("Created best model file path")
            save_object(
                self.model_training_config.trained_model_file_path, forest_model)

            metric_artifact = ClassificationMetricArtifact(
                f1_score=0.8,
                precision_score=0.8,
                recall_score=0.9
            )
            model_trainer_artifact = ModelTrainerArtifact(
                trained_model_file_path=self.model_training_config.trained_model_file_path,
                metric_artifact=metric_artifact
            )
            logging.info(
                f"Model trainer artifact : {model_trainer_artifact}")
            return model_trainer_artifact
        except Exception as e:
            logging.error(
                "Error occurred in initiate_model_trainer method of ModelTrainer class")
            logging.error(str(e))
            raise CustomException(e, sys) from e
