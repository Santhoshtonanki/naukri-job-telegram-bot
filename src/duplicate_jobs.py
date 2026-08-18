import json
import os


SENT_JOBS_FILE = "sent_jobs.json"


def load_sent_jobs():
    """
    Load previously sent job IDs/URLs.
    """

    if not os.path.exists(SENT_JOBS_FILE):
        return set()

    try:
        with open(SENT_JOBS_FILE, "r", encoding="utf-8") as file:
            data = json.load(file)

        return set(data)

    except (json.JSONDecodeError, OSError):
        return set()


def get_job_key(job):
    """
    Use Naukri job ID as the primary duplicate key.
    Fall back to URL if ID is unavailable.
    """

    job_id = job.get("id")
    job_url = job.get("url")

    return job_id or job_url


def filter_new_jobs(jobs, sent_jobs):
    """
    Return only jobs that have not been sent before.
    """

    new_jobs = []

    for job in jobs:

        job_key = get_job_key(job)

        if not job_key:
            continue

        if job_key in sent_jobs:
            continue

        new_jobs.append(job)

    print(
        f"New jobs after previous-send check: "
        f"{len(new_jobs)} / {len(jobs)}"
    )

    return new_jobs


def save_sent_jobs(sent_jobs):
    """
    Save sent job IDs/URLs for future workflow runs.
    """

    with open(
        SENT_JOBS_FILE,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            sorted(sent_jobs),
            file,
            indent=2
        )
