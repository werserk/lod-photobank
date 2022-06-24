from abc import ABC, abstractmethod
import os
import logging
from omegaconf import DictConfig
import yadisk

log = logging.getLogger(__name__)


class Loader(ABC):
    @abstractmethod
    def read_files(self, files):
        pass

    @abstractmethod
    def read_folder(self):
        pass


class LocalStorageLoader(Loader):
    def __init__(self, config: DictConfig):
        # TODO move to abstract loader
        self.cache_folder = f"{config.root_path}/{config.cache_folder}"
        os.makedirs(self.cache_folder, exist_ok=True)

    def read_folder(self):
        pass

    def read_files(self, files):
        paths = []
        for file in files:
            paths.append([])
            filepath = f"{self.cache_folder}/{file.name}"
            with open(filepath, 'wb') as f:
                f.write(file.getvalue())
                paths[-1].append(filepath)
        log.info(f"Save {len(paths)} files to {self.cache_folder}")
        return paths


class YandexDriveLoader(Loader):
    def __init__(self, config: DictConfig):
        self.client = yadisk.YaDisk(token=config.yadisk_token)
        if not self.client.check_token():
            log.error("Invalid yadisk token")
        log.info("Disk info:", self.client.get_disk_info())

        # TODO move to abstract loader
        self.cache_folder = f"{config.root_path}/{config.cache_folder}"
        os.makedirs(self.cache_folder, exist_ok=True)

    def read_folder(self):
        pass

    def read_files(self, files):
        paths = []
        for file in files:
            paths.append([])
            filepath = f"{self.cache_folder}/{file.name}"
            paths[-1].append(filepath)
            self.client.download(file.name, filepath)
        log.info(f"Save {len(paths)} files to {self.cache_folder}")
        return paths
