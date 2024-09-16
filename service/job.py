import json, bson, random, time
from models.job import JobCreateRequest, JobPopRequest
from database.job import JobDatabase


class JobService:
    job_funcs = JobDatabase()
    def __init__(self) -> None:
        pass
        
    def start(self, job: JobCreateRequest):
        request = {
            "tokens": job.tokens,
            "hasEnded": False
        }
        result = JobService.job_funcs.create(job=request).inserted_id
        return str(result)
    
    def getJobList(self) -> list:
        result = JobService.job_funcs.getAll()
        serialized = json.loads(bson.json_util.dumps(result))
        return serialized
    
    def pop(self, req_data: JobPopRequest) -> bool:
        job = JobService.job_funcs.getById(req_data.job_id)
        tokens = list(job.get('tokens'))
        if bool(job.get('hasEnded')) or len(tokens) == 0:
            raise Exception("Job deactivated")
        if req_data.token not in tokens:
            raise Exception("no token found")
        
        time.sleep(3)
        isFailed = bool(random.getrandbits(1))
        if not isFailed:
            tokens.remove(req_data.token)
            updateQuery = { "$set": { 'tokens': tokens } }
            updatedResult = JobService.job_funcs.update(req_data.job_id, updateQuery)
            if updatedResult.modified_count == 1:
                return True
            else:
                return False
        else:
            raise Exception("job failed!!!")
    
    def end(self, id: str) -> bool:
        updateQuery = { "$set": { 'hasEnded': True } }
        updatedResult = JobService.job_funcs.update(id, updateQuery)
        if updatedResult.modified_count == 1:
            return True
        else:
            return False