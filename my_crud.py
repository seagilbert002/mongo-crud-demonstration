from pymongo import MongoClient
from bson.objectid import ObjectId

class MyCrud(object):
    """ CRUD operations for Animal collection in MongoDB """
    
    def __init__(self, username, password):
        # Initializing the MongoClient will be hard-wired to access only the animals collection.

        # Connection Variables
        # USER = 'aacuser'
        # PASS = 'WhoaAcuser14!'
        HOST = 'nv-desktop-services.apporto.com'
        PORT = 33277
        DB = 'AAC'
        COL = 'animals'

        # Now we attempt initialize the Connection
        try:
            self.client = MongoClient('mongodb://%s:%s@%s:%d' % (username,password,HOST,PORT))
            self.database = self.client['%s' % (DB)]
            self.collection = self.database['%s' % (COL)]
        except Exception as e:
            print(f"Error connecting to Database: {e}")
            self.client = None
            self.db = None

    # create function to insert data into the database
    def create(self, data):
        if data is not None:
            result = self.database.animals.insert_one(data) # data should be a dictionary
            return result.inserted_id
        else:
            raise Exception("Nothing to save, because data parameter is empty")

    # read function to find information sored in the database.
    def read(self, data):
        if data is not None:
            return self.database.animals.find(data) # data should be a retievable dictionary
        else:
            raise Exception("Nothing to retrieve, because data parameter is empyt")
            
    # update function to modify data in the database
    def update(self, query, new_values):
        if query is not None and new_values is not None:
            result = self.database.animals.update_many(query, {"$set": new_values})
            return {
                "matched_count": result.matched_count,
                "modified_count": result.modified_count
            }
        else:
            raise Exception("Missing query or update data")
            
    def delete(self, query):
        if query is not None:
            result = self.database.animals.delete_many(query)
            return {
                "deleted_count": result.deleted_count
            }
        else:
            raise Exception("Nothing to delete, because query is is empty")