import re


JOB_TITLE_KEYWORDS = [
    "devops",
    "devops engineer",
    "aws devops",
    "cloud engineer",
    "cloud devops",
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


def is_relevant_title(job):
    title = normalize_text(job.get("title", ""))

    for keyword in JOB_TITLE_KEYWORDS:
        if keyword in title:
            return True

    return False


def has_required_experience(job):
    experience = job.get("experience", {})

    minimum = experience.get("minimum")
    maximum = experience.get("maximum")

    try:
        minimum = float(minimum)
        maximum = float(maximum)
    except (TypeError, ValueError):
        return False

    # We want strictly 1–2 years experience.
    return minimum >= 1 and maximum <= 2


def is_relevant_job(job):
    return (
        is_relevant_title(job)
        and has_required_experience(job)
    )


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
