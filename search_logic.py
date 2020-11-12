from helpers.helper_functions import GenerateDocumentVector, CosineSimilarity, PreprocessText

# A function to process the query term and compare the query vector with
# document vectors to find the ones that are most similar.
#
# Returns: A sorted list of indexes of the document and it's similarity
# with the query term sorted in descending order.
def SearchQuery(queryTerm, documentVectorList, model, nTerms=3):
    processedQueryTerm = PreprocessText(queryTerm)
    queryDocVector = GenerateDocumentVector(processedQueryTerm, model)

    similarityList = list()
    for index,docVector in documentVectorList:
        similarity = CosineSimilarity(queryDocVector, docVector)
        similarityList.append([index, similarity])

    similarityList = sorted(similarityList, key=lambda x:x[1], reverse=True)

    return similarityList[:nTerms]

# A function to retreive the relevant rows from the dataframe df according to
# the indices in the similarityList.
#
# Returns: A dataframe with all rows of the dataframe df whose indices are
# in similarityList.
def GetSearchResults(similarityList, df):
    indices = [x[0] for x in similarityList]
    topSearches = df.iloc[indices]
    topSearches.reset_index(inplace=True)
    return topSearches
