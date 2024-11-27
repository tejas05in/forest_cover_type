import os
from from_root import from_root

# common file name

FILE_NAME: str = "covtype.csv"
TRAIN_FILE_NAME: str = "train.csv"
TEST_FILE_NAME: str = "test.csv"
SCHEMA_FILE_PATH: str = os.path.join("config", "schema.yaml")

# Data Ingestion related constants

ARTIFACTS_DIR: str = os.path.join(from_root(), "artifacts")
DATA_INGESTION_ARTIFACTS_DIR: str = "DataIngestion"
DATA_INGESTION_FEATURE_STORE_DIR: str = "feature_store"
DATA_INGESTION_INGESTED_DIR: str = "ingested"
DATA_INGESTION_TRAIN_TEST_SPLIT_RATIO: float = 0.2

# Data Validation related constants start with DATA_VALIDATION VAR_NAME

DATA_VALIDATION_DIR_NAME: str = "data_validation"
DATA_VALIDATION_DRIFT_REPORT_DIR: str = "drift_report"
DATA_VALIDATION_DRIFT_REPORT_FILE_NAME: str = "report.yaml"
