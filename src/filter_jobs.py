import re


# Job titles that are relevant to our DevOps job search.
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
    """
    Remove HTML tags, extra spaces and convert text to lowercase.
    """

    if not text:
        return ""

    text = re.sub(r"<[^>]+>", " ", text)
    text = re.sub(r"\s+", " ", text)

    return text.lower().strip()


def is_relevant_title(job):
    """
    Check whether the job title is related to
    DevOps / Cloud / SRE / Platform Engineering.
    """

    title = normalize_text(job.get("title", ""))

    for keyword in JOB_TITLE_KEYWORDS:
        if keyword in title:
            return True

    return False


def has_required_experience(job):
    """
    Accept only jobs requiring 1 to 2 years of experience.

    Examples:

    1-2 Yrs  → YES
    1-3 Yrs  → NO
    2-5 Yrs  → NO
    5-10 Yrs → NO
    """

    experience = job.get("experience", {})

    minimum = experience.get("minimum")
    maximum = experience.get("maximum")

    try:
        minimum = float(minimum)
        maximum = float(maximum)

    except (TypeError, ValueError):
        return False

    return minimum >= 1 and maximum <= 2


def is_relevant_job(job):
    """
    A job is relevant only when BOTH conditions are satisfied:

    1. Relevant DevOps/Cloud/SRE title
    2. Experience requirement is strictly 1-2 years
    """

    return (
        is_relevant_title(job)
        and has_required_experience(job)
    )


def filter_jobs(jobs):
    """
    Filter the complete list of fetched jobs.
    """

    filtered_jobs = []

    for job in jobs:

        if is_relevant_job(job):
            filtered_jobs.append(job)

    print(
        f"Relevant jobs: "
        f"{len(filtered_jobs)} / {len(jobs)}"
    )

    return filtered_jobsdef has_required_experience(job):
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
