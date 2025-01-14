import sys
import numpy as np
import pandas as pd
from src.forest.exception import CustomException
from src.forest.logger import logging
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.compose import ColumnTransformer
from imblearn.combine import SMOTEENN
from src.forest.constants import *
from src.forest.entity.config_entity import *
from src.forest.entity.artifact_entity import *
from src.forest.utils.main_utils import save_object, save_numpy_array_data, read_yaml_file


class DataTransformation:
    def __init__(self, data_ingestion_artifact: DataIngestionArtifact,
                 data_transformation_config: DataTransformationConfig):
        self.data_ingestion_artifact = data_ingestion_artifact
        self.data_transformation_config = data_transformation_config

    def get_data_tranformer_object(self):
        """Method Name: get_data_tranformer_object
        Description: This method is used to get the data transformer object
        Output: Data transformer object is created and returned
        On Failure: Write an exception to the log file and raise an exception
        Version: 1.2
        Revisions: Moved setup to cloud
        """
        logging.info(
            "Entering get_data_tranformer_object method of the DataTransformation class")

        try:

            _schema_config = read_yaml_file(SCHEMA_FILE_PATH)

            num_features = _schema_config['numerical_columns']

            numerical_pipeline = Pipeline(steps=[
                ('imputer', SimpleImputer(strategy='mean')),
                ('scaler', StandardScaler())
            ])
            preprocessor = ColumnTransformer(
                transformers=[
                    ('Numerical_Pipeline', numerical_pipeline, num_features)
                ])
            logging.info("Created preprocessor object from ColumnTransformer")

            return preprocessor

        except Exception as e:
            logging.error(f"Error in get_data_tranformer_object: {str(e)}")
            raise CustomException(e, sys) from e

    @staticmethod
    def read_data(data_path: str) -> pd.DataFrame:
        """Method Name: read_data
        Description: This method is used to read the data from the given path
        Output: Data is read and returned as a pandas dataframe
        On Failure: Write an exception to the log file and raise an exception
        Version: 1.2
        Revisions: Moved setup to cloud
        """
        logging.info(
            "Entering read_data method of the DataTransformation class")

        try:
            data = pd.read_csv(data_path)
            logging.info("Data read successfully")
            return data
        except Exception as e:
            logging.error(f"Error in read_data: {str(e)}")
            raise CustomException(e, sys) from e

    def initiate_data_transformation(self) -> DataTransformationArtifact:
        try:
            preprocessor = self.get_data_tranformer_object()

            train_df = DataTransformation.read_data(
                self.data_ingestion_artifact.trained_file_path)
            test_df = DataTransformation.read_data(
                self.data_ingestion_artifact.test_file_path)
            logging.info(
                "Got train features and test features of the Training Dataset")

            input_feature_train_df = train_df.drop(
                columns=[TARGET_COLUMN], axis=1)
            target_feature_train_df = train_df[TARGET_COLUMN]
            logging.info(
                "Separated input features and target features of the Training Dataset")

            input_feature_test_df = test_df.drop(
                columns=[TARGET_COLUMN], axis=1)
            target_feature_test_df = test_df[TARGET_COLUMN]
            logging.info(
                "Separated input features and target features of the Test Dataset")

            input_feature_train_arr = preprocessor.fit_transform(
                input_feature_train_df)
            logging.info(
                "Used the preprocessor object to fit and transform the train input features")

            input_feature_test_arr = preprocessor.transform(
                input_feature_test_df)
            logging.info(
                "Used the preprocessor object to transform the test input features")

            smt = SMOTEENN(sampling_strategy="minority", random_state=42)

            input_feature_train_final, target_feature_train_final = smt.fit_resample(
                input_feature_train_arr, target_feature_train_df)

            logging.info("Applied SMOTEENN to the train data")

            input_feature_test_final, target_feature_test_final = smt.fit_resample(
                input_feature_test_arr, target_feature_test_df)

            logging.info("Applied SMOTEENN to the test data")

            train_arr = np.c_[input_feature_train_final,
                              np.array(target_feature_train_final)]
            test_arr = np.c_[input_feature_test_final,
                             np.array(target_feature_test_final)]

            save_object(
                self.data_transformation_config.transformed_object_file_path, preprocessor)
            save_numpy_array_data(
                self.data_transformation_config.transformed_train_file_path, array=train_arr)
            save_numpy_array_data(
                self.data_transformation_config.transformed_test_file_path, array=test_arr)
            logging.info(
                "Saved the train and test arrays and the preprocessor object")

            data_transformation_artifact = DataTransformationArtifact(
                transformed_train_file_path=self.data_transformation_config.transformed_train_file_path,
                transformed_test_file_path=self.data_transformation_config.transformed_test_file_path,
                transformed_object_file_path=self.data_transformation_config.transformed_object_file_path
            )
            logging.info(
                "Exited initiate_data_transformation method of the DataTransformation class")
            return data_transformation_artifact
        except Exception as e:
            logging.error("Error occurred while transforming data")
            raise CustomException(e, sys)
