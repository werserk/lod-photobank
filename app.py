import streamlit as st

import production
import utils
import cv2

tags = 'Время суток	Время года	Местность	Авиа	Автомобили	БПЛА	Водолаз	Кинолог	Кони	Объятия	Шерп'.split(
    '\t')


def cached_get_setup():
    return production.get_setup()


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

    ### SIDEBAR
    for tag in tags:
        st.sidebar.checkbox(tag)

    ### БЛОК ЗАГРУЗКИ ФАЙЛОВ
    download_expender = st.expander('Загрузка файлов')
    filenames = download_expender.file_uploader('Выберите или ператащите сюда снимки', type=['png', 'jpeg', 'jpg'],
                                                accept_multiple_files=True)
    if download_expender.button('Загрузить') and filenames:
        paths = utils.read_files(filenames)
        if not paths:
            st.error('Неправильный формат или название файла')
        else:
            embeddings = production.get_embeddings(model, processor, paths)
            production.save_embeddings(embeddings)

    ### ОСНОВНАЯ ЛЕНТА
    request = st.text_input('Поиск по описанию', value="")
    if st.button('Искать') and request:
        data = production.load_db_embeddings()
        embeddings = production.get_embeddings_from_text(model, processor, request)
        best_paths = production.search_max_similary(data, embeddings)
        for path in best_paths:
            path = path.replace('\\', '/')
            image = cv2.cvtColor(cv2.imread(path), cv2.COLOR_BGR2RGB)
            st.image(image)


if __name__ == '__main__':
    main()
