import enum


class Constants:
    """
    Application constants

    Includes:
        - DB_MAX_QUERIES: Maximum number of queries to database
    """
    DB_MAX_QUERIES = 1000000
    AUTHORIZATION_TOKEN_LIFETIME = 10080
    STORAGE_DATASETS_MARKERS = "storage/datasets/markers"
    STORAGE_DATASETS_RAW = "storage/datasets/raw"
    STORAGE_DATASETS_CLEAR = "storage/datasets/clear"
    STORAGE_DATASETS_READY = "storage/datasets/ready"
    STORAGE_DATASETS_TRAIN = "storage/datasets/_train"

