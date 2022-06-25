import ruclip
import torch
from PIL import Image
import os
import pandas as pd
import string
import random

DEVICE = 'cpu'


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


def generate_filename():
    filename = ''.join(random.choice(string.ascii_letters) for _ in range(8))
    return filename


def save_embeddings(embeddings):
    embeddings = [(i, j.detach().cpu().numpy()) for i, j in embeddings]
    df = pd.DataFrame([(i, *j) for i, j in embeddings],
                      columns=["path"] + [f"embeddins_{i}" for i in range(embeddings[0][1].shape[-1])])
    filename = generate_filename()
    df.to_feather(f"data/embeddings/{filename}.feather")
