from minio import Minio
from minio.error import S3Error
import logging

from omegaconf import DictConfig

log = logging.getLogger(__name__)


class S3Storage:
    def __init__(self, config: DictConfig):
        self.client = Minio(
            config.s3.endpoint_url,
            config.s3.access_key,
            config.s3.secret_key,
            secure=False
        )

        # Make 'log-photobank-prod' bucket if not exist.
        found = self.client.bucket_exists("lod-photobank-prod")
        if not found:
            self._init_bucket_with_data()

    def save_file_to_bucket(self, filepath):
        filename = filepath.split('/')[-1]
        self.client.fput_object(
            "lod-photobank-prod", filename, filepath,
        )

    def _init_bucket_with_data(self):
        log.info("Bucket 'lod-photobank-prod' doesn't exists...")
        log.info("Creating bucket.....")
        # TODO write code to load zip archive with dataset
        self.client.make_bucket("lod-photobank-prod")


def main():
    client = Minio(
        "127.0.0.1:9000",
        access_key="minioadmin",
        secret_key="minioadmin",
        secure=False
    )

    # Make 'asiatrip' bucket if not exist.
    found = client.bucket_exists("lod-photobank-prod")
    if not found:
        client.make_bucket("lod-photobank-prod")
    else:
        log.info("Bucket 'lod-photobank-prod' already exists")

    # Upload '/home/user/Photos/asiaphotos.zip' as object name
    # 'asiaphotos-2015.zip' to bucket 'asiatrip'.
    client.fput_object(
        "asiatrip", "asiaphotos-2015.zip", "/home/user/Photos/asiaphotos.zip",
    )
    print(
        "'/home/user/Photos/asiaphotos.zip' is successfully uploaded as "
        "object 'asiaphotos-2015.zip' to bucket 'asiatrip'."
    )


if __name__ == "__main__":
    try:
        main()
    except S3Error as exc:
        print("error occurred.", exc)