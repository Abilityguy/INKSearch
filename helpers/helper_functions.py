import numpy as np
import re
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

# A function to compute the cosine similarity between two vectors.
#
# Returns: A number in the range [0,1] indicating the similarity between the
# two vectors.
def cosine_similarity(v1, v2):
    dot_product = np.dot(v1, v2)
    norm1 = np.linalg.norm(v1)
    norm2 = np.linalg.norm(v2)

    if (norm1 * norm2 == 0):
        return 0
    else:
        return min(dot_product / (norm1 * norm2), 1)

# A function to preprocess the document text by removing punctuations, digits
# and stop words.
#
# Returns: A list of processed words from the document text.
def preprocess_text(text):
    stop_words = set(stopwords.words('english'))

    text = re.sub(r"\d+", " ", text) #replace digits with a whitespace
    text = re.sub(r"[:\-,.;@#?!&$]+\ *", " ", text) #replace punctuations with a whitespace
    text = text.strip() #remove leading and trailing spaces
    text = text.lower()
    text = word_tokenize(text)
    text = [word for word in text if word not in stop_words] #remove stopwords from the word list
    return text

# A function to generate a document vector given a list of processed words from
# the document text and a word embedding model.
#
# Returns: A vector which is the average of the word embeddings of the processed
# words.
def generate_document_vector(word_list, model):
    document_vector = np.zeros(model.vector_size)

    for word in word_list:
        if word in model:
            document_vector += model[word]

    document_vector /= len(word_list)
    return document_vector
