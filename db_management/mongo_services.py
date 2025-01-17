import datetime
import json
import os
import gridfs
import pymongo

client = pymongo.MongoClient('localhost')
db = client['PhyloRNAdb']
collection = db['rna_sequences']

'''
It inserts files into the collection in the database
'''
def insert_to_mongo(dir_path):
    for file_to_read in os.listdir(dir_path):
        file_path = os.path.join(dir_path, file_to_read)
        if os.path.isfile(file_path):
            with open(file_path, 'r+') as file:
                file_data = json.load(file)
                if isinstance(file_data, list):
                    collection.insert_many(file_data)
                else:
                    collection.insert_one(file_data)
    print("The json files have been inserted to mongo db. \n")


'''
Given a name of a field to add, adds the field to every document of the collection.
'''


def add_one_field_all_docs():
    field = input("Insert the field you want to add to the rna_sequences collection: ")
    collection.update_many({}, {'$set': {field: "--"}})
    print("The field has been successfully added to the collection.")


'''
Given an accession number of a document, it modifies a field of that document
'''


def update_one_field():
    acc_number = input("Insert the accession number of the rna sequence you want to modify: ")
    old_document = collection.find_one({"Accession number": acc_number})
    print(old_document)
    if old_document is None:
        print("Invalid Accession Number")
        update_one_field()
    field = input(("Insert the field you want to change: "))
    new_input = input("Insert the new value of the field: ")
    collection.find_one_and_update({"Accession number": acc_number}, {"$set": {field: new_input}})
    if new_input == old_document.get(field):
        print("Sorry, we couldn't update the value.")
    else:
        print("The value was changed successfully.")
        print(collection.find_one({"Accession number": acc_number}))


'''
Delete one document from a collection. To remove the document, you need to enter the accession number of the document 
'''


def delete_one():
    acc_number = input("Insert the accession number of the rna sequence you want to delete: ")
    old_document = collection.find_one({"Accession number": acc_number})
    print(old_document)
    if old_document is None:
        print("Invalid Accession Number")
        delete_one()
    print("Are you sure you want to delete this document? y/n (default: n) ")
    answer = input()
    if answer.upper() == "Y" or answer.upper() == "YES":
        collection.find_one_and_delete({"Accession number": acc_number})
        print("The document has been deleted. \n")
    else:
        print("Operation Aborted. \n")


'''
Delete all documents from a given collection
'''


def delete_all():
    col_name = input("Insert the name of the collection of the documents you want to delete: ")
    print("Are you sure you want to delete all documents of this collection? y/n (default: n) ")
    answer = input()
    if answer.upper() == "Y" or answer.upper() == "YES":
        db.get_collection(col_name).delete_many({})
        print("All documents have been deleted. \n")
    else:
        print("Operation Aborted. \n")


'''
It inserts additional files into the database (the files can have the extensions .ct, .bpseq, .fasta, .dbn).
'''


def insert_files():
    dir_path = input("Insert the path of the directory containing the files you want to insert: ")
    for file_to_read in os.listdir(dir_path):
        file_location = dir_path + "/" + file_to_read
        if os.path.isfile(file_location):
            file_data = open(file_location, "rb")
            data = file_data.read()
            fs = gridfs.GridFS(db)
            fs.put(data, filename=file_to_read, _id=file_to_read)
    print("All the files have been uploaded.")


'''
Delete collections that have not been used within 10 days from their creation.
'''


def delete_unused_collection():
    time_format = '%Y-%m-%d'
    current_time = str(datetime.datetime.utcnow().date())
    current_time = datetime.datetime.strptime(current_time, time_format)
    lists_to_check = db.list_collection_names()
    for l in lists_to_check:
        if l != 'fs.chunks' and l != 'fs.files' and l != 'rna_sequences':
            if db.get_collection(l).count_documents({}) == 0:
                db.get_collection(l).drop()
            else:
                l_time = db.get_collection(l).find_one().get('_id').generation_time.date()
                l_time = datetime.datetime.strptime(str(l_time), time_format)
                if (current_time - datetime.timedelta(days=10)).date() >= l_time.date():
                    db.get_collection(l).drop()
    print("Collection removed successfully")
