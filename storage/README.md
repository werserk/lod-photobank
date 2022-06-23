# Сравнение разных сервисов хранения. 

Основные требования:

1) **Бесплатное**

2) Достаточно места

3) Русское

4) Есть API

Организаторы хакатона предлагают использовать Яндекс.Диск, Mail облако или какое-либо s3 хранилище 

Варианты от меня: Dropbox, Google Drive

Сравнительная таблица:

Сервис     | Место | Русское |Доки | Ссылка на готовую либу|Доп описание
-----------| --------------|---------|--------------|-----------------------|---|
Яндекс.Диск| 10 Gb         |     ✓   |[тык](https://yandex.ru/dev/disk/)|https://pypi.org/project/yadisk/|с Я.Плюс 20 Gb
Mail Облако| 8 Gb|✓|[WebDAV платный](https://mcs.mail.ru/docs/base/s3/dev/s3-sdk?kb_language=ru_RU), [непубличный](https://github.com/SerjPopov/cloud-mail-ru-php)| https://github.com/mad-gooze/PyMailCloud | Ужасный API
DropBox| 2 Gb|✘|[Python SDK](https://www.dropbox.com/developers/documentation/python)|[тык](https://www.dropbox.com/developers/documentation/python) |
GoogleDrive|15 Gb|✘|[тык](https://developers.google.com/drive/api/quickstart/python)|[тык](https://developers.google.com/drive/api/quickstart/python)|
Amazon S3|5 Gb|✘|[тык](https://docs.amazonaws.cn/en_us/AmazonS3/latest/API/Type_API_Reference.html)|[тык](https://aws.amazon.com/ru/sdk-for-python/)|интеграция с AthenaDB, EMR. Недоступен в России. трафик ограничен
Yandex.Cloud S3|1 Gb|✓|[тык](https://cloud.yandex.ru/docs/storage/quickstart)|[тык](https://cloud.yandex.ru/docs/storage/tools/boto)|интеграция с Yandex.Cloud, [ограничения по трафику](https://cloud.yandex.ru/docs/storage/pricing)

По всем признакам хорошо подходит Яндекс.Диск - у него много места, есть удобный python SDK и он находится на территории РФ. REST и WebDAV API

Так же хорошим вариантом будет GoogleDrive - те же плюсы, что и Яндекс.Диск, интеграция с [платным Google Cloud](https://console.cloud.google.com/apis/library/drive.googleapis.com)

Поэтому выбор пал на Яндекс.Диск