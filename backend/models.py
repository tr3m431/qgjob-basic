from pydantic import BaseModel
from typing import Optional

class JobResponse(BaseModel):
    job_id: str
    org_id: str
    app_version_id: str
    test_path: str
    priority: Optional[int]
    target: str
    status: str 