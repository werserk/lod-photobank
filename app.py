import streamlit as st

from app.extract.sources import LocalSource
import production
from utils import read_files
import cv2


# import hydra
# from omegaconf import DictConfig


# @st.cache
def cached_get_setup():
    return production.get_setup()


# @hydra.main(version_base="1.1", config_path="conf", config_name="default")
# def main(config: DictConfig):
def main():
    model, processor = cached_get_setup()

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
    st.text_input('Запрос по архиву', value="")

    list_of_files = st.expander('Найденные файлы')
    # for i in range(3):
    #     img = cv2.cvtColor(cv2.imread(f"{config.root_path}/image.jpg"), cv2.COLOR_BGR2RGB)
    #     list_of_files.image(img)

    download_expender = st.expander('Загрузка файлов')
    filenames = download_expender.file_uploader('Выберите или ператащите сюда снимки', type=['png', 'jpeg', 'jpg'],
                                                accept_multiple_files=True)
    # local_loader = LocalSource(config)
    if download_expender.button('Загрузить') and filenames:
        # paths = local_loader.extract_files(filenames)
        paths = read_files(filenames)
        if not paths:
            st.error('Неправильный формат или название файла')
        else:
            embeddings = production.get_embeddings(model, processor, paths)
            production.save_embeddings(embeddings)


if __name__ == '__main__':
    main()
