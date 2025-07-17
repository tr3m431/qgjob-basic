import click
import requests

API_URL = "http://localhost:8000"

@click.group()
def cli():
    """qgjob CLI tool for submitting and tracking test jobs."""
    pass

@cli.command()
@click.option('--org-id', required=True, help='Organization ID')
@click.option('--app-version-id', required=True, help='App Version ID')
@click.option('--test', 'test_path', required=True, help='Test file path')
@click.option('--priority', default=1, help='Job priority')
@click.option('--target', required=True, type=click.Choice(['emulator', 'device', 'browserstack']), help='Target device type')
def submit(org_id, app_version_id, test_path, priority, target):
    """Submit a test job."""
    payload = {
        "org_id": org_id,
        "app_version_id": app_version_id,
        "test_path": test_path,
        "priority": priority,
        "target": target
    }
    resp = requests.post(f"{API_URL}/jobs/submit", json=payload)
    if resp.ok:
        click.echo(f"Job submitted: {resp.json()['job_id']}")
    else:
        click.echo(f"Error: {resp.text}")

@cli.command()
@click.option('--job-id', required=True, help='Job ID to check status')
def status(job_id):
    """Check the status of a job."""
    resp = requests.get(f"{API_URL}/jobs/status/{job_id}")
    if resp.ok:
        job = resp.json()
        click.echo(f"Job {job['job_id']} status: {job['status']}")
    else:
        click.echo(f"Error: {resp.text}")

if __name__ == "__main__":
    cli() 