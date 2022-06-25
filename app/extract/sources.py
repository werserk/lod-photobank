"""
Loaders for volunteers, who send random data to object storage
"""
import zipfile
from abc import ABC, abstractmethod
import os
import logging
from omegaconf import DictConfig
import yadisk

log = logging.getLogger(__name__)


class Source(ABC):
    """
    Class for loading images from different sources by volunteers.
    It's abstraction over extract stage of pipeline
    """
    def __init__(self, config: DictConfig):
        self.config = config
        self.cache_folder = f"{config.root_path}/{config.cache_folder}"
        os.makedirs(self.cache_folder, exist_ok=True)
        os.makedirs(self.cache_folder+"/images", exist_ok=True)
        os.makedirs(self.cache_folder + "/embeddings", exist_ok=True)

    @abstractmethod
    def extract_files(self, files):
        """
        Extract files from some source, that can be chosen by volunteer
        :param files: list of BytesIO-like objects,
        so can be used anywhere, where we need file. Have name and value attribute
        :return: paths to every file
        """
        pass


class LocalSource(Source):
    def extract_files(self, files):
        paths = []
        for file in files:
            paths.append([])
            filepath = f"{self.cache_folder}/{file.name}"
            with open(filepath, 'wb') as f:
                f.write(file.getvalue())
                paths[-1].append(filepath)
        log.info(f"Save {len(paths)} files to {self.cache_folder}")
        return paths

    def extract_zip(self, path_to_archive):
        paths = []
        try:
            dataset_path = f"{self.config.cache_path}/dataset"
            with zipfile.ZipFile(path_to_archive, 'r') as zip_ref:
                zip_ref.extractall(dataset_path)
            for root, subdirectories, files in os.walk(dataset_path):
                for file in files:
                    paths.append([os.path.join(root, file)])
        except FileNotFoundError:
            log.error(f"Zip archive {path_to_archive} not found!")
        return paths


class YandexDriveSource(Source):
    def __init__(self, config: DictConfig):
        super().__init__(config)
        self.client = yadisk.YaDisk(token=config.yadisk_token)
        if not self.client.check_token():
            log.error("Invalid yadisk token")
        log.info("Disk info:", self.client.get_disk_info())

    def extract_files(self, files):
        paths = []
        for file in files:
            paths.append([])
            filepath = f"{self.cache_folder}/{file.name}"
            paths[-1].append(filepath)
            self.client.download(file.name, filepath)
        log.info(f"Save {len(paths)} files to {self.cache_folder}")
        return paths
