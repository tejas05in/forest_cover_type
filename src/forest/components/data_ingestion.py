import os
import sys
import pandas as pd
from forest.logger import logging
from forest.exception import CustomException
from forest.entity.config_entity import *
from forest.entity.artifact_entity import *
from forest.utils.main_utils import *
from forest.data_access.forest_data import ForestData
from sklearn.model_selection import train_test_split


class DataIngestion:
    def __init__(self, data_ingestion_config: DataIngestionConfig = DataIngestionConfig()):
        try:
            self.data_ingestion_config = data_ingestion_config
        except Exception as e:
            logging.error(f"Error in DataIngestion constructor: {str(e)}")
            raise CustomException(e, sys)

    def export_data_into_feature_store(self) -> pd.DataFrame:
        try:
            logging.info("Exporting data from GDrive to Feature Store")
            forest_data = ForestData()
            os.makedirs(
                self.data_ingestion_config.data_ingestion_dir, exist_ok=True)
            forest_data.download_file(os.path.join(
                self.data_ingestion_config.data_ingestion_dir, FILE_NAME))
            dataframe = pd.read_csv(os.path.join(
                self.data_ingestion_config.data_ingestion_dir, FILE_NAME))
            logging.info(f"Dataframe shape: {dataframe.shape}")
            feature_store_file_path = self.data_ingestion_config.feature_store_file_path
            dir_path = os.path.dirname(feature_store_file_path)
            os.makedirs(dir_path, exist_ok=True)
            logging.info(
                f"Saving exported data into feature store file path: {feature_store_file_path}")
            dataframe.to_csv(feature_store_file_path, index=False, header=True)
            return dataframe
        except Exception as e:
            logging.error(f"Error in export_data_into_feature_store: {str(e)}")
            raise CustomException(e, sys)

    def split_data_as_train_test(self, dataframe: pd.DataFrame):
        """
        Method Name: split_data_as_train_test
        Description: This method is used to split the data into train and test dataframes

        Output: None
        On Failure: Write an exception log and raise Custom Exception

        Args:
            dataframe (pd.DataFrame): Dataframe to split into train and test

        Raises:
            CustomException: error in splitting data into train and test
        """
        try:
            logging.info("Splitting data into train and test")
            train, test = train_test_split(
                dataframe, test_size=self.data_ingestion_config.train_test_split_ratio)
            train_file_path = self.data_ingestion_config.training_file_path
            test_file_path = self.data_ingestion_config.testing_file_path
            dir_path = os.path.dirname(train_file_path)
            os.makedirs(dir_path, exist_ok=True)
            logging.info(
                f"Saving train data into train file path: {train_file_path}")
            train.to_csv(train_file_path, index=False, header=True)
            logging.info(
                f"Saving test data into test file path: {test_file_path}")
            test.to_csv(test_file_path, index=False, header=True)
        except Exception as e:
            logging.error(f"Error in split_data_as_train_test: {str(e)}")
            raise CustomException(e, sys)

    def initiate_data_ingestion(self) -> DataIngestionArtifact:
        """
        Method Name: initiate_data_ingestion
        Description: This method is used to initiate the data ingestion components of the training pipeline

        Output: Train and test sets are returned as DataIngestionArtifact
        On Failure: Write an exception log and raise Custom Exception

        Raises:
            CustomException: Error in initiate data ingestion

        Returns:
            DataIngestionArtifact: Train and test sets are returned as DataIngestionArtifact
        """
        try:
            dataframe = self.export_data_into_feature_store()
            _schema_config = read_yaml_file(file_path=SCHEMA_FILE_PATH)
            dataframe = dataframe.drop(_schema_config['drop_columns'], axis=1)
            self.split_data_as_train_test(dataframe)
            data_ingestion_artifact = DataIngestionArtifact(
                training_file_path=self.data_ingestion_config.training_file_path,
                testing_file_path=self.data_ingestion_config.testing_file_path
            )
            return data_ingestion_artifact
        except Exception as e:
            logging.error(f"Error in initiate_data_ingestion: {str(e)}")
            raise CustomException(e, sys)
