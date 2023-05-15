from PIL import Image
import clip
import pandas as pd
import torch
import umap
import argparse

def process_data(data_path, output_path, image_path, column_names, image_size, model_name, device):
    # load the data
    df = pd.read_csv(data_path)
    # load the model
    model, preprocess = clip.load(model_name, device=device)
    # load the images and preprocess them
    images = [preprocess(Image.open(image_path + image_name)).unsqueeze(0) for image_name in df[column_names[0]].tolist()]
    # get the CLIP embeddings
    with torch.no_grad():
        image_features = model.encode_image(torch.cat(images).to(device)).cpu().numpy()
    # add the CLIP embeddings to the dataframe
    df["clip_embeddings"] = image_features.tolist()
    # add the UMAP coordinates to the dataframe
    umap_embeddings = umap.UMAP(n_neighbors=5, n_components=2, metric='cosine').fit_transform(df['clip_embeddings'].tolist())
    df['umap_x'] = umap_embeddings[:,0]
    df['umap_y'] = umap_embeddings[:,1]

    # create a column containing the tags, by combining the 'str' values of the columns in 'column_names with a space seperator
    df['tags'] = df[column_names].apply(lambda x: ' '.join(x.astype(str)), axis=1)
    # save the dataframe
    df.to_pickle(output_path)
    
    return df

def argparser():
    parser = argparse.ArgumentParser(description='Load a csv file containing a column "image_paths" which contains paths to images and save the table in pickle format with an added column: "clip_embeddings" which contains the CLIP embedding of the images and produce a column "umap_x" and "umap_y" which contains the UMAP coordinates of the images based on the clip embeddings')
    parser.add_argument('--data_path', type=str, help='path to the csv file containing the image paths')
    parser.add_argument('--output_path', type=str, help='path to the output pickle file')
    parser.add_argument('--image_path', type=str, help='path to the folder containing the images')
    parser.add_argument('--column_names', nargs='+', help='list of column names that should be used to create the tags')
    parser.add_argument('--image_size', type=int, default=224, help='size of the images that should be loaded')
    parser.add_argument('--model_name', type=str, default='ViT-B/32', help='name of the CLIP model that should be used')
    parser.add_argument('--device', type=str, default='cuda', help='device that should be used to run the CLIP model on')
    args = parser.parse_args()
    return args
if __name__ == '__main__':
    args = argparser()
    process_data(args.data_path, args.output_path, args.image_path, args.column_names, args.image_size, args.model_name, args.device)

