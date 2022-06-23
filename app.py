import streamlit as st
from utils import read_files, create_folder
from production import get_setup
import cv2


@st.cache
def cached_get_setup():
    return get_setup()


def main():
    models, transforms = cached_get_setup()

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
    for i in range(3):
        img = cv2.cvtColor(cv2.imread('image.jpg'), cv2.COLOR_BGR2RGB)
        list_of_files.image(img)

    download_expender = st.expander('Загрузка файлов')
    filenames = download_expender.file_uploader('Выберите или ператащите сюда снимки', type=['png', 'jpeg', 'jpg'],
                                                accept_multiple_files=True)
    if download_expender.button('Загрузить') and filenames:
        paths, folder_name = read_files(filenames)
        if not paths:
            st.error('Неправильный формат или название файла')


if __name__ == '__main__':
    main()
