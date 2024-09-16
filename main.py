from models.job import JobCreateRequest, JobPopRequest
from service.job import JobService
from database._manager import MongoDB
from fastapi.responses import JSONResponse, Response
from fastapi import FastAPI, HTTPException, status

app = FastAPI()
mongo = MongoDB()
job_service = JobService()

@app.post("/start")
def start_job(req: JobCreateRequest):
    try:
        return JSONResponse(status_code=status.HTTP_201_CREATED, content={"_id": job_service.start(req)})
    except Exception as e:
        return Response(status_code=status.HTTP_400_BAD_REQUEST, content=str(e))

@app.put("/pop")
def pop_token(req: JobPopRequest):
    try:
        if not job_service.pop(req):
            return Response(status_code=status.HTTP_400_BAD_REQUEST, content="Mongo db error when updating")
        return JSONResponse(status_code=status.HTTP_202_ACCEPTED, content={"message": "update success"})
    except Exception as e:
        return Response(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content=str(e))

@app.put("/end/{job_id}")
def end_user(job_id: str):
    try:
        if not job_service.end(job_id):
            return Response(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content="Mongo db error when updating")
        return JSONResponse(status_code=status.HTTP_202_ACCEPTED, content={"message": "update success"})
    except Exception as e:
        return Response(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content=str(e))

@app.get("/tracker")
def get_tracker():
    try:
        return job_service.getJobList()
    except Exception as e:
        return Response(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content=str(e))

