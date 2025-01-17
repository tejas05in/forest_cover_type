import os
import sys
import json
import pandas as pd
from src.forest.logger import logging
from src.forest.exception import CustomException
from src.forest.entity.config_entity import *
from src.forest.entity.artifact_entity import *
from src.forest.constants import *
from src.forest.utils.main_utils import *
from evidently.model_profile import Profile
from evidently.model_profile.sections import DataDriftProfileSection


class DataValidation:
    def __init__(self, data_ingestion_artifact: DataIngestionArtifact,
                 data_validation_config: DataValidationConfig):
        self.data_ingestion_artifact = data_ingestion_artifact
        self.data_validation_config = data_validation_config
        self._schema_config = read_yaml_file(file_path=SCHEMA_FILE_PATH)

    @staticmethod
    def read_data(file_path: str) -> pd.DataFrame:
        try:
            logging.info(f"Reading data from file: {file_path}")
            return pd.read_csv(file_path)
        except Exception as e:
            logging.error(f"Error in read_data: {str(e)}")
            raise CustomException(e, sys)

    def validate_number_of_columns(self, dataframe: pd.DataFrame) -> bool:
        """validates the number of columns in the dataframe

        Args:
            dataframe (pd.DataFrame): dataframe to validate

        Returns:
            bool: True if all columns are present, False otherwise
        """
        try:
            status = len(dataframe.columns) == len(
                self._schema_config['columns'])
            logging.info(f"Number of columns validation status: [{status}]")
            return status
        except Exception as e:
            logging.error(f"Error in validate_number_of_columns: {str(e)}")
            raise CustomException(e, sys)

    def is_numerical_column_exist(self, df: pd.DataFrame) -> bool:
        """checks if numerical columns are present in the dataframe

        Args:
            dataframe (pd.DataFrame): dataframe to validate

        Returns:
            bool: True if numerical columns are present, False otherwise
        """
        try:
            dataframe_columns = df.columns
            status = True
            missing_numerical_columns = []
            for column in self._schema_config['numerical_columns']:
                if column not in dataframe_columns:
                    status = False
                    missing_numerical_columns.append(column)
            if len(missing_numerical_columns) > 0:
                logging.info(
                    f"Missing numerical columns: {missing_numerical_columns}")
            return status
        except Exception as e:
            logging.error(f"Error in is_numerical_column_exist: {str(e)}")
            raise CustomException(e, sys)

    def detect_data_drift(self, reference_df: pd.DataFrame, current_df: pd.DataFrame) -> bool:
        """Method to detect data drift between reference and current dataframes

        Args:
            reference_df (pd.DataFrame): reference dataframe
            current_df (pd.DataFrame): current dataframe

        Raises:
            CustomException:    Exception raised if any error occurs

        Returns:
            bool:  True if data drift is detected, False otherwise
        """
        try:
            data_drift_profile = Profile(sections=[DataDriftProfileSection()])
            data_drift_profile.calculate(reference_df, current_df)
            report = data_drift_profile.json()
            json_report = json.loads(report)
            write_yaml_file(
                file_path=self.data_validation_config.drift_report_file_path, content=json_report)
            n_features = json_report['data_drift']['data']['metrics']['n_features']
            n_drifted_features = json_report['data_drift']['data']['metrics']['n_drifted_features']
            logging.info(f"{n_drifted_features}/{n_features} drift detected")
            drift_status = json_report['data_drift']['data']['metrics']['dataset_drift']
            return drift_status
        except Exception as e:
            logging.error(f"Error in detect_data_drift: {str(e)}")
            raise CustomException(e, sys)

    def initiate_data_validation(self):
        logging.info(
            "Entering initiate_data_validation method of Data_Validation class")
        try:
            logging.info("Initiating data validation")
            validation_error_msg = ""
            train_df, test_df = (DataValidation.read_data(self.data_ingestion_artifact.trained_file_path),
                                 DataValidation.read_data(self.data_ingestion_artifact.test_file_path))
            status = self.validate_number_of_columns(train_df)
            if not status:
                validation_error_msg += "Columns not valid and are missing in train dataframe"
            status = self.validate_number_of_columns(test_df)
            if not status:
                validation_error_msg += "Columns not valid are missing in test dataframe"
            status = self.is_numerical_column_exist(train_df)
            if not status:
                validation_error_msg += "Columns are missing in train dataframe"
            status = self.is_numerical_column_exist(test_df)
            if not status:
                validation_error_msg += "Columns are missing in test dataframe"
            validation_status = len(validation_error_msg) == 0
            # if validation_status:
            #     drift_status = self.detect_data_drift(train_df, test_df)
            #     if drift_status:
            #         logging.info("Data Drift detected")
            # else:
            #     logging.info(f"Data validation failed: {validation_error_msg}")
            data_validation_artifact = DataValidationArtifact(
                validation_status=validation_status,
                message=validation_error_msg,
                drift_report_file_path=self.data_validation_config.drift_report_file_path
            )
            logging.info(
                f"Data validation artifact: {data_validation_artifact}")
            return data_validation_artifact
        except Exception as e:
            logging.error(f"Error in initiate_data_validation: {str(e)}")
            raise CustomException(e, sys)
