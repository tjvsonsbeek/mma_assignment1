
""" 7,470 chest x-rays with 3,955 reports"""
import glob
import xmltodict
import xml.dom.minidom as minidom
import re
import os
from PIL import Image
import clip
import pandas as pd
import torch
import argparse
import umap
import torch
from torchvision.transforms import functional as F
from tqdm import tqdm
import h5py
import numpy as np
from sklearn.manifold import TSNE

    
def get_clip_embeddings(model_name, device, df, batch_size=1, base_path='', output_file='image_features.h5'):
    # load the model
    model, preprocess = clip.load(model_name, device=device)
    image_features = []

    with torch.no_grad(), h5py.File(output_file, "w") as hf:
        for i, image_name in tqdm(enumerate(df['filepaths'])):
            ## load the image, resize to 224x224 and load clip embeddings
            image = Image.open(os.path.join(base_path,image_name))
            image_input = preprocess(image).unsqueeze(0).to(device)
            image_features.append(model.encode_image(image_input).cpu().numpy())
    image_features = np.concatenate(image_features, axis=0)

    # Save image features to an H5 file
    with h5py.File(output_file, "w") as hf:
        hf.create_dataset("image_features", data=image_features)
    return skipped_indices
def make_df(dataset_path, train=True):
    """make a dataframe containing the image paths and the tags"""
    df = pd.DataFrame(columns=["filepaths", "tags"])
    train_test_split = pd.read_csv(os.path.join(dataset_path, 'train_test_split.txt'), sep=' ', index_col=0, header=None)
    id_to_img = pd.read_csv(os.path.join(dataset_path, 'images.txt'), sep=' ', index_col=0, header=None)
    classes = pd.read_csv(os.path.join(dataset_path, 'classes.txt'), sep='.', index_col=0, header=None)

    if train:
        is_train_image = 1
    else:
        is_train_image = 0

    img_ids = train_test_split[train_test_split[1]== is_train_image].index.tolist()
    ## fill dataframe with paths to images and tags (labels)
    for idx in tqdm(range(len(img_ids))):
        img_id = img_ids[idx]
        img_name = id_to_img[id_to_img.index== img_id].values[0][0]
        label = int(img_name[:3]) - 1
        text_label = classes.iloc[label].values[0]
        text_label = text_label.replace('_', ' ')
        df.at[idx, "filepaths"] =  'images/' + img_name
        df.at[idx, "tags"] = text_label
    return df
def make_umap(data, n_neighbors=6, n_components=2, metric='cosine'):
    return umap.UMAP(n_neighbors=n_neighbors, n_components=n_components, metric=metric).fit_transform(data)
def make_tsne(data, n_components=2, perplexity=30, n_iter=1000, metric='cosine'):
    return TSNE(n_components=n_components, perplexity=perplexity, n_iter=n_iter, metric=metric).fit_transform(data)
def process_data(dataset_path, output_path, column_names, image_size, model_name, device):
    # load the data

        
    df = make_df(dataset_path, train=True)

    get_clip_embeddings(model_name, device, df, base_path=dataset_path, output_file='openI_image_features_1000.h5')

# 
    output_file = "openI_image_features_1000.h5"
    # add the UMAP coordinates to the dataframe
    with h5py.File(output_file, "r") as hf:
        image_features = hf["image_features"][:]
    umap_embeddings = make_umap(image_features)
    df['umap_x'] = umap_embeddings[:,0]
    df['umap_y'] = umap_embeddings[:,1]
    
    tsne_embeddings = make_tsne(image_features)
    df['tsne_x'] = tsne_embeddings[:,0]
    df['tsne_y'] = tsne_embeddings[:,1]

    # create a column containing the tags, by combining the 'str' values of the columns in 'column_names with a ; 
    df['tags'] = df[column_names].apply(lambda x: ';'.join(x.astype(str)), axis=1)
    # save the dataframe
    df.to_pickle(output_path)
    return df

def argparser():
    parser = argparse.ArgumentParser(description='Load a csv file containing a column "image_paths" which contains paths to images and save the table in pickle format with an added column: "clip_embeddings" which contains the CLIP embedding of the images and produce a column "umap_x" and "umap_y" which contains the UMAP coordinates of the images based on the clip embeddings')
    parser.add_argument('--dataset_path', type=str, help='path to the csv file containing the image paths', default='/home/tjvsonsbeek/Documents/Datasets/CUB_200_2011')
    parser.add_argument('--output_path', type=str, help='path to the output pickle file',default='/home/tjvsonsbeek/Documents/Datasets/CUB_200_2011/CUB.pkl')
    parser.add_argument('--column_names', nargs='+', help='list of column names that should be used to create the tags', default=['tags'])#),'scientific name'])
    parser.add_argument('--image_size', type=int, default=224, help='size of the images that should be loaded')
    parser.add_argument('--model_name', type=str, default='ViT-B/32', help='name of the CLIP model that should be used')
    parser.add_argument('--device', type=str, default='cuda', help='device that should be used to run the CLIP model on')
    args = parser.parse_args()
    return args
if __name__ == '__main__':
    args = argparser()
    process_data(args.dataset_path, args.output_path, args.column_names, args.image_size, args.model_name, args.device)

