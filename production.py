import ruclip
import torch
from PIL import Image
import os

DEVICE = 'cpu'


def get_setup():
    model, processor = ruclip.load("ruclip-vit-large-patch14-336", device=DEVICE)
    return model, processor


def gen_batch(inputs, batch_size):
    batch_start = 0
    while batch_start < len(inputs):
        yield inputs[batch_start: batch_start + batch_size]
        batch_start += batch_size


def get_embeddings(model, processor, paths):
    results = []
    batch_size = 128

    with torch.no_grad():
        for path in paths:
            data = [os.path.join(path, filename)
                    for filename in os.listdir(path)]
            data.sort()
            batches = list(gen_batch(inputs=data, batch_size=batch_size))
            for batch in batches:
                pil_images = []
                for idx, path2img in enumerate(batch):
                    try:
                        image = Image.open(path2img)
                        pil_images.append(image)
                    except:
                        del batch[idx]
                batch_torch = processor(images=pil_images,
                                        return_tensors='pt',
                                        padding=True)["pixel_values"].to(DEVICE)
                preds = model.encode_image(batch_torch)
                for idx, (path2img, embeddings) in enumerate(zip(batch, preds)):
                    results.append([path2img, embeddings])
    return results


