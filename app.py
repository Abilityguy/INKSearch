from flask import Flask, render_template, request
import os
import pandas as pd
import pickle
import gensim.downloader as api
from search_logic import SearchQuery, GetSearchResults

app = Flask(__name__)

model = api.load('glove-wiki-gigaword-50')

with open(os.path.join('document_vectors','document_vectors.pkl'), 'rb') as f:
    documentVectorList = pickle.load(f)

df = pd.read_csv(os.path.join('data','INKtalks_metaData.csv'))

@app.route('/', methods=['POST', 'GET'])
def index():
    if(request.method == 'POST'):
        queryTerm = request.form['query']
        similarityList = SearchQuery(queryTerm, documentVectorList, model)
        topSearches = GetSearchResults(similarityList, df)
        return render_template('index.html', results=topSearches, search=True)
    else:
        return render_template('index.html', search=False)

if __name__ == "__main__":
    app.run()
