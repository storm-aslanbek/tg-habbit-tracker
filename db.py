from pymongo import MongoClient


class Client:
    def __init__(self):
        self.client = MongoClient('localhost', 27017)
        self.db = self.client['students_data']
        self.collection = self.db['students']
        self.task_collection = self.db["tasks"]

    def insert(self, data):
        self.collection.insert_one(data)

    # def get_name(self, name):
    #     student_list = []
    #     for value in self.collection.find({"_id": 0, "name": 1}):
    #         student_list.append(value)


if __name__ == '__main__':

    db = Client()
    student_list = []
    query = ()
    for value in db.collection.find(query, {"_id": 0, "name": 1}):
        student_list.append(value.get("name"))

    print(student_list)