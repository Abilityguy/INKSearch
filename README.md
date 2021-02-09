# INKSearch

INKSearch is a INK talk video search engine, which searches through more than 350 videos and retreives relevant results for you to watch.

![INKSearch](extras/INKSearch.gif?style=centerme)

## Environment setup
After cloning this repository, navigate to the INKSearch folder and run the following commands.
```
python3 -m venv env
source env/bin/activate
pip3 install -r requirements.txt
```
## To run
Add the MongoDB Connection String URI in ```app.py```, ```upload_data.py``` and ```upload_vectors.py```. Run the scripts ```upload_data.py``` and ```upload_vectors.py``` to insert data into the MongoDB database. Then,
```
python3 app.py
```
And navigate to http://localhost:5000/

## Data
The data was extracted using the code from this [repository](https://github.com/Abilityguy/INK-talks-scraper).

## Live Project
You can access a live version of the project [here](https://ink-search.herokuapp.com/).
