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
def get_clip_embeddings(model_name, device, df, batch_size=1, image_path='images/', output_file='image_features.h5'):
    # load the model
    model, preprocess = clip.load(model_name, device=device)
    image_features = []
    skipped_indices = []

    with torch.no_grad(), h5py.File(output_file, "w") as hf:
        for i, image_name in tqdm(enumerate(df['filepaths'].values[:1000])):
            try:
                image = Image.open(image_path + image_name)
                tensor_image = F.to_tensor(image)
                # if tensor_image.shape != (3, 224, 224):
                #     skipped_indices.append(i)
                #     continue
                tensor_image = tensor_image.unsqueeze(0).to(device)
                batch_features = model.encode_image(tensor_image)
                image_features.append(batch_features.cpu().numpy())
            except (FileNotFoundError, OSError):
                skipped_indices.append(i)

    image_features = np.concatenate(image_features, axis=0)

    # Save image features to an H5 file
    with h5py.File(output_file, "a") as hf:
        hf.create_dataset("image_features", data=image_features)

    # Print skipped indices
    print("Skipped Indices:", skipped_indices)
    # Save image features to an H5 file
    output_file = "image_features.h5"

    with h5py.File(output_file, "w") as hf:
        hf.create_dataset("image_features", data=image_features)
def make_umap(data, n_neighbors=5, n_components=2, metric='cosine'):
    return umap.UMAP(n_neighbors=n_neighbors, n_components=n_components, metric=metric).fit_transform(data)

def process_data(data_path, output_path, image_path, column_names, image_size, model_name, device):
    # load the data
    df = pd.read_csv(data_path, nrows=1000)
    print(df.head())
    
    get_clip_embeddings(model_name, device, df, image_path=image_path, output_file='image_features.h5')

    output_file = "image_features.h5"
    # add the UMAP coordinates to the dataframe
    with h5py.File(output_file, "r") as hf:
        image_features = hf["image_features"][:]
    umap_embeddings = make_umap(image_features)
    df['umap_x'] = umap_embeddings[:,0]
    df['umap_y'] = umap_embeddings[:,1]

    # create a column containing the tags, by combining the 'str' values of the columns in 'column_names with a space seperator
    df['tags'] = df[column_names].apply(lambda x: ' '.join(x.astype(str)), axis=1)
    # save the dataframe
    df.to_pickle(output_path)
    df.to_pickle('birds.pkl')
    return df

def argparser():
    parser = argparse.ArgumentParser(description='Load a csv file containing a column "image_paths" which contains paths to images and save the table in pickle format with an added column: "clip_embeddings" which contains the CLIP embedding of the images and produce a column "umap_x" and "umap_y" which contains the UMAP coordinates of the images based on the clip embeddings')
    parser.add_argument('--data_path', type=str, help='path to the csv file containing the image paths', default='/home/tjvsonsbeek/Documents/Datasets/birds/birds.csv')
    parser.add_argument('--output_path', type=str, help='path to the output pickle file',default='/home/tjvsonsbeek/Documents/Datasets/birds/birds.pkl')
    parser.add_argument('--image_path', type=str, help='path to the folder containing the images', default='/home/tjvsonsbeek/Documents/Datasets/birds/')
    parser.add_argument('--column_names', nargs='+', help='list of column names that should be used to create the tags', default=['labels','scientific name'])
    parser.add_argument('--image_size', type=int, default=224, help='size of the images that should be loaded')
    parser.add_argument('--model_name', type=str, default='ViT-B/32', help='name of the CLIP model that should be used')
    parser.add_argument('--device', type=str, default='cuda', help='device that should be used to run the CLIP model on')
    args = parser.parse_args()
    return args
if __name__ == '__main__':
    args = argparser()
    process_data(args.data_path, args.output_path, args.image_path, args.column_names, args.image_size, args.model_name, args.device)

