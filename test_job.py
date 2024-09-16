import pytest
from unittest.mock import patch
from service.job import JobService
from models.job import JobCreateRequest, JobPopRequest
from database.job import JobDatabase
from pydantic import BaseModel

class UpdateResult(BaseModel):
        modified_count: int
        
@pytest.fixture
def mock_job_database():
    with patch.object(JobService, 'job_funcs') as mock_db:
        yield mock_db

def test_start_job(mock_job_database):
    job_data = JobCreateRequest(tokens=["token1", "token2"])
    result = JobService().start(job_data)
    assert isinstance(result, str)  # Assert the result is a string (inserted ID)

def test_get_job_list(mock_job_database):
    mock_job_database.getAll.return_value = [{"_id": "1", "tokens": ["token1"]}]
    result = JobService().getJobList()
    assert isinstance(result, list)
    assert result[0]["_id"] == "1"
    # mock_job_database.getAll.assert_called_once()

# def test_pop_success(mock_job_database): 
#     job_data = {"_id": "1", "tokens": ["token1", "token2"], "hasEnded": False}
#     updateResult = UpdateResult(modified_count=1)
#     mock_job_database.getById.return_value = job_data
#     mock_job_database.update.return_value = updateResult
#     result = JobService().pop(JobPopRequest(job_id="1", token="token1"))
#     if result == True:
#         assert result is True

def test_pop_failure_job_deactivated(mock_job_database):
    job_data = {"_id": "1", "tokens": [], "hasEnded": True}
    mock_job_database.getById.return_value = job_data

    with pytest.raises(Exception) as excinfo:
        JobService().pop(JobPopRequest(job_id="1", token="token1"))
    assert str(excinfo.value) == "Job deactivated"
    
def test_pop_failure_job_deactivated_2(mock_job_database):
    job_data = {"_id": "1", "tokens": ["token1", "token2"], "hasEnded": True}
    mock_job_database.getById.return_value = job_data
    
    with pytest.raises(Exception) as excinfo:
        JobService().pop(JobPopRequest(job_id="1", token="token1"))
    assert str(excinfo.value) == "Job deactivated"

def test_pop_failure_token_notfound(mock_job_database):
    job_data = {"_id": "1", "tokens": ["token1", "token2"], "hasEnded": False}
    mock_job_database.getById.return_value = job_data
    
    with pytest.raises(Exception) as excinfo:
        JobService().pop(JobPopRequest(job_id="1", token="token3"))
    assert str(excinfo.value) == "no token found"
    
def test_end_job_success(mock_job_database):
    job_data = {"_id": "1", "tokens": ["token1", "token2"], "hasEnded": False}
    updateResult = UpdateResult(modified_count=1)
    mock_job_database.getById.return_value = job_data
    mock_job_database.update.return_value = updateResult
    result = JobService().end(id="1")
    assert result is True
    
def test_end_job_failed(mock_job_database):
    job_data = {"_id": "1", "tokens": ["token1", "token2"], "hasEnded": False}
    updateResult = UpdateResult(modified_count=0)
    mock_job_database.getById.return_value = job_data
    mock_job_database.update.return_value = updateResult
    result = JobService().end(id="1")
    assert result is False