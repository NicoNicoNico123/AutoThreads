import sys
from pathlib import Path
import random

# Add the project root directory to sys.path
sys.path.append(str(Path(__file__).parent.parent.parent))

from threads.main import Main
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
def threads():
    local_thread = Main.local_thread()
    return local_thread

@flow(log_prints=True)
def daily_flow():
    threads()

if __name__ == "__main__":
    daily_flow.serve(
        name="yiying_threads_flow",
        interval=timedelta(minutes=random.randint(30, 120)),
        tags=["threads"]
    )
