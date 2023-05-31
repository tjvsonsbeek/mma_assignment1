import json
import re
import traceback

import pandas
from PIL import Image
import clip
import pandas as pd
import umap
import argparse
import torch
from torchvision.transforms import functional as F
from tqdm import tqdm
import h5py
import numpy as np
from sklearn.manifold import TSNE


def get_clip_embeddings(model_name, device, df, image_path, output_file):
    # load the model
    model, preprocess = clip.load(model_name, device=device)
    image_features = []
    skipped_indices = []

    with torch.no_grad(), h5py.File(output_file, "w") as hf:
        for i, image_name in tqdm(enumerate(df['filepaths'])):
            ## load the image, preprocess them and load clip embeddings
            try:
                image = preprocess(Image.open(image_path + image_name))
                image_input = image.unsqueeze(0).to(device)
                image_features.append(model.encode_image(image_input).cpu().numpy())
            except Exception as ex:
                traceback.print_exception(ex)
                skipped_indices.append(i)
    # Print skipped indices
    print("Skipped Indices:", skipped_indices)

    # Save image features to an H5 file
    image_features = np.concatenate(image_features, axis=0)

    with h5py.File(output_file, "w") as hf:
        hf.create_dataset("image_features", data=image_features)
    return skipped_indices


def make_umap(data, n_neighbors=6, n_components=2, metric='cosine'):
    return umap.UMAP(n_neighbors=n_neighbors, n_components=n_components, metric=metric).fit_transform(data)


def make_tsne(data, n_components=2, perplexity=30, n_iter=1000, metric='cosine'):
    return TSNE(n_components=n_components, perplexity=perplexity, n_iter=n_iter, metric=metric).fit_transform(data)


def process_data(df, output_path, image_path, column_names, model_name, device):
    output_file = "funda_image_features.h5"
    get_clip_embeddings(model_name, device, df, image_path=image_path, output_file=output_file)

    # add the UMAP coordinates to the dataframe
    with h5py.File(output_file, "r") as hf:
        image_features = hf["image_features"][:]
    umap_embeddings = make_umap(image_features)
    df['umap_x'] = umap_embeddings[:, 0]
    df['umap_y'] = umap_embeddings[:, 1]

    tsne_embeddings = make_tsne(image_features)
    df['tsne_x'] = tsne_embeddings[:, 0]
    df['tsne_y'] = tsne_embeddings[:, 1]

    # create a column containing the tags, by combining the 'str' values of the columns in 'column_names with a ;
    df['tags'] = df[column_names].apply(lambda x: ';'.join(x.astype(str)), axis=1)
    # save the dataframe
    df.to_pickle(output_path)
    return df

def parse_real_estate_json(json_path):
    with open(json_path, 'r') as ads_json:
        images_paths = []
        labels = []
        parsed = 0
        while parsed < 1000:
            ad = json.loads(ads_json.readline())
            if 'construction' in ad['features'] and 'kind of house' in ad['features']['construction']:
                images_paths.append(ad['images_paths'][0])
                house_type = re.sub('\(.*\)', '', ad['features']['construction']['kind of house'])
                labels.append(house_type)
                parsed += 1
        return pandas.DataFrame({'labels': labels, 'filepaths': images_paths})
    
def argparser():
    parser = argparse.ArgumentParser(description='Load the Funda ads jsonlines file containing image_paths to real estate images and save the table in pickle format with an added column: "clip_embeddings" which contains the CLIP embedding of the images and produce a column "umap_x" and "umap_y" which contains the UMAP coordinates of the images based on the clip embeddings')
    parser.add_argument('--json_path', type=str, help='path to the json file containing the image paths', default='./ads.jsonlines')
    parser.add_argument('--output_path', type=str, help='path to the output pickle file',default='./real_estate.pkl')
    parser.add_argument('--image_path', type=str, help='path to the folder containing the images', default='../RealEstateCrawler/funda/data/images/')
    parser.add_argument('--column_names', nargs='+', help='list of column names that should be used to create the tags', default=['labels'])
    parser.add_argument('--model_name', type=str, default='ViT-B/32', help='name of the CLIP model that should be used')
    parser.add_argument('--device', type=str, default='cpu', help='device that should be used to run the CLIP model on')
    args = parser.parse_args()
    return args

if __name__ == '__main__':
    args = argparser()
    data = parse_real_estate_json(args.json_path)
    process_data(data, args.output_path, args.image_path, args.column_names, args.model_name, args.device)