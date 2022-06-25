import ruclip
import torch
from PIL import Image
import os
import faiss
import pandas as pd
import numpy as np
from utils import generate_filename

DEVICE = 'cpu'
EMBEDDING_LENGTH = 768
K = 2


def get_setup():
    model, processor = ruclip.load("ruclip-vit-large-patch14-336", device=DEVICE)
    return model, processor


def gen_batch(inputs, batch_size):
    batch_start = 0
    while batch_start < len(inputs):
        yield inputs[batch_start: batch_start + batch_size]
        batch_start += batch_size


def get_embeddings(model, processor, data):
    results = []
    data.sort()
    batch_size = 128
    batches = list(gen_batch(inputs=data, batch_size=batch_size))
    for batch in batches:
        pil_images = []
        for idx, path2img in enumerate(batch):
            try:
                image = Image.open(path2img)
                pil_images.append(image)
            except:
                del batch[idx]
        with torch.no_grad():
            batch_torch = processor(images=pil_images,
                                    return_tensors='pt',
                                    padding=True)["pixel_values"].to(DEVICE)
            preds = model.encode_image(batch_torch)
        for idx, (path2img, embeddings) in enumerate(zip(batch, preds)):
            results.append([path2img, embeddings])
    return results


def save_embeddings(classifiers, embeddings):
    embeddings = [(i, j.detach().cpu().numpy()) for i, j in embeddings]
    df = pd.DataFrame([(i, *j) for i, j in embeddings],
                      columns=["path"] + [f"embeddins_{i}" for i in range(embeddings[0][1].shape[-1])])
    predictions = []
    embeddings = [x for _, x in embeddings]
    for classifier in classifiers[:2]:
        time_preds_class = classifier.predict(embeddings)
        time_preds_class = [x[0] for x in time_preds_class]
        predictions.append(time_preds_class)
    for classifier in classifiers[2:]:
        preds_class = classifier.predict(embeddings)
        predictions.append(preds_class)

    preds_df = pd.DataFrame(predictions).transpose().add_prefix("tag")
    df.join(preds_df)
    filename = generate_filename()
    df.to_feather(f"data/embeddings/{filename}.feather")


def load_db_embeddings(include_filter):
    folder = 'data/embeddings'
    feathers = os.listdir(folder)
    df_res = pd.read_feather(os.path.join(folder, feathers[0]))
    for feather in feathers[1:]:
        df = pd.read_feather(os.path.join(folder, feather))
        df_res = df_res.append(df)
    for index, tag in enumerate(include_filter):
        if tag != 0:
            df_res = df_res[df_res[f"tag{index}"] == tag]
        df_res = df_res.drop(f"tag{index}")
    return df_res


def search_max_similary(df, embedding):
    data = df.iloc[:, 1:].to_numpy()
    data = np.ascontiguousarray(data)
    index = faiss.IndexFlatL2(EMBEDDING_LENGTH)
    embedding = embedding.detach().cpu().numpy()
    embedding = np.ascontiguousarray(embedding)
    index.add(data)
    D, I = index.search(embedding, K)
    I = list(I[0])
    return df.iloc[I, 0]


def get_embeddings_from_text(model, processor, request):
    tokenized = processor(text=request, return_tensors='pt', padding=True)["input_ids"]
    with torch.no_grad():
        embeddings = model.encode_text(tokenized)
    return embeddings
