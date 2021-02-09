import argparse
import pymongo
import gensim
from helpers import helper_functions
import gensim.downloader as api
import numpy as np

# Computes the SIF weighted word vectors from given gensim model.
#
# Returns: List of that contains the word and it's corresponding weighted vector.
def compute_word_vectors(model, alpha=1e-3):
    word_vectors = list()
    vlookup = model.vocab
    Z = 0

    for word in vlookup:
        Z += vlookup[word].count

    for word in vlookup:
        vector = ((alpha / (alpha + (vlookup[word].count / Z)))*model[word]).tolist()
        word_vectors.append({'word':word, 'vector':vector})

    return word_vectors

# Inserts word vectors into the database.
#
# Returns: Object Ids of inserted documents.
def insert_word_vectors(db, word_vectors):
    inserted_ids = db.word_vectors.insert_many(word_vectors).inserted_ids
    return inserted_ids

def make_vector_indexes(db):
    db.word_vectors.create_index("word", unique=True)

# Computes SIF embeddings for INK video titles.
#
# Returns: A list of _id from the database and corresponding vector.
def compute_ink_embeddings(db, vector_size):
    sif_embeddings = dict()
    cursor = db.word_vectors.find({})
    for data in cursor:
        sif_embeddings[data['word']] = data['vector']

    ink_embeddings = list()
    for ink_details in db.inktalks.find({}):
        title = ink_details['Title']
        processed_title = helper_functions.preprocess_text(title)
        v = np.zeros(vector_size)
        vecs = [sif_embeddings[w] for w in processed_title if w in sif_embeddings]

        if (len(vecs) > 0):
            v = np.sum(vecs, axis=0)
            v *= 1/len(vecs)
        ink_embeddings.append({'_id': ink_details['_id'], 'sif_embeddings': v.tolist()})

    return ink_embeddings

# Inserts the SIF embeddings for each video into the database.
#
# Returns: Number of modified documents from the collection.
def update_ink_embeddings(db, ink_embeddings):
    bulk_ops = list()
    for data in ink_embeddings:
        bulk_ops.append(pymongo.UpdateOne({"_id": data['_id']}, {'$set': {'sif_embeddings': data['sif_embeddings']}}))

    n_modified = db.inktalks.bulk_write(bulk_ops, ordered=False).bulk_api_result['nModified']
    return n_modified

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--model', type=str, default='glove-wiki-gigaword-50')
    args = parser.parse_args()

    MONGO_SRV = "" # Add MongoDB Connection String URI here.

    mongo_client = pymongo.MongoClient(MONGO_SRV)
    db = mongo_client.db

    model = api.load(args.model)

    word_vectors = compute_word_vectors(model, alpha=1e-3)
    make_vector_indexes(db)
    successful_ids = insert_word_vectors(db, word_vectors)
    print(f"Successfully inserted {len(successful_ids)} / {len(word_vectors)} documents")

    ink_embeddings = compute_ink_embeddings(db, model.vector_size)
    n_modified = update_ink_embeddings(db, ink_embeddings)
    print(f"Successfully updated {n_modified}/{len(ink_embeddings)} documents")
