from bson import ObjectId
from database._manager import MongoDB
from models.job import Job

mongo = MongoDB()

class JobDatabase:
    def __init__(self) -> None:    
        self.job_db = mongo.db["jobs"]
    
    def create(self, job: Job):
        return self.job_db.insert_one(job)
    
    def update(self, id, updateQuery):
        return self.job_db.update_one({"_id": ObjectId(id)}, updateQuery)
        
    def getAll(self):
        return self.job_db.find({})
    
    def getById(self, id):
        return self.job_db.find_one({"_id": ObjectId(id)})
    
    def delete(self, id) -> None:
        return self.job_db.find_one({"_id": ObjectId(id)})
    