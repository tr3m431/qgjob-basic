# QualGent Backend Coding Challenge

## Overview
This project implements a modular test job orchestration system for AppWright, including:
- A Python CLI tool (`qgjob`) for submitting and tracking test jobs
- A backend REST API service for job queueing, grouping, and scheduling
- GitHub Actions integration for CI workflows

## Project Structure
```
qgjob-basic/
├── backend/           # Backend REST API service (FastAPI)
├── cli/               # CLI tool (Python, Click)
├── .github/
│   └── workflows/     # GitHub Actions workflow
├── README.md
└── requirement.txt
```

## Setup
1. Install dependencies:
   ```sh
   pip install -r requirement.txt
   ```
2. Start the backend server:
   ```sh
   uvicorn backend.main:app --reload
   ```

## CLI Usage
Submit a job:
```sh
python3 cli/qgjob.py submit --org-id=qualgent --app-version-id=xyz123 --test=tests/onboarding.spec.js --target=emulator --priority=5
```
Check job status:
```sh
python3 cli/qgjob.py status --job-id=job_1
```

## API Endpoints
- `POST /jobs/submit` — Submit a job
- `GET /jobs/status/{job_id}` — Get job status
- `GET /jobs/group/{app_version_id}` — List jobs in a group (sorted by priority)
- `POST /agents/register` — Register an agent
- `GET /agents` — List agents
- `POST /agents/assign` — Assign a group to an agent

## How Grouping, Scheduling, and Prioritization Work
- **Grouping:** Jobs are grouped by `app_version_id` to minimize redundant app installs.
- **Prioritization:** Jobs within a group are sorted by priority (higher first), then by submission order (FIFO).
- **Agent Assignment:** Agents register with a target type and can be assigned job groups when available.

## End-to-End Test Example
1. Start backend.
2. Submit jobs via CLI (with different priorities).
3. Register and assign agents via API.
4. Query job groups and agent status to verify grouping and assignment.

## Requirement Mapping
| Requirement | Implementation |
|-------------|----------------|
| **CLI Tool** | `cli/qgjob.py` provides `submit` and `status` commands, communicating with the backend via REST. |
| **Backend Service** | `backend/main.py` and `backend/queue.py` implement job queueing, grouping, prioritization, and agent assignment. |
| **Job Grouping** | Jobs are grouped by `app_version_id` in the backend for efficient scheduling. |
| **Agent Assignment** | Agents register and are assigned job groups based on availability and target type. |
| **Job Prioritization** | Jobs within a group are sorted by priority (higher first), then FIFO. |
| **Retry/Failure Handling** | (Not yet implemented, but can be added as an extension.) |
| **Horizontal Scalability** | The design is modular and can be extended to use Redis/PostgreSQL for distributed queueing. |
| **GitHub Actions Integration** | Example workflow in `.github/workflows/appwright-test.yml` demonstrates CLI usage in CI. |
| **Documentation** | This README provides setup, usage, and requirement mapping. |

## Sample Output
```
$ python3 cli/qgjob.py submit --org-id=qualgent --app-version-id=xyz123 --test=tests/onboarding.spec.js --target=emulator --priority=5
Job submitted: job_1

$ python3 cli/qgjob.py status --job-id=job_1
Job job_1 status: queued

$ curl -s http://127.0.0.1:8000/jobs/group/xyz123 | python3 -m json.tool
[
  {"job_id": "job_1", "priority": 5, ...},
  ...
]
```
