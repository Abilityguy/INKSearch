from helpers import helper_functions
import numpy as np

def get_ink_vectors(db):
    ink_data = list(db.inktalks.find({},{'Title': 1, 'Speakers': 1, \
            'Talk URL': 1, 'Talk Thumbnail URL': 1, 'sif_embeddings': 1}))
    for i in range(len(ink_data)):
        ink_data[i]['sif_embeddings'] = np.asarray(ink_data[i]['sif_embeddings'])
    return ink_data

# A function to process the query term and compare the query vector with
# document vectors to find the ones that are most similar.
#
# Returns: A sorted list of indexes of the document and it's similarity
# with the query term sorted in descending order.
def search_query(db, query, ink_data, n_terms=3, vector_size=50):
    processed_query = helper_functions.preprocess_text(query)
    v = np.zeros(vector_size)
    sif_embeddings = db.word_vectors.find({'word':{'$in': processed_query}})

    for vec in sif_embeddings:
        v += vec['vector']

    search_result = list()
    for idx, data in enumerate(ink_data):
        search_result.append([idx, helper_functions.cosine_similarity(v, data['sif_embeddings'])])

    search_result = sorted(search_result, key=lambda x: x[1], reverse=True)

    return search_result[:n_terms]

# A function to retreive the relevant rows from the dataframe df according to
# the indices in the similarity_list.
#
# Returns: A dataframe with all rows of the dataframe df whose indices are
# in similarity_list.
def get_search_results(search_result, ink_data):
    top_searches = list()
    for res in search_result:
        top_searches.append(ink_data[res[0]])
    return top_searches
