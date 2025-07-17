from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional
from backend.queue import job_queue, agent_manager
from fastapi import HTTPException

app = FastAPI()

class JobPayload(BaseModel):
    org_id: str
    app_version_id: str
    test_path: str
    priority: Optional[int] = 1
    target: str  # emulator, device, browserstack

class AgentPayload(BaseModel):
    agent_id: str
    target: str

class AssignPayload(BaseModel):
    agent_id: str
    app_version_id: str

@app.get("/health")
def health_check():
    return {"status": "ok"}

@app.post("/jobs/submit")
def submit_job(payload: JobPayload):
    job = job_queue.add_job(
        org_id=payload.org_id,
        app_version_id=payload.app_version_id,
        test_path=payload.test_path,
        priority=payload.priority,
        target=payload.target
    )
    return {"message": "Job submitted", "job_id": job.job_id}

@app.post("/agents/register")
def register_agent(payload: AgentPayload):
    agent = agent_manager.register_agent(payload.agent_id, payload.target)
    return {"agent_id": agent.agent_id, "target": agent.target, "status": agent.status}

@app.get("/agents")
def list_agents():
    agents = agent_manager.list_agents()
    return [{
        "agent_id": agent.agent_id,
        "target": agent.target,
        "status": agent.status,
        "assigned_group": agent.assigned_group
    } for agent in agents]

@app.post("/agents/assign")
def assign_group(payload: AssignPayload):
    success = agent_manager.assign_group(payload.agent_id, payload.app_version_id)
    if not success:
        raise HTTPException(status_code=400, detail="Agent not available or already busy")
    return {"message": f"Group {payload.app_version_id} assigned to agent {payload.agent_id}"}

@app.get("/jobs/status/{job_id}")
def job_status(job_id: str):
    job = job_queue.get_job(job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    return {
        "job_id": job.job_id,
        "org_id": job.org_id,
        "app_version_id": job.app_version_id,
        "test_path": job.test_path,
        "priority": job.priority,
        "target": job.target,
        "status": job.status
    }

@app.get("/jobs/group/{app_version_id}")
def jobs_in_group(app_version_id: str):
    jobs = job_queue.get_group(app_version_id)
    return [{
        "job_id": job.job_id,
        "org_id": job.org_id,
        "app_version_id": job.app_version_id,
        "test_path": job.test_path,
        "priority": job.priority,
        "target": job.target,
        "status": job.status
    } for job in jobs] 