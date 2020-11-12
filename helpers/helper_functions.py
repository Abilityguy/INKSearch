import numpy as np
import re
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

# A function to compute the cosine similarity between two vectors.
#
# Returns: A number in the range [0,1] indicating the similarity between the
# two vectors.
def CosineSimilarity(v1, v2):
    dotProduct = np.dot(v1, v2)
    norm1 = np.linalg.norm(v1)
    norm2 = np.linalg.norm(v2)

    if (norm1 * norm2 == 0):
        return 0
    else:
        return min(dotProduct / (norm1 * norm2), 1)

# A function to preprocess the document text by removing punctuations, digits
# and stop words.
#
# Returns: A list of processed words from the document text.
def PreprocessText(text):
    stop_words = set(stopwords.words('english'))

    text = re.sub(r"\d+", " ", text)
    text = re.sub(r"[:\-,.;@#?!&$]+\ *", " ", text)
    text = text.strip()
    text = text.lower()
    text = word_tokenize(text)
    text = [word for word in text if word not in stop_words]
    return text

# A function to generate a document vector given a list of processed words from
# the document text and a word embedding model.
#
# Returns: A vector which is the average of the word embeddings of the processed
# words.
def GenerateDocumentVector(wordList, model):
    documentVector = np.zeros(model.vector_size)

    for word in wordList:
        if word in model:
            documentVector += model[word]

    documentVector /= len(wordList)
    return documentVector
