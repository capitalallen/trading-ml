import pymongo


class Store_model_result:
    def __inti__(self):
        pass

    def record_model(self, data):
        try:

            client = pymongo.MongoClient(
                "mongodb+srv://allen123:allen123@cluster0.usmqn.gcp.mongodb.net/<dbname>?retryWrites=true&w=majority")
            db = client.get_database('ml_data')
            records = db.training_result
            model_result = data
            records.insert_one(model_result)
        except pymongo.errors.PyMongoError as e:
            print("insert unsuccessfully")
            return False

    def record_model_mean_reverting(self, data):
        try:

            client = pymongo.MongoClient(
                "mongodb+srv://allen123:allen123@cluster0.usmqn.gcp.mongodb.net/<dbname>?retryWrites=true&w=majority")
            db = client.get_database('ml_data')
            records = db.mean_reverting
            model_result = data
            records.insert_one(model_result)
        except pymongo.errors.PyMongoError as e:
            print(e)
            return False

    def record_error(self, data):
        try:
            client = pymongo.MongoClient(
                "mongodb+srv://allen123:allen123@cluster0.usmqn.gcp.mongodb.net/<dbname>?retryWrites=true&w=majority")
            db = client.get_database('ml_data')
            records = db.log_error
            model_result = data
            records.insert_one(model_result)
        except pymongo.errors.PyMongoError as e:
            print("insert unsuccessfully")
            return False

    def record_model_trend_following(self, data):
        try:
            client = pymongo.MongoClient(
                "mongodb+srv://allen123:allen123@cluster0.usmqn.gcp.mongodb.net/<dbname>?retryWrites=true&w=majority")
            db = client.get_database('ml_data')
            records = db.trend_following
            print(records)
            records.insert_one(data)
        except pymongo.errors.PyMongoError as e:
            print(e)
            return False
