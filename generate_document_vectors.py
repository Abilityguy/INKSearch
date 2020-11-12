import numpy as np
import pandas as pd
import os
import pickle
import gensim.downloader as api
from helpers.helper_functions import generate_document_vector, preprocess_text
import argparse

parser = argparse.ArgumentParser(description = 'A program to generate and save \
                                                document vectors. ')
parser.add_argument('--csv', default='data/INKtalks_metaData.csv',
                    help='Path to csv file which contains the textual corpus.')
parser.add_argument('--column', default='Title', help='header name of column \
                    in csv file which contains the text of each document.')
parser.add_argument('--dst', default='document_vectors/', help = 'Destination  \
                    folder to save document vectors')

if __name__ == '__main__':
    args = parser.parse_args()

    model = api.load('glove-wiki-gigaword-50')
    df = pd.read_csv(args.csv)

    df['ProcessedText'] = df[args.column].apply(preprocess_text)

    document_vector_list = list()
    for index,word_list in enumerate(df['ProcessedText']):
        doc_vector = generate_document_vector(word_list, model)
        document_vector_list.append([index, doc_vector])

    with open(os.path.join(args.dst, 'document_vectors.pkl'), 'wb') as f:
        pickle.dump(document_vector_list, f)
