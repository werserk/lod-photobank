import numpy as np
import logging
import os

import streamlit as st
from hydra.core.global_hydra import GlobalHydra

import production
import utils
import cv2
from catboost import CatBoostClassifier
import hashlib
import pickle
from _youtokentome_cython import BPE

from app.extract.sources import LocalSource
from app.load.storages import S3Storage

import hydra
from omegaconf import DictConfig

log = logging.getLogger(__name__)

tags = 'Время суток	Время года	Местность	Авиа	Автомобили	БПЛА	Водолаз	Кинолог	Кони	Объятия	Шерп'.split(
    '\t')


# def _hash(obj):
#     return hashlib.sha1(obj).digest()


# @st.cache(hash_funcs={BPE: _hash})
def get_setup():
    model, processor = production.get_setup()
    catboost_classifiers = [CatBoostClassifier().load_model(f'models/{tag.replace(" ", "_")}.cbm') for tag in tags]
    return model, processor, catboost_classifiers


@hydra.main(version_base="1.1", config_path="conf", config_name="default")
def main(config: DictConfig):
    model, processor, catboost_classifiers = get_setup()
    log.info(os.getcwd())
    GlobalHydra.instance().clear()

    source = LocalSource(config)
    storage = S3Storage(config)

    # pre-initialization
    dataset_path = os.environ.get('ZIP_DATASET_PATH')
    if dataset_path:
        paths = source.extract_zip(dataset_path)
        embeddings = production.get_embeddings(model, processor, paths)
        production.save_embeddings(embeddings)
        storage.move_files_to_bucket(paths)

    config.yadisk_token = os.environ.get("YADISK_TOKEN")

    page_bg_img = '''
    <style>
    .stApp {
      background-image: url("https://img2.goodfon.ru/wallpaper/nbig/a/b8/fon-minimalizm-tekstury.jpg");
      background-size: cover;
    }
    </style>
    '''

    st.markdown(page_bg_img, unsafe_allow_html=True)
    st.title('Фотобанк')

    include_tags = []
    # SIDEBAR
    for tag in tags:
        if tag == "Время суток":
            time_of_day = {0: "Не выбрано", 1: "День", 2: "Ночь", 3: "Рассвет/закат"}
            include_tag = st.sidebar.selectbox('Время суток', time_of_day, format_func=lambda x: time_of_day[x])
            include_tags.append(include_tag)
        elif tag == "Время года":
            season = {0: "Не выбрано", 1: "Зима", 2: "Весна", 3: "Лето", 4: "Осень"}
            include_tag = st.sidebar.selectbox('Время года', season, format_func=lambda x: season[x])
            include_tags.append(include_tag)
        elif tag == "Местность":
            place = {0: "Не выбрано", 1: "Лес", 2: "Город"}
            include_tag = st.sidebar.selectbox('Местность', place, format_func=lambda x: place[x])
            include_tags.append(include_tag)
        else:
            include_tag = st.sidebar.checkbox(tag)
            include_tags.append(int(include_tag))

    # БЛОК ЗАГРУЗКИ ФАЙЛОВ
    download_expander = st.expander('Загрузка файлов')
    filenames = download_expander.file_uploader('Выберите или перетащите сюда снимки', type=['png', 'jpeg', 'jpg'],
                                                accept_multiple_files=True)

    if download_expander.button('Загрузить') and filenames:
        paths = source.extract_files(filenames)
        if not paths:
            st.error('Неправильный формат или название файла')
        else:
            embeddings = production.get_embeddings(model, processor, paths)
            production.save_embeddings(catboost_classifiers, embeddings)
            storage.move_files_to_bucket(paths)

    # # ОСНОВНАЯ ЛЕНТА
    request = st.text_input('Поиск по описанию', value="")
    if st.button('Искать') and request:
        data = production.load_db_embeddings(include_tags)
        embeddings = production.get_embeddings_from_text(model, processor, request)
        best_paths = production.search_max_similary(data, embeddings)
        for path in best_paths:
            path = path.replace('\\', '/')
            if not os.path.isfile(path):
                storage.load_file_from_bucket(path)
            f = open(path, "rb")
            chunk = f.read()
            chunk_arr = np.frombuffer(chunk, dtype=np.uint8)
            img = cv2.imdecode(chunk_arr, cv2.IMREAD_COLOR)
            image = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            st.image(image)


if __name__ == '__main__':
    main()
