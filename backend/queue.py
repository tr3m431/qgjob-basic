from typing import List, Dict, Optional
from threading import Lock

class Job:
    def __init__(self, job_id, org_id, app_version_id, test_path, priority, target):
        self.job_id = job_id
        self.org_id = org_id
        self.app_version_id = app_version_id
        self.test_path = test_path
        self.priority = priority
        self.target = target
        self.status = 'queued'

class Agent:
    def __init__(self, agent_id, target):
        self.agent_id = agent_id
        self.target = target  # emulator, device, browserstack
        self.status = 'idle'  # idle, busy
        self.assigned_group: Optional[str] = None  # app_version_id

class AgentManager:
    def __init__(self):
        self.agents: Dict[str, Agent] = {}
        self.lock = Lock()

    def register_agent(self, agent_id, target):
        with self.lock:
            if agent_id not in self.agents:
                self.agents[agent_id] = Agent(agent_id, target)
            return self.agents[agent_id]

    def list_agents(self):
        return list(self.agents.values())

    def assign_group(self, agent_id, app_version_id):
        with self.lock:
            agent = self.agents.get(agent_id)
            if agent and agent.status == 'idle':
                agent.status = 'busy'
                agent.assigned_group = app_version_id
                return True
            return False

    def release_agent(self, agent_id):
        with self.lock:
            agent = self.agents.get(agent_id)
            if agent:
                agent.status = 'idle'
                agent.assigned_group = None

class JobQueue:
    def __init__(self):
        self.jobs: Dict[str, Job] = {}
        self.groups: Dict[str, List[str]] = {}  # app_version_id -> list of job_ids
        self.lock = Lock()
        self.counter = 0

    def add_job(self, org_id, app_version_id, test_path, priority, target):
        with self.lock:
            self.counter += 1
            job_id = f"job_{self.counter}"
            job = Job(job_id, org_id, app_version_id, test_path, priority, target)
            self.jobs[job_id] = job
            if app_version_id not in self.groups:
                self.groups[app_version_id] = []
            self.groups[app_version_id].append(job_id)
            return job

    def get_job(self, job_id):
        return self.jobs.get(job_id)

    def list_jobs(self):
        return list(self.jobs.values())

    def get_group(self, app_version_id):
        job_ids = self.groups.get(app_version_id, [])
        jobs = [self.jobs[job_id] for job_id in job_ids]
        # Sort by priority (higher first), then by job_id (FIFO for same priority)
        jobs.sort(key=lambda job: (-job.priority, job.job_id))
        return jobs

job_queue = JobQueue()
agent_manager = AgentManager() 