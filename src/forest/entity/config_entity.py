import os
from dataclasses import dataclass
from from_root import from_root
from forest.constants import *


@dataclass
class DataIngestionConfig:
    def __init__(self):
        self.data_ingestion_dir: str = os.path.join(
            from_root(), ARTIFACTS_DIR, DATA_INGESTION_ARTIFACTS_DIR)
        self.feature_store_file_path: str = os.path.join(
            self.data_ingestion_dir, DATA_INGESTION_FEATURE_STORE_DIR, FILE_NAME)
        self.training_file_path: str = os.path.join(
            self.data_ingestion_dir, DATA_INGESTION_INGESTED_DIR, TRAIN_FILE_NAME)
        self.testing_file_path: str = os.path.join(
            self.data_ingestion_dir, DATA_INGESTION_INGESTED_DIR, TEST_FILE_NAME)
        self.train_test_split_ratio: float = DATA_INGESTION_TRAIN_TEST_SPLIT_RATIO
        
@dataclass
class DataValidationConfig:
    def __init__(self):
        self.data_validation_dir: str = os.path.join(
            from_root(), ARTIFACTS_DIR, DATA_VALIDATION_DIR_NAME)
        self.drift_report_file_path: str = os.path.join(
            self.data_validation_dir, DATA_VALIDATION_DRIFT_REPORT_DIR, 
            DATA_VALIDATION_DRIFT_REPORT_FILE_NAME)
