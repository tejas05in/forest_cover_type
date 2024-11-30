import os
import sys
from forest.components.data_ingestion import DataIngestion
from forest.components.data_validation import DataValidation
from forest.components.data_transformation import DataTransformation
from forest.logger import logging
from forest.exception import CustomException
from forest.entity.config_entity import *
from forest.entity.artifact_entity import *


class TrainPipeline:
    def __init__(self):
        self.data_ingestion_config = DataIngestionConfig()
        self.data_validation_config = DataValidationConfig()
        self.data_transformation_config = DataTransformationConfig()

    def start_data_ingestion(self) -> DataIngestionArtifact:
        try:
            logging.info(
                "Entering start_data_ingestion method of the TrainPipeline class")
            data_ingestion = DataIngestion(
                data_ingestion_config=self.data_ingestion_config)
            data_ingestion_artifact = data_ingestion.initiate_data_ingestion()
            logging.info(
                "Exited start_data_ingestion method of the TrainPipeline class")
            return data_ingestion_artifact
        except Exception as e:
            logging.error(f"Error in start_data_ingestion: {str(e)}")
            raise CustomException(e, sys)

    def start_data_validation(self, data_ingestion_artifact: DataIngestionArtifact) -> DataValidationArtifact:
        try:
            logging.info(
                "Entering start_data_validation method of the TrainPipeline class")
            data_validation = DataValidation(
                data_ingestion_artifact=data_ingestion_artifact,
                data_validation_config=self.data_validation_config)
            data_validation_artifact = data_validation.initiate_data_validation()
            logging.info(
                "Exited start_data_validation method of the TrainPipeline class")
            return data_validation_artifact
        except Exception as e:
            logging.error(f"Error in start_data_validation: {str(e)}")
            raise CustomException(e, sys)

    def start_data_transformation(self, data_ingestion_artifact: DataIngestionArtifact) -> DataTransformationArtifact:
        try:
            logging.info(
                "Entering start_data_transformation method of the TrainPipeline class")
            data_transformation = DataTransformation(
                data_ingestion_artifact=data_ingestion_artifact,
                data_transformation_config=self.data_transformation_config)
            data_transformation_artifact = data_transformation.initiate_data_transformation()
            return data_transformation_artifact
            logging.info(
                "Exited start_data_transformation method of the TrainPipeline class")
        except Exception as e:
            logging.error(f"Error in start_data_transformation: {str(e)}")
            raise CustomException(e, sys)

    def run_pipeline(self):
        data_ingestion_artifact = self.start_data_ingestion()
        data_validation_artifact = self.start_data_validation(
            data_ingestion_artifact)
        data_tranformation_artifact = self.start_data_transformation(
            data_ingestion_artifact)
        print(data_tranformation_artifact)
