import re


# Relevant DevOps / Cloud job titles.
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

    text = re.sub(r"<[^>]+>", " ", str(text))
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
    Accept:

    - Intern / Internship
    - Fresher / Entry Level
    - 0 years
    - 0-1 years
    - 0-2 years
    - 1-2 years

    Reject jobs requiring more than 2 years.
    """

    experience = job.get("experience", {})

    minimum = experience.get("minimum")
    maximum = experience.get("maximum")

    experience_text = normalize_text(
        experience.get("text", "")
    )

    # ------------------------------------------------
    # 1. Explicit intern / internship
    # ------------------------------------------------

    intern_keywords = [
        "intern",
        "internship",
        "trainee",
    ]

    for keyword in intern_keywords:
        if keyword in experience_text:
            return True

    # ------------------------------------------------
    # 2. Explicit fresher / entry-level
    # ------------------------------------------------

    fresher_keywords = [
        "fresher",
        "freshers",
        "entry level",
        "entry-level",
        "graduate",
    ]

    for keyword in fresher_keywords:
        if keyword in experience_text:
            return True

    # ------------------------------------------------
    # 3. Numeric experience
    # ------------------------------------------------

    try:
        minimum = float(minimum)
    except (TypeError, ValueError):
        minimum = None

    try:
        maximum = float(maximum)
    except (TypeError, ValueError):
        maximum = None

    # If maximum experience is known,
    # it must not exceed 2 years.
    if maximum is not None:
        return maximum <= 2

    # If only minimum experience is available,
    # allow up to 2 years.
    if minimum is not None:
        return minimum <= 2

    # Unknown experience → reject
    return False


def is_relevant_job(job):
    """
    Job must satisfy BOTH:

    1. Relevant DevOps / Cloud / SRE title
    2. Intern / Fresher / Entry Level / <= 2 years
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

    return filtered_jobs
