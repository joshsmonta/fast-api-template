
from fastapi import FastAPI
from fastapi.testclient import TestClient
from dotenv import dotenv_values
from pymongo import MongoClient
from models.job import Job
from main import app

config = dotenv_values(".env")

def test_job_default_init():
    job = Job(tokens=["token1", "token2", "token3"], hasEnded=False)
    assert job.tokens == ["token1", "token2", "token3"]
    assert job.hasEnded == False
    
def test_job_start():
    with TestClient(app) as client:
        response = client.post("/start/", json={"tokens": ['token1', 'token2', 'token3']})
        assert response.status_code == 201
        assert "_id" in response.json()