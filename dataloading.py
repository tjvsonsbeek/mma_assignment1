##load a csv file containing a column 'image_paths' which contains paths to images and save the table in pickle format with an added column: 'clip_embeddings' which contains the CLIP embedding of the images
##and produce a column "umap_x" and "umap_y" which contains the UMAP coordinates of the images based on the clip embeddings
import pandas as pd
import clip
import h5py
import numpy as np
import pandas as pd
import os
import cv2
import umap
def process_data():
    df = pd.read_pickle('/media/tjvsonsbeek/Data11/physionet.org/files/mimic-cxr-jpg/2.0.0/vkd_val_1904.pkl')
    
    # get clip embeddings
    model, preprocess = clip.load('ViT-B/32', device='cuda')
    # model = clip.load('ViT-B/32', device='cuda')
    # print(df['Path_compr'])
    print(model.encode_image(preprocess(cv2.imread(df['Path_compr'].values[0].replace('Data1','Data11'))).unsqueeze(0)))
    df['clip_embeddings'] = df['Path_compr'].apply(lambda x: model.encode_image(preprocess(cv2.imread(x)).unsqueeze(0)).detach().cpu().numpy())
    print(df['clip_embeddings'])
    # create umap coordinates
    umap_embeddings = umap.UMAP(n_neighbors=5, n_components=2, metric='cosine').fit_transform(df['clip_embeddings'].tolist())
    df['umap_x'] = umap_embeddings[:,0]
    df['umap_y'] = umap_embeddings[:,1]
    
    df.to_pickle('data.pkl')
    
    # create hdf5 archive
    df = pd.read_pickle('data.pkl')
    with h5py.File('data.hdf5', 'w') as f:
        for i in range(len(df)):
            image = cv2.imread(df['Path_compr'][i])
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            image = cv2.resize(image, (224,224))
            f.create_dataset(str(i), data=image)
            

    # create tags for each image. If the value in a column in list column_names has value one the name of this column is added to the tags. Multiple tags are possible, and are concatenated with a space
    column_names = ['No Finding', 'Enlarged Cardiomediastinum', 'Cardiomegaly', 'Lung Opacity',
                      'Lung Lesion', 'Edema', 'Consolidation', 'Pneumonia', 'Atelectasis', 'Pneumothorax',
                      'Pleural Effusion', 'Pleural Other', 'Fracture', 'Support Devices']
    df['tags'] = df[column_names].apply(lambda x: ','.join([column_names[i] for i in range(len(x)) if x[i] == 1]), axis=1)
    df.to_pickle('data.pkl')
    
if __name__ == '__main__':
    process_data()