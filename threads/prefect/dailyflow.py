import sys
from pathlib import Path

# Add the project root directory to sys.path
sys.path.append(str(Path(__file__).parent.parent.parent))

from threads import interact_chain, SerpAPI, Threads
from prefect import flow, task
from datetime import timedelta
from prefect.client.schemas.schedules import IntervalSchedule

@task
def serp_api():
    return SerpAPI().main()

@task
def chain(result):
    return interact_chain(result)

@task
def threads(output):
    return Threads().main(output)

@flow(log_prints=True)
def daily_flow():
    result = serp_api()
    output = chain(result)
    threads(output)

if __name__ == "__main__":
    daily_flow.serve(
        name="daily-flow-deployment",
        interval=60 * 60 * 12,  # Runs every 12 hours
        pause_on_shutdown=False  # Optional: prevents schedule from pausing on shutdown
    )
