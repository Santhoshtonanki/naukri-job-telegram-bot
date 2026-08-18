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
    """
    Remove HTML tags, extra spaces and convert to lowercase.
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
    - Trainee
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

    # Intern / Internship / Trainee
    intern_keywords = [
        "intern",
        "internship",
        "trainee",
    ]

    for keyword in intern_keywords:
        if keyword in experience_text:
            return True

    # Fresher / Entry Level
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

    # Numeric experience
    try:
        minimum = float(minimum)
    except (TypeError, ValueError):
        minimum = None

    try:
        maximum = float(maximum)
    except (TypeError, ValueError):
        maximum = None

    # Maximum experience must not exceed 2 years
    if maximum is not None:
        return maximum <= 2

    # If only minimum is available
    if minimum is not None:
        return minimum <= 2

    return False


def get_job_text(job):
    """
    Combine useful job fields into searchable text.
    """

    description = job.get("description", {})

    if isinstance(description, dict):
        full_description = description.get("full", "")
        short_description = description.get("short", "")
    else:
        full_description = description or ""
        short_description = ""

    return normalize_text(
        " ".join([
            str(job.get("title", "")),
            str(job.get("url", "")),
            str(full_description),
            str(short_description),
        ])
    )


def has_visa_sponsorship(job):
    """
    Detect explicit visa sponsorship / visa support.
    """

    text = get_job_text(job)

    sponsorship_keywords = [
        "visa sponsorship",
        "visa sponsored",
        "visa sponsor",
        "sponsor visa",
        "work visa sponsorship",
        "visa support",
        "sponsorship available",
        "sponsorship provided",
        "visa assistance",
        "relocation and visa",
        "relocation assistance and visa",
    ]

    for keyword in sponsorship_keywords:
        if keyword in text:
            return True

    return False


def is_location_eligible(job):
    """
    Current Naukri scraper is focused on India.

    Office, Remote and Hybrid jobs are allowed.
    """

    wfh_type = str(job.get("wfhType", ""))

    # 0 = Office
    # 2 = Remote
    # 3 = Hybrid
    if wfh_type in ["0", "2", "3"]:
        return True

    # Allow if work mode is unavailable.
    if not wfh_type or wfh_type == "None":
        return True

    return has_visa_sponsorship(job)


def is_relevant_job(job):
    """
    Job must satisfy:

    1. Relevant DevOps / Cloud / SRE title
    2. Intern / Fresher / Entry Level / <= 2 years
    3. Eligible location/work mode
    """

    return (
        is_relevant_title(job)
        and has_required_experience(job)
        and is_location_eligible(job)
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
