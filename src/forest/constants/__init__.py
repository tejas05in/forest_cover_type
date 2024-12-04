import os
from from_root import from_root

# common file name

TARGET_COLUMN = "Cover_Type"
FILE_NAME: str = "covtype.csv"
TRAIN_FILE_NAME: str = "train.csv"
TEST_FILE_NAME: str = "test.csv"
PREPROCSSING_OBJECT_FILE_NAME = "preprocessing.pkl"
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

# Data Transformation related constants start with DATA_TRANSFORMATION VAR_NAME

DATA_TRANSFORMATION_DIR_NAME: str = "data_transformation"
DATA_TRANSFORMATION_TRANSFORMED_DATA_DIR: str = "transformed"
DATA_TRANSFORMATION_TRANSFORMED_OBJECT_DIR: str = "transformed_object"

# Model Training related constants start with MODEL_TRAINING VAR_NAME

MODEL_TRAINER_DIR_NAME: str = "model_trainer"
MODEL_TRAINER_TRAINED_MODEL_DIR: str = "trained_model"
MODEL_TRAINER_TRAINED_MODEL_NAME: str = "model.pkl"
MODEL_TRAINER_EXPECTED_SCORE: float = 0.6
MODEL_FILE_NAME: str = "model.pkl"
MODEL_TRAINER_MODEL_CONFIG_FILE_PATH: str = os.path.join(
    "config", "model.yaml")
