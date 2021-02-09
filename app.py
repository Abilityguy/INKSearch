from flask import Flask, render_template, request
import search_logic
import pymongo

app = Flask(__name__)

MONGO_SRV = ""

mongo_client = pymongo.MongoClient(MONGO_SRV)
db = mongo_client.db

ink_data = search_logic.get_ink_vectors(db)

@app.route('/', methods=['POST', 'GET'])
def index():
    if(request.method == 'POST'):
        query = request.form['query']
        search_result = search_logic.search_query(db, query, ink_data)
        top_searches = search_logic.get_search_results(search_result, ink_data)
        return render_template('index.html', results=top_searches, search=True)
    else:
        return render_template('index.html', search=False)

if __name__ == "__main__":
    app.run(host='localhost', port=5000)
