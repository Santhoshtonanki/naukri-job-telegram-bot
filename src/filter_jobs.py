import re


JOB_KEYWORDS = [
    "devops",
    "aws devops",
    "cloud engineer",
    "cloud devops",
    "devops engineer",
    "devops associate",
    "site reliability engineer",
    "sre",
    "platform engineer",
]


def normalize_text(text):
    if not text:
        return ""

    text = re.sub(r"<[^>]+>", " ", text)
    text = re.sub(r"\s+", " ", text)

    return text.lower().strip()


def is_relevant_job(job):
    title = normalize_text(job.get("title", ""))

    description = job.get("description", {})

    if isinstance(description, dict):
        full_description = normalize_text(
            description.get("full", "")
        )
        short_description = normalize_text(
            description.get("short", "")
        )
    else:
        full_description = normalize_text(description)
        short_description = ""

    searchable_text = (
        f"{title} "
        f"{full_description} "
        f"{short_description}"
    )

    for keyword in JOB_KEYWORDS:
        if keyword in title:
            return True

    for keyword in JOB_KEYWORDS:
        if keyword in searchable_text:
            return True

    return False


def filter_jobs(jobs):
    filtered_jobs = []

    for job in jobs:
        if is_relevant_job(job):
            filtered_jobs.append(job)

    print(
        f"Relevant jobs: "
        f"{len(filtered_jobs)} / {len(jobs)}"
    )

    return filtered_jobs
