from flask import Flask, render_template, request
import os
import pandas as pd
import pickle
import gensim.downloader as api
from search_logic import search_query, get_search_results

app = Flask(__name__)

model = api.load('glove-wiki-gigaword-50')

with open(os.path.join('document_vectors','document_vectors.pkl'), 'rb') as f:
    document_vector_list = pickle.load(f)

df = pd.read_csv(os.path.join('data','INKtalks_metaData.csv'))

@app.route('/', methods=['POST', 'GET'])
def index():
    if(request.method == 'POST'):
        query_term = request.form['query']
        similarity_list = search_query(query_term, document_vector_list, model)
        top_searches = get_search_results(similarity_list, df)
        return render_template('index.html', results=top_searches, search=True)
    else:
        return render_template('index.html', search=False)

if __name__ == "__main__":
    app.run(host='0.0.0.0')
