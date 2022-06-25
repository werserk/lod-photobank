import logging
import os

import streamlit as st
from hydra.core.global_hydra import GlobalHydra

import production
import utils

from app.extract.sources import LocalSource
from app.load.storages import S3Storage

import hydra
from omegaconf import DictConfig

log = logging.getLogger(__name__)

tags = 'Время суток	Время года	Местность	Авиа	Автомобили	БПЛА	Водолаз	Кинолог	Кони	Объятия	Шерп'.split(
    '\t')


def cached_get_setup():
    return production.get_setup()


@hydra.main(version_base="1.1", config_path="conf", config_name="default")
def main(config: DictConfig):
    # model, processor = cached_get_setup()
    log.info(os.getcwd())
    GlobalHydra.instance().clear()

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

    # SIDEBAR
    for tag in tags:
        st.sidebar.checkbox(tag)

    # БЛОК ЗАГРУЗКИ ФАЙЛОВ
    download_expander = st.expander('Загрузка файлов')
    filenames = download_expander.file_uploader('Выберите или перетащите сюда снимки', type=['png', 'jpeg', 'jpg'],
                                                accept_multiple_files=True)
    source = LocalSource(config)
    storage = S3Storage(config)
    if download_expander.button('Загрузить') and filenames:
        paths = source.extract_files(filenames)
        if not paths:
            st.error('Неправильный формат или название файла')
        else:
            #embeddings = production.get_embeddings(model, processor, paths)
            #production.save_embeddings(embeddings)
            for inner_paths in paths:
                for path in inner_paths:
                    log.info(paths)
                    storage.save_file_to_bucket(path)

    # # ОСНОВНАЯ ЛЕНТА
    # request = st.text_input('Поиск по описанию', value="")
    # st.button('Искать')
    # if st.button:
    #     data = production.load_db_embeddings()
    #     embeddings = production.get_embeddings_from_text(processor, request)
    #     max_k = production.search_max_similary(data, embeddings)
    #     print(max_k)


if __name__ == '__main__':
    main()
