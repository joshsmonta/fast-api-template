from fastapi import APIRouter, Body, Request, Response, HTTPException, status
from fastapi.encoders import jsonable_encoder
from typing import List

from models.job import JobCreateRequest, JobPopRequest,
from service.job import JobService

job_service = JobService()
router = APIRouter()

@router.post("/start", status_code=status.HTTP_201_CREATED, response_model=Job)
def start_job(req: JobCreateRequest):
    try:
        return JSONResponse(status_code=201, content={"_id": job_service.start(req)})
    except Exception as e:
        return JSONResponse(status_code=400, content={"message": str(e)})

@app.post("/pop")
def pop_token(req: JobPopRequest):
    try:
        if not job_service.pop(req):
            return JSONResponse(status_code=500, content={"message": "Mongo db error when updating"})
        return JSONResponse(status_code=204, content={})
    except Exception as e:
        return JSONResponse(status_code=500, content={"message": str(e)})

@app.post("/end/{job_id}")
def end_user(job_id: str):
    try:
        if not job_service.end(job_id):
            return JSONResponse(status_code=500, content={"message": "Mongo db error when updating"})
        return JSONResponse(status_code=204, content={})
    except Exception as e:
        return JSONResponse(status_code=500, content={"message": str(e)})

@app.get("/tracker")
def get_tracker():
    try:
        return job_service.getJobList()
    except Exception as e:
        return JSONResponse(status_code=500, content={"message": str(e)})