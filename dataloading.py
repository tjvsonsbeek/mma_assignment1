from PIL import Image
import clip
import pandas as pd
import torch
import umap
import argparse
import torch
from torchvision.transforms import functional as F
from tqdm import tqdm
import h5py
import numpy as np
from sklearn.manifold import TSNE
def get_clip_embeddings(model_name, device, df, batch_size=1, image_path='images/', output_file='image_features.h5'):
    # load the model
    model, preprocess = clip.load(model_name, device=device)
    image_features = []
    skipped_indices = []

    with torch.no_grad(), h5py.File(output_file, "w") as hf:
        for i, image_name in tqdm(enumerate(df['filepaths'])):
            ## load the image, resize to 224x224 and load clip embeddings
            try:
                image = Image.open(image_path+image_name)
                tensor_image = F.to_tensor(image)
                
                image_input = tensor_image.unsqueeze(0).to(device)
                image_features.append(model.encode_image(image_input).cpu().numpy())
            except:
                print(image_input.shape)
                skipped_indices.append(i)
    image_features = np.concatenate(image_features, axis=0)

    # Print skipped indices
    print("Skipped Indices:", skipped_indices)
    # Save image features to an H5 file

    with h5py.File(output_file, "w") as hf:
        hf.create_dataset("image_features", data=image_features)
    return skipped_indices
def make_umap(data, n_neighbors=6, n_components=2, metric='cosine'):
    return umap.UMAP(n_neighbors=n_neighbors, n_components=n_components, metric=metric).fit_transform(data)
def make_tsne(data, n_components=2, perplexity=30, n_iter=1000, metric='cosine'):
    return TSNE(n_components=n_components, perplexity=perplexity, n_iter=n_iter, metric=metric).fit_transform(data)
def process_data(data_path, output_path, image_path, column_names, image_size, model_name, device):
    # load the data
    df = pd.read_csv('/home/tjvsonsbeek/Documents/Datasets/birds/birds.csv', nrows=1000)
    print(df.head())
    
    skipped_indices = get_clip_embeddings(model_name, device, df, image_path=image_path, output_file='image_features_1000.h5')
    # drop skipped indices
    # df = df.drop(skipped_indices)
# 
    output_file = "image_features_1000.h5"
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
    df.to_pickle('birds_1000.pkl')
    return df

def argparser():
    parser = argparse.ArgumentParser(description='Load a csv file containing a column "image_paths" which contains paths to images and save the table in pickle format with an added column: "clip_embeddings" which contains the CLIP embedding of the images and produce a column "umap_x" and "umap_y" which contains the UMAP coordinates of the images based on the clip embeddings')
    parser.add_argument('--data_path', type=str, help='path to the csv file containing the image paths', default='/home/tjvsonsbeek/Documents/Datasets/birds/birds.csv')
    parser.add_argument('--output_path', type=str, help='path to the output pickle file',default='/home/tjvsonsbeek/Documents/Datasets/birds/birds.pkl')
    parser.add_argument('--image_path', type=str, help='path to the folder containing the images', default='/home/tjvsonsbeek/Documents/Datasets/birds/')
    parser.add_argument('--column_names', nargs='+', help='list of column names that should be used to create the tags', default=['labels'])#),'scientific name'])
    parser.add_argument('--image_size', type=int, default=224, help='size of the images that should be loaded')
    parser.add_argument('--model_name', type=str, default='ViT-B/32', help='name of the CLIP model that should be used')
    parser.add_argument('--device', type=str, default='cuda', help='device that should be used to run the CLIP model on')
    args = parser.parse_args()
    return args
if __name__ == '__main__':
    args = argparser()
    process_data(args.data_path, args.output_path, args.image_path, args.column_names, args.image_size, args.model_name, args.device)

