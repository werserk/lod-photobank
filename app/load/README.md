# Выбор s3 хранилища

Критерии выбора:

1) Количество бесплатного места
2) Количество бесплатного трафика
3) Для локальных вариантов сложность развёртывания
4) Русское
5) Доступная документация

| Сервис       | Место | Трафик                           | Развёртывание                | Русское | Доки                                                                               | Доп описание                                                               |
|--------------|-------|:---------------------------------|:-----------------------------|---------|------------------------------------------------------------------------------------|----------------------------------------------------------------------------|
| AWS          | 5 Gb  | 100 Gb/месяц                     | Облако                       | ✘       | [тык](https://docs.amazonaws.cn/en_us/AmazonS3/latest/API/Type_API_Reference.html) | интеграция с AthenaDB, EMR. Недоступен в России                            |
| Yandex.Cloud | 1 Gb  | 10 000 операций PUT, 100 000 GET | Облако                       | ✓       | [тык](https://cloud.yandex.ru/docs/storage/quickstart)                             | интеграция с Yandex.Cloud                                                  |
| SberCloud    | N/D   | N/D                              | Облако                       | ✓       | [тык](https://docs.sbercloud.ru/s3/ug/index.html)                                  | неограниченный доступ, но всего на 14 дней                                 |
| MinIO        | ∞     | ∞                                | Docker, кубер, portable .exe | ✘       | [тык](https://min.io/download#/docker)                                             | простое и понятное ПО, 34к звёзд на GitHub, легко расширяемо               |
| LocalStack   | ∞     | ∞                                | Docker, cli                  | ✘       | [тык](https://github.com/localstack/localstack)                                    | максимально похож на AWS, создан для тестовых целей, имеет платные функции |
| Scality      | ∞     | ∞                                | Docker, yarn                 | ✘       | [тык](https://github.com/scality/cloudserver)                                      | написан на Node.js, 1.4к звёзд на Github, легко расширяемо                 |

  --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------


Таким образом исходя из требований кейсодержателя в наличии хранилища на 300 Gb, удобства использования и личных предпочтений был выбран MinIO