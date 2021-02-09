import csv
import argparse
import pymongo
import ast

def parse_csv(csvfilename):
    csvfile = open(csvfilename)
    reader = parse_rows(csv.DictReader(csvfile))

    return reader

# A function to process each row of the csv.
#
# Returns: A generator that yields a row of data after processing.
def parse_rows(generator):
    for row in generator:
        row["Id"] = int(row["Id"])

        row['Views'] = row['Views'].strip()
        row['Views'] = row['Views'].replace(',', '')
        row['Views'] = int(row['Views'])

        row['Recommended Videos'] = ast.literal_eval(row['Recommended Videos'])
        row['tags'] = ast.literal_eval(row['tags'])
        try:
            row['Speakers'] = ast.literal_eval(row['Speakers'])
        except:
            row['Speakers'] = row['Speakers'].replace('[', '["')
            row['Speakers'] = row['Speakers'].replace(']', '"]')
            row['Speakers'] = ast.literal_eval(row['Speakers'])

        yield row

# Insert INK video data into the database.
#
# Returns: Object Ids of inserted documents.
def insert_data(db, data):
    inserted_ids = db.inktalks.insert_many(data).inserted_ids
    return inserted_ids

def make_data_indexes(db):
    db.inktalks.create_index("Id", unique=True)
    db.inktalks.create_index("Title", unique=True)
    db.inktalks.create_index("Talk URL", unique=True)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--filename', type=str, required=True)
    args = parser.parse_args()

    MONGO_SRV = "" # Add MongoDB Connection String URI here.

    mongo_client = pymongo.MongoClient(MONGO_SRV)
    db = mongo_client.db

    data = parse_csv(args.filename)
    make_data_indexes(db)
    inserted_ids = insert_data(db, data)
    print(f"Inserted {len(inserted_ids)} documents")

if __name__ == "__main__":
    exit(main())
