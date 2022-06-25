# Lod-photobank

## Запуск
### Обычный способ

1) Для начала нужно запустить minIO для хранения изображений: 

`app/load/minio.exe server <дисковые тома>`

Например:
`app/load/minio.exe server F:\ G:\ H:\ I:\ J:\ K:\`

Самым простым вариантом будет указание папки, но в таком случае хранилище потеряет в производительности:

`app/load/minio.exe server app/load/data`

2) Запускаем само приложение в другом терминале:

2.1) (OPTIONAL) Указав ENV ZIP_DATASET_PATH можно добавить zip архив с датасетом для дампа изображений из датасета 

2.2) `streamlit run app.py`

### Docker
Пишем:

`docker-compose up`