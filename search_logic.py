from helpers.helper_functions import generate_document_vector, preprocess_text, cosine_similarity

# A function to process the query term and compare the query vector with
# document vectors to find the ones that are most similar.
#
# Returns: A sorted list of indexes of the document and it's similarity
# with the query term sorted in descending order.
def search_query(query_term, document_vector_list, model, n_terms=3):
    processed_query_term = preprocess_text(query_term)
    query_doc_vector = generate_document_vector(processed_query_term, model)

    similarity_list = list()
    for index,doc_vector in document_vector_list:
        similarity = cosine_similarity(query_doc_vector, doc_vector)
        similarity_list.append([index, similarity])

    similarity_list = sorted(similarity_list, key=lambda x:x[1], reverse=True)

    return similarity_list[:nTerms]

# A function to retreive the relevant rows from the dataframe df according to
# the indices in the similarity_list.
#
# Returns: A dataframe with all rows of the dataframe df whose indices are
# in similarity_list.
def get_search_results(similarity_list, df):
    indices = [x[0] for x in similarity_list]
    top_searches = df.iloc[indices]
    top_searches.reset_index(inplace=True)
    return top_searches
