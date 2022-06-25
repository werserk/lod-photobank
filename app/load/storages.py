from abc import ABC, abstractmethod

from minio import Minio
import logging

from omegaconf import DictConfig

log = logging.getLogger(__name__)


class Storage(ABC):
    """
    Storage class relate to different storage of our files
    Like S3, LocalFolders and others
    It's abstraction of load stage of pipeline
    """
    @abstractmethod
    def save_file_to_bucket(self, filepath, filename=None):
        """
        Saving file from path to cache to object some storage
        :param filepath: path to file
        :param filename: filename, which be assigned to image/video in object storage
        """
        pass

    @abstractmethod
    def load_file_from_bucket(self, filename):
        """
        Load file from bucket to cache
        :param filename: file id in object storage
        :return path to saved file
        """
        pass

    @abstractmethod
    def save_files_to_bucket(self, paths):
        """
        Save several files to bucket. This method is composition over save_file_to_bucket
        :param paths: paths to files to save
        """
        pass


class S3Storage(Storage):
    def __init__(self, config: DictConfig):
        self.config = config
        self.bucket_name = self.config.s3.bucket_name

        self.client = Minio(
            config.s3.endpoint_url,
            config.s3.access_key,
            config.s3.secret_key,
            secure=False
        )

        found = self.client.bucket_exists(self.bucket_name)
        if not found:
            log.info(f"Bucket '{self.bucket_name}' doesn't exists...")
            log.info("Creating bucket.....")
            self.client.make_bucket(self.bucket_name)

    def save_file_to_bucket(self, filepath, filename=None):
        if filename is None:
            filename = filepath.split('/')[-1]
        self.client.fput_object(
            self.bucket_name, filename, filepath,
        )

    def load_file_from_bucket(self, filename):
        path = f"{self.config.cache_path}/{filename}"
        self.client.fget_object(
            self.bucket_name, filename, path)
        return path

    def save_files_to_bucket(self, paths):
        for inner_paths in paths:
            for path in inner_paths:
                self.save_file_to_bucket(path, path)
