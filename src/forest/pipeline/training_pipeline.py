import os
import sys
from forest.components.data_ingestion import DataIngestion
from forest.logger import logging
from forest.exception import CustomException
from forest.entity.config_entity import *
from forest.entity.artifact_entity import *


class TrainPipeline:
    def __init__(self):
        self.data_ingestion_config = DataIngestionConfig()

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

    def run_pipeline(self):
        data_ingestion_artifact = self.start_data_ingestion(self)
