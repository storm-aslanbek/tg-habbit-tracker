import pymongo


class Client:
    def __init__(self):
        self.client = pymongo.MongoClient('localhost', 27017)
        self.db = self.client['students_data']
        self.collection = self.db['students']
        self.habit_collection = self.db["habits"]
        self.task_collection = self.db["tasks"]

    def insert(self, data):
        self.collection.insert_one(data)

    # def get_name(self, name):
    #     student_list = []
    #     for value in self.collection.find({"_id": 0, "name": 1}):
    #         student_list.append(value)

    def update_data(self, current, new_data):
        self.collection.update_one(current, new_data)
        # current = {"name": "Aslanbek"}
        # new_data = {"$set": {"name": "new"}}

    def insert_habit(self, data):
        self.habit_collection.insert_one(data)

    def habits_sum(self):
        count = 1
        for value in self.habit_collection.find():
            count += 1
        return count

    def print_habits(self):
        query = ()
        habit_list = []
        for value in self.habit_collection.find(query, {"_id": 0, "time": 1, "description": 1}):
            habit_list.append(value)
        return habit_list


    def insert_task(self, data):
        self.task_collection.insert_one(data)
    def tasks_sum(self):
        count = 1
        for value in self.task_collection.find():
            count += 1
        return count

    def print_task(self):
        query = ()
        task_list = []
        for value in self.task_collection.find(query, {"_id": 0, "dedline": 1, "description": 1, "status": 1}):
            task_list.append(value)
        return task_list

    def update_task_status(self, current, new_data):
        self.task_collection.update_one(current, new_data)

if __name__ == '__main__':
    client = Client()
    # student_list = []
    # query = ()
    # for value in db.collection.find(query, {"_id": 0, "name": 1}):
    #     student_list.append(value.get("name"))
    #
    # print(student_list)

    print(client.print_habits())

