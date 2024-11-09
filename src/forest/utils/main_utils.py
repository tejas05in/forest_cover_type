import os
import sys
import yaml
from forest.logger import logging
from forest.exception import CustomException


def read_yaml_file(file_path: str) -> dict:
    try:
        with open(file_path, 'r') as stream:
            try:
                return yaml.safe_load(stream)
            except yaml.YAMLError as exc:
                logging.error(exc)
    except Exception as e:
        logging.error(e)
        raise CustomException(e, sys)
